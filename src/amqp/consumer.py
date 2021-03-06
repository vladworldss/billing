import json
import structlog

import pika

from cache import cache
from amqp.config import amqp_config
from schema import WalletOutput, TransactionOutput
from db.constants import TransactionStatuses
from db.session import open_db_session
from db.wallet_repository import repo as wallet_repo
from db.transaction_repostory import repo as transaction_repo

logger = structlog.get_logger(__name__)


class Consumer:

    def __init__(self, queue_name, routing_key, amqp_config=amqp_config):
        self.queue_name = queue_name
        self.routing_key = routing_key
        self.amqp_config = amqp_config
        self.consumer_tag = None
        self.connection = self._create_connection()

    def _create_connection(self):
        credentials = pika.PlainCredentials(self.amqp_config.user, self.amqp_config.pwd)
        parameters = pika.ConnectionParameters(
            self.amqp_config.host, self.amqp_config.port, self.amqp_config.vhost, credentials
        )
        return pika.BlockingConnection(parameters)

    def callback(self, channel, method, properties, body):
        pass

    def setup(self):
        channel = self.connection.channel()
        channel.exchange_declare(
            exchange=self.amqp_config.exchange.name, exchange_type=self.amqp_config.exchange.type
        )
        channel.queue_declare(queue=self.queue_name)
        channel.queue_bind(
            queue=self.queue_name, exchange=self.amqp_config.exchange.name, routing_key=self.routing_key
        )
        self.consumer_tag = channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.callback
        )

        try:
            channel.start_consuming()
        except (Exception, KeyboardInterrupt) as ex:
            logger.error(f'_______Got Exception: {ex}')
            channel.basic_cancel(consumer_tag=self.consumer_tag)
            self.consumer_tag = None
            channel.stop_consuming()


class WalletConsumer(Consumer):

    def __init__(self, *args, **kwargs):
        self.wallet_repo = kwargs.get('wallet_repo', wallet_repo)
        super(WalletConsumer, self).__init__(*args, **kwargs)

    def callback(self, channel, method, properties, body):
        logger.info('____WalletConsumer gets callback')
        try:
            msg = json.loads(body)
        except Exception as ex:
            logger.erro(f'callback except: {ex}')
            return

        action = msg.pop('action')
        if action == 'stop':
            raise Exception('Stop consuming')
        elif action == 'get':
            with open_db_session() as session:
                wallet = self.wallet_repo.get_wallet_by_id(db_session=session, **msg)
                if wallet is None:
                    wallet = WalletOutput(status='not_found').dict()
                cache.set_to_cache(msg['handshake_id'], wallet)
        elif action == 'create':
            with open_db_session(with_commit=True) as session:
                wallet = self.wallet_repo.create_wallet(db_session=session, **msg)
                cache.set_to_cache(msg['handshake_id'], wallet)

        channel.basic_ack(delivery_tag=method.delivery_tag)


class TransactionConsumer(Consumer):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.trans_repo = kw.get('transaction_repo', transaction_repo)
        self.wallet_repo = kw.get('wallet_repo', wallet_repo)

    def callback(self, channel, method, properties, body):
        logger.info('____TransactionConsumer gets callback')
        try:
            msg = json.loads(body)
        except Exception as ex:
            logger.erro(f'callback except: {ex}')
            return

        action = msg.pop('action')
        if action == 'stop':
            raise Exception('Stop consuming')
        elif action == 'get':
            with open_db_session() as session:
                trans = self.trans_repo.get_transaction(db_session=session, **msg)
                if trans is None:
                    trans = TransactionOutput(status='not_found').dict()
                cache.set_to_cache(msg['handshake_id'], trans)

        elif action == 'create':
            with open_db_session(with_commit=True) as session:
                trans = self.trans_repo.create_transaction(db_session=session, **msg)
                if trans['status'] != TransactionStatuses.PROCESSED.value:
                    return

                s_wallet = self.wallet_repo.get_wallet_by_id(session, msg['source_wallet_id'])
                s_handshake = s_wallet['handshake_id']

                d_wallet = self.wallet_repo.get_wallet_by_id(session, msg['dest_wallet_id'])
                d_handshake = d_wallet['handshake_id']
                # clear invalid wallets in cache
                logger.info(f'___DELETE KEYS \n{s_handshake}\n {d_handshake}\n from cache')
                cache.delete(s_handshake)
                cache.delete(d_handshake)
                # set result of transaction
                cache.set_to_cache(msg['handshake_id'], trans)
