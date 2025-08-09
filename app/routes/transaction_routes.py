""""Customer routes""" ""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.constants import ChannelEnum
from app.core.postgres_database import get_db
from app.helpers.account_helper import AccountHelper
from app.helpers.transaction_helper import TransactionHelper
from app.models.account_model import Account
from app.models.transaction_model import Transaction
from app.schemas.transaction import PutTransactionRequest

router = APIRouter(prefix="/api/transaction")


@router.put("/", status_code=status.HTTP_201_CREATED)
def put_transaction(
    data: PutTransactionRequest,
    db: Session = Depends(get_db),
):
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
    origin_account = Account(
        agency=data.agencia_de_origem, account=data.conta_de_origem
    )
    dest_account = Account(
        agency=data.agencia_de_destino, account=data.conta_de_destino
    )
    try:
        channel = ChannelEnum(data.canal)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid channel code",
        ) from e

    transaction_helper = TransactionHelper(db)
    account_helper = AccountHelper(db)
    transaction = Transaction(
        origin_account_rel=account_helper.get_account(origin_account),
        destination_account_rel=account_helper.get_account(dest_account),
        amount=data.valor_da_transacao,
        channel=channel,
        type=transaction_type,  # TODO: remover isso
        suspect=False,  # TODO: implementar calculo de risco
        transaction_date=datetime.fromtimestamp(data.data_e_hora_da_transacao),
    )
    try:
        transaction_helper.insert(transaction)

    except (SQLAlchemyError, IntegrityError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.WS_1011_INTERNAL_ERROR, detail=str(e)
        ) from e
    return {"message": "Created", "suspect": transaction.suspect}
