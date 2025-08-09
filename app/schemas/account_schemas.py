from typing import List

from pydantic import BaseModel, Field

from app.schemas.transaction import TransactionSummary


class AccountInfoResponse(BaseModel):
    nome: str
    idade: int
    balance: float
    last_transactions: List[TransactionSummary]
