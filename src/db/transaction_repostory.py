import structlog
from decimal import Decimal

from sqlalchemy.orm import Session
from db.models import Wallet, Transaction, transaction_table
from db.constants import TransactionStatuses
from db.session import async_database

logger = structlog.get_logger(__name__)


class Repository:

    @staticmethod
    def create_transaction(
            db_session: Session,
            handshake_id: str,
            source_wallet_id: int,
            dest_wallet_id: int,
            trans_sum: Decimal
    ):
        if trans_sum < 0:
            msg = 'Value error: trans_sum must be positive'
            logger.debug(msg)
            return Transaction(status=TransactionStatuses.FAILED.value, info={'msg': msg}).as_dict()

        wallets = db_session.query(Wallet).filter(Wallet.wallet_id.in_([source_wallet_id, dest_wallet_id])).all()
        if not wallets:
            logger.debug(f'Unknown wallets source_wallet_id={source_wallet_id} dest_wallet_id={dest_wallet_id}')
            return Transaction(status=TransactionStatuses.FAILED.value, info={'msg': 'Unknown wallets'}).as_dict()

        w_dict = {w.wallet_id: w for w in wallets}
        source_wallet, dest_wallet = w_dict[source_wallet_id], w_dict[dest_wallet_id]
        trans_sum = Decimal(trans_sum)

        trans = Transaction(
            handshake_id=handshake_id,
            source_wallet_id=source_wallet_id,
            destination_wallet_id=dest_wallet_id,
            trans_sum=trans_sum
        )

        new_amount = Decimal(source_wallet.amount) - trans_sum
        if new_amount < 0:
            trans.status = TransactionStatuses.FAILED.value
            trans.info = {'msg': f'wallet {source_wallet_id} does not have enough money'}

        else:
            trans.status = TransactionStatuses.PROCESSED.value
            trans.info = {'msg': f'transaction was successful'}
            source_wallet.amount = new_amount
            dest_wallet.amount += trans_sum

        db_session.add(trans)
        db_session.commit()
        db_session.refresh(trans)

        return trans.as_dict()

    @staticmethod
    def get_transaction(
            db_session: Session,
            transaction_id: int,
            **kw
    ):
        trans = db_session.query(Transaction).filter_by(transaction_id=transaction_id).first()
        if not trans:
            logger.debug(f'Transaction by transaction_id={transaction_id} not found')
            return None

        return trans.as_dict()

    @staticmethod
    async def a_get_transaction(trans_id: int):
        q = transaction_table.select(transaction_table.c.transaction_id == trans_id)
        return await async_database.fetch_one(query=q)


repo = Repository()
