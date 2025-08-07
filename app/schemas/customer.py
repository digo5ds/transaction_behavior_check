from typing import Annotated, List

from pydantic import BaseModel, Field

from app.models.transaction import Transaction


class PutCustomerRequest(BaseModel):
    """
    Schema for updating customer information.

    Attributes:
        agencia (int): Branch number. Must be zero or positive.
        conta (int): Account number. Must be zero or positive.
        nome (str): Customer's full name. Cannot be empty.
        idade (int): Customer's age. Must be zero or greater.
    """

    agencia: Annotated[int, Field(ge=0, description="Branch number, zero or positive")]
    conta: Annotated[int, Field(ge=0, description="Account number, zero or positive")]
    nome: Annotated[
        str, Field(min_length=1, description="Customer's full name (cannot be empty)")
    ]
    idade: Annotated[
        int, Field(ge=0, description="Customer's age, must be zero or greater")
    ]


class GetCustomerResponse(BaseModel):
    """
    Represents the response model for a customer.

    Attributes:
        nome (str): The name of the customer.
        idade (int): The age of the customer.
        last_transactions (List[Transaction]): A list of the customer's most recent transactions.
        balance (float): The current balance of the customer.
    """

    nome: str
    idade: int
    last_transactions: List[Transaction]
    balance: float
