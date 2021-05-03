import os
from logging.config import dictConfig

from invoke import task, Collection
from subprocess import run

import settings as app_settings
from db import tasks as db_tasks


@task
def run_consuming(ctx):
    """
    Starts consuming

    Usage:
        inv runserver
    """

    for _ in range(3):
        run("nohup python testz.py > /dev/null 2>&1", shell=True)



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


# dictConfig(app_settings.LOGGING)

ns = Collection()
ns.add_task(init_config)
ns.add_task(run_consuming)
ns.add_collection(Collection.from_module(db_tasks), name='db')
