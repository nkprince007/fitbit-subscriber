#!/bin/sh

set -e

# Use this when testing or using postgresql
# while ! pg_isready -h $DB_HOST -p $DB_PORT 2>/dev/null; do
#     echo "Waiting for database ..."
#     sleep 1
# done

echo "Migrating database ..."
python3 manage.py migrate --no-input

echo "Starting debug server with live reload ..."
exec python3 manage.py runserver 0.0.0.0:8000
