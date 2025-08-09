from decimal import Decimal
from typing import Annotated, List

from pydantic import BaseModel, Field


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

    id_da_transacao: Annotated[str, Field(..., description="Transaction ID")]
    data_e_hora_da_transacao: Annotated[
        int, Field(..., description="Transaction timestamp as UNIX epoch")
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


class TransactionSummary(BaseModel):
    agencia: int
    conta: int
    type: str  # 'debit' ou 'credit'
    valor: float
    nome: str
    idade: int
    suspect: bool
