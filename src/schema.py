import typing
from pydantic import BaseModel
from pydantic import Field
from decimal import Decimal


class CreateWalletInput(BaseModel):
    user_id: int
    amount: Decimal


class GetWalletInput(BaseModel):
    user_id: int
    wallet_id: int


class WalletOutput(BaseModel):
    user_id: typing.Optional[int] = None
    wallet_id: int = None
    handshake_id: str
    status: str
    amount: Decimal
    created_at: str
    updated_at: str
    currency: str


class TransactionInput(BaseModel):
    """Transaction input model"""



class TransactionOutput(BaseModel):
    handshake_id: str
    transaction_id: int

