import os

from invoke import task


@task
def run_wallet_consuming(ctx):
    print(f'Start run_wallet_consuming from {os.getpid()}')
    ctx.run("nohup python wallet_consuming.py > /dev/null 2>&1&")


@task
def run_trans_consuming(ctx):
    print(f'Start run_trans_consuming from {os.getpid()}')
    ctx.run("nohup python trans_consuming.py > /dev/null 2>&1&")
