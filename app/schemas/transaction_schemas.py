"""Transaction Schemas"""

import hashlib
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field

from app.core.constants import ChannelEnum


class PutTransactionRequest(BaseModel):
    """
    TransactionCreateRequest defines the schema for creating a new transaction.

    Attributes:
        id_da_transacao (str): Transaction ID.
        data_e_hora_da_transacao (int): Transaction timestamp as UNIX epoch.
        valor_da_transacao (Decimal): Transaction amount,
            must be greater than zero with max 15 digits and 2 decimals.
        canal (int): Channel code (must be greater than or equal to 0).
        agencia_de_origem (int): Origin branch number (must be greater than or equal to 0).
        conta_de_origem (int): Origin account number (must be greater than or equal to 0).
        agencia_de_destino (int): Destination branch number (must be greater than or equal to 0).
        conta_de_destino (int): Destination account number (must be greater than or equal to 0).
    """

    id_da_transacao: Annotated[
        str,
        Field(
            ...,
            description="Transaction ID",
            example=hashlib.sha256(str(datetime.now().second).encode()).hexdigest(),
        ),
    ]
    data_e_hora_da_transacao: Annotated[
        datetime,
        Field(
            ...,
            description="Transaction timestamp as UNIX epoch",
            example=int((datetime.now() - timedelta(hours=3)).timestamp()),
        ),
    ]
    valor_da_transacao: Annotated[
        Decimal,
        Field(
            ...,
            max_digits=15,
            decimal_places=2,
            description=(
                "Transaction amount, can be positive (credit) or negative (debit), "
                "with up to 15 digits and 2 decimal places."
            ),
        ),
    ]
    agencia_de_origem: Annotated[
        int, Field(..., ge=0, description="Origin branch number")
    ]
    conta_de_origem: Annotated[
        int, Field(..., ge=0, description="Origin account number")
    ]
    agencia_de_destino: Annotated[
        int, Field(..., ge=0, description="Destination branch number")
    ]
    conta_de_destino: Annotated[
        int, Field(..., ge=0, description="Destination account number")
    ]
    canal: Annotated[
        Union[int, Literal["ATM", "TELLER", "INTERNET_BANKING", "MOBILE_BANKING"]],
        Field(
            ...,
            description="Transaction channel: either integer code or one of the predefined strings",
        ),
    ]


class TransactionSummary(BaseModel):
    """
    TransactionSummary defines the schema for a transaction summary.
    Attributes:
        agencia (int): Branch number.
        conta (int): Account number.
        type (Literal["credit", "debit"]): Transaction type.
        valor (float): Transaction amount.
        nome (str): Customer name.
        idade (int): Customer age.
        suspect (bool): Whether the customer is a suspect.
    """

    agencia: int
    conta: int
    type: Literal["credit", "debit"]
    valor: float
    nome: str
    idade: int
    suspect: bool
