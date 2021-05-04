from typing import Optional
import structlog

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.encoders import jsonable_encoder

from amqp.producer import WalletProducer
from cache import cache
from db.wallet_repository import repo as wallet_repo
from helpers.hash import create_handshake_id
from schema import CreateWalletInput, GetWalletInput, WalletOutput

logger = structlog.get_logger(__name__)

wallet = APIRouter()
wallet_producer = WalletProducer()


@wallet.post(
    "/",
    response_description="User's wallet",
    description="Create a new wallet by user",
    response_model=WalletOutput,
)
async def create_wallet(wallet_input: CreateWalletInput, bckgr_tasks: BackgroundTasks):
    handshake_id = create_handshake_id(wallet_input.user_id)
    bckgr_tasks.add_task(wallet_producer.publish_create, handshake_id, wallet_input.amount)
    return WalletOutput(handshake_id=handshake_id)


@wallet.get(
    "/",
    response_description="User's wallet",
    description="Get wallet from database",
    response_model=WalletOutput,
)
async def get_wallet_by_id(
        wallet_input: GetWalletInput, background_tasks: BackgroundTasks
):
    if wallet_input.handshake_id:
        wallet = cache.get_from_cache(wallet_input.handshake_id)
        if wallet:
            return WalletOutput(**wallet)
        else:
            background_tasks.add_task(
                wallet_producer.publish_get,
                wallet_input.handshake_id,
                wallet_input.wallet_id
            )
    else:
        handshake_id = create_handshake_id(wallet_input.user_id)
        background_tasks.add_task(
            wallet_producer.publish_get,
            handshake_id,
            wallet_input.wallet_id
        )
        return handshake_id


@wallet.get(
    "/async",
    response_description="User's wallet",
    description="Get wallet from database",
    response_model=WalletOutput,
)
async def async_get_wallet_by_id(wallet_input: GetWalletInput):
    logger.info('______GET ASYNC')
    if wallet_input.handshake_id:
        wallet = cache.get_from_cache(wallet_input.handshake_id)
        if wallet:
            return WalletOutput(**wallet)
        wallet = jsonable_encoder(await wallet_repo.a_get_wallet(wallet_input.wallet_id))
        logger.info(f'______GET WALLET {wallet}')
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
        cache.set_to_cache(wallet_input.handshake_id, wallet)
        return WalletOutput(**wallet)


# @wallet.post(
#     "/async",
#     response_description="User's wallet",
#     description="Create a new wallet by user",
#     response_model=WalletOutput,
# )
# async def async_create_wallet_by_id(wallet_input: CreateWalletInput):
#     logger.info('______GET ASYNC')
#     handshake_id = create_handshake_id(wallet_input.user_id)
#     wallet = jsonable_encoder(
#         await wallet_repo.a_create_wallet(handshake_id=handshake_id, amount=wallet_input.amount)
#     )
#     if not wallet:
#         raise HTTPException(status_code=500, detail="Wallet has not been created")
#     cache.set_to_cache(handshake_id, wallet)
#     return WalletOutput(**wallet)
