from decimal import Decimal


from fastapi import FastAPI, BackgroundTasks
from fastapi import HTTPException

from schema import CreateWalletInput, GetWalletInput, WalletOutput, TransactionInput, TransactionOutput

from producer import basic_pub
from db.session import open_db_session
from db.logic import WalletStore
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


# @app.get(
#     "/get",
#     response_description="Random phrase",
#     description="Get random phrase from database",
#     response_model=PhraseOutput,
# )
# async def get():
#     try:
#         phrase = db.get(db.get_random())
#     except IndexError:
#         raise HTTPException(404, "Phrase list is empty")
#     return phrase
#
# @app.post(
#     "/add",
#     response_description="Added phrase with *id* parameter",
#     response_model=PhraseOutput,
# )
# async def add(phrase: PhraseInput, background_tasks: BackgroundTasks):
#     # validate msg
#     # создать trans_hash_id
#     # если тип NEW - таска на создание кошелька в бд, в redis - trans_hash_id:status__created
#     # если тип TRANS - таска на перевод в бд,в redis - trans_hash_id:status__created
#     # возвращаем trans_hash_id
#     phrase_out = db.add(phrase)
#     background_tasks.add_task(basic_pub, str(phrase_out))
#     return phrase_out
#
#
#
#
# @app.delete("/delete", response_description="Result of deleting")
# async def delete(id: int):
#     try:
#         db.delete(id)
#     except ValueError as e:
#         raise HTTPException(404, str(e))
