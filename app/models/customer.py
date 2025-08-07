"""Models for representing customers."""

from typing import List

from pydantic import BaseModel, Field

from app.models.transaction import Transaction


class CustomerCreate(BaseModel):
    """
    Pydantic model for creating a new customer.

    Attributes:
        agency (int): The agency number. Must be greater than 0.
        account (int): The account number. Must be greater than 0.
        name (str): The customer's name. Must have at least 1 character.
        age (int): The customer's age. Must be greater than 0.
    """

    agency: int = Field(..., gt=0)
    account: int = Field(..., gt=0)
    name: str = Field(..., min_length=1)
    age: int = Field(..., gt=0)


class CustomerResponse(BaseModel):
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
