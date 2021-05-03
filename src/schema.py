import typing
from pydantic import BaseModel
from pydantic import Field
from decimal import Decimal


class BaseInputModel(BaseModel):
    user_id: int


class BaseOutputModel(BaseModel):
    handshake_id: str


class CreateWalletInput(BaseInputModel):
    amount: Decimal


class GetWalletInput(BaseInputModel):
    wallet_id: int


class WalletOutput(BaseOutputModel):
    user_id: typing.Optional[int] = None
    wallet_id: int = None
    status: str
    amount: Decimal
    created_at: str
    updated_at: str
    currency: str


class TransactionInput(BaseInputModel):
    """Transaction input model"""
    source_wallet_id: int
    dest_wallet_id: int
    trans_sum: Decimal


class TransactionOutput(BaseOutputModel):
    transaction_id: int
    status: str
    source_wallet_id: int
    destination_wallet_id: int
    info: dict


class RedisTestInput(BaseInputModel):
    msg: typing.Optional[str] = None
    handshake_id: typing.Optional[str] = None


class RedisTestOutput(BaseOutputModel):
    msg: typing.Optional[str] = None
    handshake_id: typing.Optional[str] = None