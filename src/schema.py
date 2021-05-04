import typing
from pydantic import BaseModel
from pydantic import Field
from decimal import Decimal


class BaseBillingModel(BaseModel):
    user_id: int
    handshake_id: typing.Optional[str] = None


class CreateWalletInput(BaseBillingModel):
    amount: Decimal


class GetWalletInput(BaseBillingModel):
    wallet_id: int


class WalletOutput(BaseBillingModel):
    user_id: typing.Optional[int] = None
    wallet_id: typing.Optional[int] = None
    status: typing.Optional[str] = None
    amount: typing.Optional[Decimal] = None
    created_at: typing.Optional[str] = None
    updated_at: typing.Optional[str] = None
    currency: typing.Optional[str] = None


class CreateTransactionInput(BaseBillingModel):
    """create transaction input model"""
    source_wallet_id: int
    dest_wallet_id: int
    trans_sum: Decimal


class GetTransactionInput(BaseBillingModel):
    """get transaction input model"""
    transaction_id: int


class TransactionOutput(BaseBillingModel):
    transaction_id: int
    status: str
    source_wallet_id: int
    destination_wallet_id: int
    info: dict


class RedisTestInput(BaseBillingModel):
    msg: typing.Optional[str] = None
    handshake_id: typing.Optional[str] = None


class RedisTestOutput(BaseBillingModel):
    msg: typing.Optional[str] = None
    handshake_id: typing.Optional[str] = None