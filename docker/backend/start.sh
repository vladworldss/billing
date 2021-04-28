#!/bin/bash

service ssh start

mkdir -p logs

#invoke init_config --db-connection="$DB_CONNECTION"  --redis-connection "$REDIS_CONNECTION" --amqp-userinfo "$RABBITMQ_DEFAULT_USER:$RABBITMQ_DEFAULT_PASS" --silent

uvicorn --host 0.0.0.0 --port 8000 app:app --reload
