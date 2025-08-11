"""FastAPI application entry point."""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.core.constants import ChannelEnum
from app.core.logger import logger
from app.helpers.account_helper import AccountHelper
from app.helpers.customer_helper import CustomerHelper
from app.helpers.mongo_helper import MongoHelper
from app.helpers.risk_engine_helper import RiskEvaluator
from app.helpers.transaction_helper import TransactionHelper
from app.models.collections.user_cache_model import KnowlegedDestinations
from app.models.tables.account_model import Account
from app.models.tables.transaction_model import Transaction
from app.schemas.transaction_schemas import PutTransactionRequest

router = APIRouter(prefix="/api/transaction")


@router.put("/create", status_code=status.HTTP_201_CREATED)
def put_transaction(data: PutTransactionRequest):
    """
    Create a new transaction based on the given data.

    Args:
        data (PutTransactionRequest): The transaction data.
        db (Session): The database session.

    Returns:
        JSON response with a message and a boolean indicating if the transaction is suspect.

    Raises:
        HTTPException: If the channel code is invalid or if any unexpected error happens.
    """
    if (
        data.agencia_de_origem == data.agencia_de_destino
        and data.conta_de_origem == data.conta_de_destino
    ):
        # Use o estilo %s para lazy evaluation
        logger.error(
            "Origin and destination accounts cannot be the same: %s/%s",
            data.agencia_de_origem,
            data.conta_de_origem,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Origin and destination accounts cannot be the same",
        )
    transaction_helper = TransactionHelper()
    account_helper = AccountHelper()
    customer_helper = CustomerHelper()
    mongo_helper = MongoHelper()
    origin_account = Account(
        agency=data.agencia_de_origem, account=data.conta_de_origem
    )
    dest_account = Account(
        agency=data.agencia_de_destino, account=data.conta_de_destino
    )
    origin_account = account_helper.get_account(origin_account)
    if not origin_account:
        # Use o estilo %s para lazy evaluation
        logger.error(
            "Origin account not found (agency/account) %s/%s",
            data.agencia_de_origem,
            data.conta_de_origem,
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Origin account not found",
        )
    dest_account = account_helper.get_account(dest_account)
    if not dest_account:
        # Use o estilo %s para lazy evaluation
        logger.error(
            "Destination account not found (agency/account) %s/%s",
            data.agencia_de_destino,
            data.conta_de_destino,
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination account not found",
        )

    risk_evaluator = RiskEvaluator()
    try:
        channel = ChannelEnum(data.canal)
    except ValueError as e:
        # Use o estilo %s e a mensagem do HTTPException
        logger.error(
            "Invalid channel code, use one of the following values: %s",
            [member.name for member in ChannelEnum],
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid channel code, use one of the following values",
        ) from e

    origin_account.customer_rel = customer_helper.get_customer_by_id(origin_account)
    transaction = Transaction(
        id=data.id_da_transacao,
        origin_account_id=origin_account.customer_id,
        destination_account_id=dest_account.customer_id,
        amount=data.valor_da_transacao,
        channel=channel,
        created_at=data.data_e_hora_da_transacao.replace(tzinfo=None),
        origin_account_rel=origin_account,
        destination_account_rel=dest_account,
    )

    is_suspect = risk_evaluator.calculate_risk(transaction=transaction)

    transaction.suspect = is_suspect

    try:
        transaction = transaction_helper.insert(transaction)
        # Use o estilo %s
        logger.info("Transaction created %s", transaction.id)

    except (SQLAlchemyError, IntegrityError) as e:
        if "duplicate key" in str(getattr(e.orig, "diag", "")).lower():
            # Use uma mensagem mais genérica, pois o exc_info=True já captura o detalhe
            logger.error("Database error: Duplicate key", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Transaction already exists",
            ) from e
        # Use uma mensagem mais genérica
        logger.error("Database error", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e

    except Exception as e:
        # Use uma mensagem mais genérica
        logger.error("An unexpected error occurred", exc_info=True)
        raise HTTPException(
            status_code=status.WS_1011_INTERNAL_ERROR, detail=str(e)
        ) from e

    mongo_helper.save(
        KnowlegedDestinations(
            origin_user=transaction.origin_account_id,
            destination_user=transaction.destination_account_id,
        )
    )

    return {"message": "Created", "suspect": transaction.suspect}
