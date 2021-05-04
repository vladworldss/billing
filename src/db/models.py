from datetime import datetime

from sqlalchemy import (
    Column, BigInteger, CHAR, Numeric, TIMESTAMP, Enum, func, ForeignKey, CheckConstraint,
    Table, MetaData
)
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.ext.declarative import declarative_base

from db.constants import WalletStatuses, TransactionStatuses, Currency

Base = declarative_base()


class Wallet(Base):
    __tablename__ = 'wallet'

    wallet_id = Column(BigInteger, primary_key=True, autoincrement=True)
    status = Column(
        Enum(*tuple((x.value for x in WalletStatuses)), name='wallet_status'),  # Dirty hack
        nullable=False
    )
    amount = Column(Numeric(10, 2), default=0, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, server_default=func.now(), nullable=False)
    currency = Column(
        Enum(*tuple((x.value for x in Currency)), name='wallet_currency'),
        nullable=False
    )
    handshake_id = Column(CHAR(64))

    CheckConstraint('amount > 0', 'positive_amount')

    def as_dict(self):
        return {
            'wallet_id': self.wallet_id,
            'handshake_id': self.handshake_id,
            'status': self.status,
            'amount': self.amount,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'currency': self.currency
        }

metadata = MetaData()


wallet_table = Table(
    'wallet',
    metadata,
    Column('wallet_id', BigInteger, primary_key=True, autoincrement=True),
    Column('status',
        Enum(*tuple((x.value for x in WalletStatuses)), name='wallet_status'),  # Dirty hack
        nullable=False
    ),
    Column('amount', Numeric(10, 2), default=0, nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.utcnow, server_default=func.now(), nullable=False),
    Column('updated_at', TIMESTAMP, default=datetime.utcnow, server_default=func.now(), nullable=False),
    Column('currency',
        Enum(*tuple((x.value for x in Currency)), name='wallet_currency'),
        nullable=False
    ),
    Column('handshake_id', CHAR(64)),
    CheckConstraint('amount > 0', 'positive_amount')
)


class Transaction(Base):
    __tablename__ = 'transaction'

    transaction_id = Column(BigInteger, primary_key=True, autoincrement=True)
    handshake_id = Column(CHAR(64))
    status = Column(
        Enum(*tuple((x.value for x in TransactionStatuses)), name='transaction_status'),
        nullable=False
    )
    source_wallet_id = Column(BigInteger, ForeignKey(Wallet.wallet_id, ondelete='CASCADE'), nullable=False)
    destination_wallet_id = Column(BigInteger, ForeignKey(Wallet.wallet_id, ondelete='CASCADE'), nullable=False)
    trans_sum = Column(Numeric(10, 2), default=0, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, server_default=func.now(), nullable=False)
    info = Column(JSONB, nullable=False, default='{}')

    CheckConstraint('source_wallet_id != destination_wallet_id', 'non_self_transaction')

    def as_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'handshake_id': self.handshake_id,
            'status': self.status,
            'source_wallet_id': self.source_wallet_id,
            'destination_wallet_id': self.destination_wallet_id,
            'trans_sum': self.trans_sum,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'info': self.info
        }


transaction_table = Table(
    'transaction',
    metadata,
    Column('transaction_id', BigInteger, primary_key=True, autoincrement=True),
    Column('handshake_id', CHAR(64)),
    Column(
        'status',
        Enum(*tuple((x.value for x in TransactionStatuses)), name='transaction_status'),
        nullable=False
    ),
    Column('source_wallet_id', BigInteger, ForeignKey(Wallet.wallet_id, ondelete='CASCADE'), nullable=False),
    Column('destination_wallet_id', BigInteger, ForeignKey(Wallet.wallet_id, ondelete='CASCADE'), nullable=False),
    Column('trans_sum', Numeric(10, 2), default=0, nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.utcnow, server_default=func.now(), nullable=False),
    Column('updated_at', TIMESTAMP, default=datetime.utcnow, server_default=func.now(), nullable=False),
    Column('info', JSONB, nullable=False, default='{}'),
    CheckConstraint('source_wallet_id != destination_wallet_id', 'non_self_transaction')
)
