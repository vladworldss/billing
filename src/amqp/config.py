from pydantic import BaseModel

from settings import AMQPS


class Exchange(BaseModel):
    name: str = ''
    type: str = 'direct'


class AmqpConfig(BaseModel):
    host: str
    port: int
    vhost: str
    user: str
    pwd: str
    exchange: Exchange


amqp_config = AMQPS.copy()
amqp_config['exchange'] = Exchange(**amqp_config['exchange'])
amqp_config = AmqpConfig(**amqp_config)