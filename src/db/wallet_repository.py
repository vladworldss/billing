from decimal import Decimal

import structlog
from sqlalchemy.orm import Session

from db.constants import WalletStatuses, Currency
from db.models import Wallet, wallet_table
from db.session import async_database

logger = structlog.get_logger(__name__)


class Repository:

    @staticmethod
    async def a_get_wallet(wallet_id: int):
        q = wallet_table.select(wallet_table.c.wallet_id == wallet_id)
        return await async_database.fetch_one(query=q)

    @staticmethod
    def create_wallet(db_session: Session, handshake_id: str, amount: Decimal):
        wallet = Wallet(
            amount=amount,
            status=WalletStatuses.ACTIVE.value,
            currency=Currency.USD.value,
            handshake_id=handshake_id
        )
        db_session.add(wallet)
        db_session.commit()
        db_session.refresh(wallet)

        logger.debug(
            'Wallet by handshake_id "{}": id={} has been created'.format(handshake_id, wallet.wallet_id if wallet else None)
        )

        return wallet.as_dict()

    @staticmethod
    def get_wallet_by_handshake(db_session: Session, handshake_id: str):
        wallet = db_session.query(Wallet).filter(Wallet.handshake_id == handshake_id).first()
        if not wallet:
            logger.debug(f'Wallet by handshake_id={handshake_id} not found')
            return None

        logger.debug(
            'Found wallet by handshake_id "{}": id={}'.format(handshake_id, wallet.wallet_id if wallet else None)
        )
        return wallet.as_dict()

    @staticmethod
    def get_wallet_by_id(db_session: Session, wallet_id: int, handshake_id: str = None):
        wallet = db_session.query(Wallet).filter(Wallet.wallet_id == wallet_id).first()
        if not wallet:
            logger.debug(f'Wallet by wallet_id={wallet_id} not found')
            return None

        logger.debug(
            'Found wallet by id={}'.format(wallet.wallet_id)
        )
        return wallet.as_dict()


repo = Repository()
