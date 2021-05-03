import logging
from decimal import Decimal

from sqlalchemy.orm import Session

from db.models import Wallet, Transaction
from db.constants import WalletStatuses, TransactionStatuses, Currency
from db.constants import TransactionStatuses

logger = logging.getLogger('rblb.' + __name__)


class WalletStore:

    @staticmethod
    def get_wallet(db_session: Session, wallet_id: int):
        w = db_session.query(Wallet).filter_by(wallet_id=wallet_id).first()
        if not w:
            return Exception('Wallet does not found')
        return w.as_dict()

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
            raise Exception(f'Wallet by handshake_id={handshake_id} not found')

        logger.debug(
            'Found wallet by handshake_id "{}": id={}'.format(handshake_id, wallet.wallet_id if wallet else None)
        )
        return wallet.as_dict()

    @staticmethod
    def get_wallet_by_id(db_session: Session, wallet_id: int):
        wallet = db_session.query(Wallet).filter(Wallet.wallet_id == wallet_id).first()
        if not wallet:
            raise Exception(f'Wallet by id={wallet_id} not found')

        logger.debug(
            'Found wallet by id={}'.format(wallet.wallet_id if wallet else None)
        )
        return wallet.as_dict()







def create_transaction(
        db_session: Session,
        handshake_id: str,
        source_wallet_id: int,
        dest_wallet_id: int,
        summ: Decimal
):
    wallets = db_session.query(Wallet).filter(Wallet.wallet_id.in_([source_wallet_id, dest_wallet_id])).all()
    if not wallets:
        return Exception('Unknown wallets')

    w_dict = {w.wallet_id: w for w in wallets}
    source_wallet, dest_wallet = w_dict[source_wallet_id], w_dict[dest_wallet_id]

    new_amount = Decimal(source_wallet.amount) - summ
    if new_amount < 0:
        trans = Transaction(
            handshake_id=handshake_id,
            status=TransactionStatuses.FAILED,
            source_wallet_id=source_wallet_id,
            destination_wallet_id=dest_wallet_id,
            trans_sum=summ,
            info={'msg': f'wallet {source_wallet_id} does not have enough money'}
        )
        db_session.add(trans)
        return trans.as_dict()

    source_wallet.amount = new_amount
    dest_wallet.amount += summ

    trans = Transaction(
        handshake_id=handshake_id,
        status=TransactionStatuses.PROCESSED,
        source_wallet_id=source_wallet_id,
        destination_wallet_id=dest_wallet_id,
        trans_sum=summ,
        info={'msg': f'transaction was successful'}
    )
    db_session.add(trans)
    return trans.as_dict()
