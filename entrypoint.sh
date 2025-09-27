#!/bin/bash
echo "STARTING entrypoint.sh"

python src/infrastructure/manage.py migrate
python src/infrastructure/manage.py collectstatic --noinput

export ADMIN_USERNAME=${DJANGO_SUPERUSER_USERNAME:-admin}
export ADMIN_EMAIL=${DJANGO_SUPERUSER_EMAIL:-admin@example.com}
export ADMIN_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-admin_password}
python src/infrastructure/manage.py createsuperuser --noinput || echo "Superuser already exists"


echo "ENDING entrypoint.sh"
exec python src/infrastructure/manage.py runserver 0.0.0.0:8000