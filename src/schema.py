import typing
from pydantic import BaseModel
from decimal import Decimal


class BaseBillingModel(BaseModel):
    user_id: typing.Optional[int] = None
    handshake_id: typing.Optional[str] = None


class CreateWalletInput(BaseBillingModel):
    amount: Decimal


class GetWalletInput(BaseBillingModel):
    wallet_id: typing.Optional[int] = None


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
    transaction_id: typing.Optional[int] = None


class TransactionOutput(BaseBillingModel):
    transaction_id: typing.Optional[int] = None
    status: typing.Optional[str] = None
    source_wallet_id: typing.Optional[int] = None
    destination_wallet_id: typing.Optional[int] = None
    info: typing.Optional[dict] = None
