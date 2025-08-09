"""Account Schemas"""

from typing import List

from pydantic import BaseModel

from app.schemas.transaction_schemas import TransactionSummary


class AccountInfoResponse(BaseModel):
    nome: str
    idade: int
    balance: float
    last_transactions: List[TransactionSummary]
