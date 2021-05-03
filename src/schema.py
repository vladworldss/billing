import typing
from pydantic import BaseModel
from pydantic import Field
from decimal import Decimal


class WalletInput(BaseModel):
    user_id: int
    wallet_id: typing.Optional[int] = None
    msg: str = Field(..., title="Msg", description="Text of request", max_length=200)


class WalletOutput(BaseModel):
    user_id: typing.Optional[int] = None
    wallet_id: int = None
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

