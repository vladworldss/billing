from os import path
from pathlib import Path
from enum import Enum, unique

PROJECT_DIR: Path = Path(path.abspath(path.dirname(__file__))).parent


@unique
class WalletStatuses(Enum):
    ACTIVE = 'active'
    CLOSED = 'closed'


@unique
class TransactionStatuses(Enum):
    CREATED = 'created'
    PROCESSED = 'processed'
    FAILED = 'failed'


@unique
class Currency(Enum):
    USD = 'usd'


class Msg(Enum):
    NEW_WALLET_MSG = 'NEW:{SUM}'
    TRANSACTION_MSG = 'TRANS:{DEST}:{SUM}'
