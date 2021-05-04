import os
import structlog

from settings import AMQPS
from amqp.consumer import TransactionConsumer

logger = structlog.get_logger(__name__)


if __name__ == '__main__':
    trans_queue = 'transaction_queue'
    trans_routing_key = AMQPS['queue']['transaction_queue']

    trans_consumer = TransactionConsumer(trans_queue, trans_routing_key)
    logger.info(f'Start trans consuming from {os.getpid()}')
    trans_consumer.setup()
