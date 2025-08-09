""" "Customer routes"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.postgres_database import get_db
from app.helpers.account_helper import AccountHelper
from app.helpers.customer_helper import CustomerHelper
from app.models.account_model import Account
from app.models.customer_model import Customer
from app.schemas.account import AccountInfoResponse
from app.schemas.customer import GetCustomerRequest, PutCustomerRequest

router = APIRouter(prefix="/api/customers")


@router.put("/{agencia}/{conta}", status_code=status.HTTP_201_CREATED)
def put_customer(
    agencia: int,
    conta: int,
    data: PutCustomerRequest,
    db: Session = Depends(get_db),
):
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Agency and account numbers do not match. Update is not allowed",
        )

    customer_helper = CustomerHelper(db)
    account_helper = AccountHelper(db)
    customer = Customer(name=data.nome, age=data.idade)
    account = Account(agency=data.agencia, account=data.conta)
    account.rel_customer = customer

    try:
        customer_helper.insert(customer=customer)
        account_helper.save_account(account=account)
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    return {"message": "Created"}


@router.get("/{agencia}/{conta}")
def get_customer_info(agencia: int, conta: int, db: Session = Depends(get_db)):
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
    try:
        account_helper = AccountHelper(db)
        request_model = GetCustomerRequest(agencia=agencia, conta=conta)

        account = account_helper.get_account(
            Account(agency=request_model.agencia, account=request_model.conta)
        )

        if account is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
            )
        return AccountInfoResponse(**account_helper.get_account_report(account))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e
