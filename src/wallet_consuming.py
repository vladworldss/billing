import os
import structlog

from settings import AMQPS
from amqp.consumer import WalletConsumer

logger = structlog.get_logger(__name__)


if __name__ == '__main__':
    wallet_queue = 'wallet_queue'
    wallet_routing_key = AMQPS['queue']['wallet_queue']

    w_consumer = WalletConsumer(wallet_queue, wallet_routing_key)
    logger.info(f'Start wallet consuming from {os.getpid()}')
    w_consumer.setup()
