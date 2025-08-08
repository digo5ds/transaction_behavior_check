""""Customer routes""" ""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.postgres_database import get_db
from app.helpers.customer_helper import CustomerHelper
from app.models.account import Account
from app.models.customer import Customer
from app.schemas.customer import PutCustomerRequest

router = APIRouter(prefix="/api/customers")


@router.put("/{agencia}/{conta}", status_code=status.HTTP_201_CREATED)
def put_customer(
    agencia: int,
    conta: int,
    data: PutCustomerRequest,
    db: Session = Depends(get_db),
):
    if agencia != data.agencia or conta != data.conta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Agency and account numbers do not match. Update is not allowed",
        )

    customer_helper = CustomerHelper(db)
    customer = Customer(name=data.nome, age=data.idade)
    account = Account(agency=data.agencia, account=data.conta)
    try:
        customer_helper.save_customer_profile(customer=customer, account=account)
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return {"message": "Created"}
