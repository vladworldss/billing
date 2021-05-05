from decimal import Decimal
import structlog

from db.session import open_db_session
from db.wallet_repository import repo as wallet_repo
from db.transaction_repostory import repo as transaction_repo


logger = structlog.get_logger(__name__)

def test_transaction():
    """
    python -m pytest -s tests db/tests/test_models.py
    :return:
    """

    with open_db_session(with_commit=True) as session:
        original_source_amount = 7000
        original_dest_amount = 5000
        origin_delta = 1500
        source_wallet = wallet_repo.create_wallet(session, handshake_id='123', amount=original_source_amount)
        dest_wallet = wallet_repo.create_wallet(session, handshake_id='456', amount=5000)

        transaction_repo.create_transaction(
            session,
            handshake_id="76cc415d55fbd8cdb3cc24dd9aa5f771ee5108804cb6604a8d6e4910b87b82c7",
            source_wallet_id=source_wallet['wallet_id'],
            dest_wallet_id=dest_wallet['wallet_id'],
            trans_sum=1500
        )

        source_wallet = wallet_repo.get_wallet_by_id(session, source_wallet['wallet_id'])
        dest_wallet = wallet_repo.get_wallet_by_id(session, dest_wallet['wallet_id'])

        new_source_amount = source_wallet["amount"]
        new_dest_amount = dest_wallet["amount"]

        assert origin_delta == (original_source_amount - new_source_amount)
        assert origin_delta == (new_dest_amount - original_dest_amount)


