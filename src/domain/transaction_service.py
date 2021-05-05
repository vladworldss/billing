import structlog

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.encoders import jsonable_encoder

from amqp.producer import TransactionProducer
from cache import cache
from db.transaction_repostory import repo as trans_repo
from helpers.hash import create_handshake_id
from schema import GetTransactionInput, CreateTransactionInput, TransactionOutput

logger = structlog.get_logger(__name__)

transaction = APIRouter()
trans_producer = TransactionProducer()


@transaction.post(
    "/",
    response_description="User's transaction",
    description="Refill wallet transaction ",
    response_model=TransactionOutput,
)
async def create_transaction(trans_input: CreateTransactionInput, bckgr_tasks: BackgroundTasks):
    handshake_id = create_handshake_id(trans_input.user_id)
    bckgr_tasks.add_task(
        trans_producer.publish_create,
        handshake_id,
        trans_input.source_wallet_id,
        trans_input.dest_wallet_id,
        trans_input.trans_sum
    )
    return TransactionOutput(handshake_id=handshake_id)


@transaction.get(
    "/",
    response_description="User's transaction",
    description="Get wallet transaction ",
    response_model=TransactionOutput,
)
async def get_transaction_by(trans_input: GetTransactionInput, background_tasks: BackgroundTasks):
    if trans_input.handshake_id:
        trans = cache.get_from_cache(trans_input.handshake_id)
        if trans:
            return TransactionOutput(**trans)

    background_tasks.add_task(
        trans_producer.publish_get,
        trans_input.handshake_id,
        trans_input.transaction_id
    )

    return TransactionOutput(handshake_id=trans_input.handshake_id)


@transaction.get(
    "/async",
    response_description="User's transaction",
    description="Get wallet transaction ",
    response_model=TransactionOutput,
)
async def async_get_transaction_by_id(trans_input: GetTransactionInput):
    trans = cache.get_from_cache(trans_input.handshake_id)
    if trans:
        return TransactionOutput(**trans)
    trans = jsonable_encoder(await trans_repo.a_get_transaction(trans_input.transaction_id))
    if not trans:
        raise HTTPException(status_code=404, detail="Transaction not found")
    cache.set_to_cache(trans_input.handshake_id, trans)
    return TransactionOutput(**trans)
