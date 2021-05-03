import logging
import pickle

from redis import Redis, ResponseError, ConnectionError as RedisConnectionError

import settings as app_settings


billing_redis = Redis().from_url(app_settings.REDIS_CONNECTION)
logger = logging.getLogger('billing.' + __name__)


def redis_decorator(func):
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ResponseError, RedisConnectionError) as e:
            logger.error(e)

    return wrapped


@redis_decorator
def get_from_cache(key):
    value = billing_redis.get(key)
    if value is not None:
        value = pickle.loads(value)
    return value


@redis_decorator
def get_keys(pattern):
    return billing_redis.keys(pattern)


@redis_decorator
def set_to_cache(key, value, expired=app_settings.REDIS_CACHE_DEFAULT_TIMEOUT):
    if value is not None:
        value = pickle.dumps(value)
    billing_redis.set(key, value, ex=expired)


@redis_decorator
def delete(*keys):
    billing_redis.delete(*keys)


@redis_decorator
def flushdb():
    billing_redis.flushdb()


