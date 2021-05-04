import os

from invoke import task, Collection

import settings as app_settings
from cache import tasks as cache_tasks
from db import tasks as db_tasks
from amqp import tasks as amqp_tasks


@task
def init_config(ctx, db_connection, redis_connection, amqp_userinfo, silent=False):
    settings_local = '''
LOG_LEVEL = 'DEBUG'
DB_CONNECTION = '{db_connection}'
TESTING_DB_CONNECTION = '{db_connection}_test'
REDIS_CONNECTION = '{redis_connection}'
AMQP_CONNECTION = 'amqp://{amqp_userinfo}%@localhost:5672'
'''.format(db_connection=db_connection,
           redis_connection=redis_connection,
           amqp_userinfo=amqp_userinfo)

    settings_local_path = os.path.join(app_settings.PROJECT_ROOT, 'settings_local.py')
    if os.path.isfile(settings_local_path):
        if silent:
            exit(0)

        print('settings_local.py already exists')
        exit(1)

    with open(settings_local_path, 'w') as settings_file:
        settings_file.write(settings_local)


ns = Collection()
ns.add_task(init_config)

ns.add_collection(Collection.from_module(cache_tasks), name='cache')
ns.add_collection(Collection.from_module(db_tasks), name='db')
ns.add_collection(Collection.from_module(amqp_tasks), name='amqp')
