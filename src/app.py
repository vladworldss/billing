from decimal import Decimal
from random import randint

from fastapi import FastAPI, BackgroundTasks
from fastapi import HTTPException

from schema import WalletInput, WalletOutput, TransactionInput, TransactionOutput

from producer import basic_pub
from db.session import open_db_session
from db.logic import WalletStore

app = FastAPI(title="Billing")


@app.get(
    "/wallet",
    response_description="User's wallet",
    description="Get wallet from database",
    response_model=WalletOutput,
)
async def get_wallet(wallet_input: WalletInput):
    hash_id = str(randint(1000, 10 ** 5))
    with open_db_session(with_commit=True) as session:

        WalletStore.create_wallet(session, hash_id, Decimal(13232.23232))

    with open_db_session(with_commit=True) as session:
        wallet = WalletStore.get_wallet_id(session, hash_id)
        print(wallet)


        # if isinstance(wallet, Exception) or not wallet:
        #     raise HTTPException(404, 'empry res')

    return WalletOutput(status='ok')



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
