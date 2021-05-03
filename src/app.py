from decimal import Decimal


from fastapi import FastAPI, BackgroundTasks
from fastapi import HTTPException

from schema import (
    CreateWalletInput, GetWalletInput, WalletOutput, TransactionInput,
    TransactionOutput, RedisTestInput, RedisTestOutput
)

from producer import basic_pub
from db.session import open_db_session
from db.logic import WalletStore, TransactionStore
from helpers.hash import create_handshake_id
from cache import cache

app = FastAPI(title="Billing")


@app.post(
    "/wallet",
    response_description="User's wallet",
    description="Create a new wallet by user",
    response_model=WalletOutput,
)
async def create_wallet(wallet_input: CreateWalletInput):
    handshake_id = create_handshake_id(wallet_input.user_id)

    with open_db_session(with_commit=True) as session:
        try:
            wallet = WalletStore.create_wallet(session, handshake_id, wallet_input.amount)
        except Exception as ex:
                raise HTTPException(500, f'Wallet has not been created. Info: {ex}')

        return WalletOutput(**wallet)


@app.get(
    "/wallet",
    response_description="User's wallet",
    description="Get wallet from database",
    response_model=WalletOutput,
)
async def get_wallet(wallet_input: GetWalletInput):

    handshake_id = create_handshake_id(wallet_input.user_id)
    print('HELLO GET WALLET')
    with open_db_session() as session:
        try:
            # so far without authorization (any user can get wallet by id)
            wallet = WalletStore.get_wallet_by_id(session, wallet_input.wallet_id)
        except Exception as ex:
                raise HTTPException(404, f'{ex}')

        return WalletOutput(**wallet)


@app.post(
    "/transaction",
    response_description="User's transaction",
    description="Refill wallet transaction ",
    response_model=TransactionOutput,
)
async def create_transaction(trans_input: TransactionInput):
    handshake_id = create_handshake_id(trans_input.user_id)

    with open_db_session(with_commit=True) as session:
        try:
            trans = TransactionStore.create_transaction(
                session,
                handshake_id,
                trans_input.source_wallet_id,
                trans_input.dest_wallet_id,
                trans_input.trans_sum
            )
        except Exception as ex:
            raise HTTPException(500, f'Transaction has not been created. Info: {ex}')

        return TransactionOutput(**trans)



@app.get(
    "/redis",
    response_description="Redis test",
    description="Redis test",
    response_model=RedisTestOutput,
)
async def get_redis(redis_input: RedisTestInput):
    res = cache.get_from_cache(redis_input.handshake_id)
    if res:
        return RedisTestOutput(msg=res+'___FROM REDIS')
    raise HTTPException(404, 'msg not found')



@app.post(
    "/redis",
    response_description="Redis test",
    description="Redis test",
    response_model=RedisTestOutput,
)
async def set_redis(redis_input: RedisTestInput):
    handshake_id = create_handshake_id(redis_input.user_id)
    cache.set_to_cache(handshake_id, redis_input.msg)
    print(f'________RES TO REDIS: {redis_input.msg}')
    return RedisTestOutput(handshake_id=handshake_id)
