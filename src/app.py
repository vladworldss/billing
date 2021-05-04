from fastapi import FastAPI

from db.session import async_database
from domain.wallet_service import wallet
from domain.transaction_service import transaction

app = FastAPI(title="Billing")


@app.on_event("startup")
async def startup():
    await async_database.connect()


@app.on_event("shutdown")
async def shutdown():
    await async_database.disconnect()


app.include_router(wallet, prefix='/api/v1/wallet', tags=['wallet'])
app.include_router(transaction, prefix='/api/v1/transaction', tags=['transaction'])
