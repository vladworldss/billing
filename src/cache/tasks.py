from invoke import task

from cache.cache import flushdb, delete


@task
def flush_db(ctx):
    flushdb()


@task(help={
    'key': 'Key for delete from cache',
})
def delete_key(ctx, key):
    delete(key)
