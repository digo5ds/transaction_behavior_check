""" "Customer routes"""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.core.logger import logger
from app.helpers.account_helper import AccountHelper
from app.helpers.customer_helper import CustomerHelper
from app.models.tables.account_model import Account
from app.models.tables.customer_model import Customer
from app.schemas.account_schemas import AccountInfoResponse
from app.schemas.customer_schemas import GetCustomerRequest, PutCustomerRequest

router = APIRouter(prefix="/api/customers")


@router.put("/{agencia}/{conta}", status_code=status.HTTP_201_CREATED)
def put_customer(agencia: int, conta: int, data: PutCustomerRequest):
    """
    Creates a new customer with the given agency, account, name, and age.

    Args:
        agencia (int): Agency number.
        conta (int): Account number.
        data (PutCustomerRequest): Object containing the customer's name and age.
        db (Session): SQLAlchemy database session.

    Returns:
        JSON response with a success message.

    Raises:
        HTTPException: If the agency and account numbers do not match.
    """
    if agencia != data.agencia or conta != data.conta:
        logger.error("Agency and account numbers do not match: %s/%s", agencia, conta)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Agency and account numbers do not match. Update is not allowed",
        )

    customer_helper = CustomerHelper()
    account_helper = AccountHelper()
    customer = Customer(name=data.nome, age=data.idade)
    account = Account(agency=data.agencia, account=data.conta)

    try:
        customer = customer_helper.insert(customer=customer)
        account.customer_id = customer.id
        account_helper.save_account(account=account)
        logger.info("Customer created with ID: %s", customer.id)
        return {"message": "Created"}

    except IntegrityError as e:
        if "duplicate key" in str(e.orig).lower():
            customer_helper.delete(customer)
            logger.error("Database error: Duplicate key", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Accout (agency/account) already exists",
            ) from e


@router.get("/{agencia}/{conta}")
def get_customer_info(agencia: int, conta: int):
    """
    Retrieves a customer's information based on their agency and account numbers.

    Args:
        agencia (int): Agency number.
        conta (int): Account number.
        db (Session): SQLAlchemy database session.

    Returns:
        JSON response with the customer's name, age, balance, and last transactions.

    Raises:
        HTTPException: If the account is not found or if any unexpected error occurs.
    """
    account_helper = AccountHelper()
    request_model = GetCustomerRequest(agencia=agencia, conta=conta)

    account = account_helper.get_account(
        Account(agency=request_model.agencia, account=request_model.conta)
    )

    if account is None:
        logger.error("Account not found for agency/account: %s/%s", agencia, conta)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    result = account_helper.get_account_report(account)
    if not result:
        logger.error(
            "Account without transactions for agency/account: %s/%s", agencia, conta
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account without transactions",
        )
    return AccountInfoResponse(**result)
