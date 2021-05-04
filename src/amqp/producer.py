import json
from decimal import Decimal

import structlog

import pika

from amqp.config import amqp_config

logger = structlog.get_logger(__name__)


def basic_pub(msg=None, host='localhost'):
    credentials = pika.PlainCredentials('billing', 'billing')
    parameters = pika.ConnectionParameters(host, 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='basic')
    msg = msg or 'ON GET RESPONSE'
    channel.basic_publish(
        exchange='',
        routing_key='basic',
        body=msg,
        properties=pika.BasicProperties(delivery_mode=2)
    )

    connection.close()


class Producer:
    def publish(self, routing_key, msg):
        conn = self.create_connection()
        channel = conn.channel()
        channel.exchange_declare(
            exchange=amqp_config.exchange.name, exchange_type=amqp_config.exchange.type
        )
        channel.basic_publish(
            exchange=amqp_config.exchange.name, routing_key=routing_key, body=msg,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        logger.info(f"MSG was published exchange={amqp_config.exchange.name}  routing_key={routing_key}")
        # conn.close()

    @staticmethod
    def create_connection():
        credentials = pika.PlainCredentials(amqp_config.user, amqp_config.pwd)
        parameters = pika.ConnectionParameters(
            amqp_config.host, amqp_config.port, amqp_config.vhost, credentials
        )
        return pika.BlockingConnection(parameters)


class WalletProducer(Producer):

    def publish_create(self, handshake_id, amount):
        routing_key = 'wallet.create'
        msg = json.dumps({
            'action': 'create',
            'handshake_id': handshake_id,
            'amount': float(amount)
        })
        self.publish(routing_key, msg)
        logger.info(f"WalletProducer publish_create msg={msg}")

    def publish_get(self, handshake_id, wallet_id):
        routing_key = 'wallet.get'
        msg = json.dumps({
            'action': 'get',
            'handshake_id': handshake_id,
            'wallet_id': wallet_id
        })
        self.publish(routing_key, msg)
        logger.info(f"WalletProducer publish_get msg={msg}")


class TransactionProducer(Producer):

    def publish_create(
            self,
            handshake_id: str,
            source_wallet_id: int,
            dest_wallet_id: int,
            trans_sum: Decimal
    ):
        routing_key = 'transaction.create'
        msg = json.dumps({
            'action': 'create',
            'handshake_id': handshake_id,
            'source_wallet_id': source_wallet_id,
            'dest_wallet_id': dest_wallet_id,
            'trans_sum': float(trans_sum)
        })
        self.publish(routing_key, msg)
        logger.info(f"TransactionProducer publish_create msg={msg}")

    def publish_get(self, handshake_id: str, transaction_id: int):
        routing_key = 'transaction.get'
        msg = json.dumps({
            'action': 'get',
            'handshake_id': handshake_id,
            'transaction_id': transaction_id
        })
        self.publish(routing_key, msg)
        logger.info(f"TransactionProducer publish_get msg={msg}")