#!/bin/sh

set -e

echo "Waiting for Postgres at $POSTGRES_HOST:$POSTGRES_PORT..."
until nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 1
done

python manage.py migrate --noinput

gunicorn myproject.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 60