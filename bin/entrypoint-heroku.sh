#!/bin/sh

set -e

echo "Migrating database ..."
python3 manage.py migrate --no-input

exec \
    gunicorn subscriber.asgi:application \
        --name=subscriber \
        --user=$APP_USER --group=$APP_USER \
        --bind=0.0.0.0:$PORT \
        --log-level=$LOG_LEVEL \
        --log-file=- \
        --workers=4 \
        --worker-class=uvicorn.workers.UvicornWorker
