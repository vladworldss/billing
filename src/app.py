from decimal import Decimal


from fastapi import FastAPI, BackgroundTasks
from fastapi import HTTPException

from schema import CreateWalletInput, GetWalletInput, WalletOutput, TransactionInput, TransactionOutput

from producer import basic_pub
from db.session import open_db_session
from db.logic import WalletStore, TransactionStore
from helpers.hash import create_handshake_id

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