import time
from invoke import task

import settings as app_settings


@task
def migration_apply(ctx):
    print('Start migration apply...')
    command = 'yoyo apply --database {db_connection} migrations --no-config-file --batch'
    ctx.run(command.format(db_connection=app_settings.DB_CONNECTION_YOYO))
    print('Success')


@task
def migration_make(ctx, message):
    print('Start migration make...')
    command = 'yoyo new --database {db_connection} migrations -m  "{message}" --no-config-file --batch'
    ctx.run(command.format(db_connection=app_settings.DB_CONNECTION_YOYO, message=message))
    print('Success')


@task
def migration_list(ctx):
    print('Show migrations list...')
    command = 'yoyo list --database {db_connection} migrations --no-config-file'
    ctx.run(command.format(db_connection=app_settings.DB_CONNECTION_YOYO))
    print('Success')


@task
def migration_rollback(ctx, revision):
    print('Rollback migrations...')
    command = 'yoyo rollback --database {db_connection} migrations --no-config-file --batch -r {revision}'
    ctx.run(command.format(db_connection=app_settings.DB_CONNECTION_YOYO, revision=revision))
    print('Success')

