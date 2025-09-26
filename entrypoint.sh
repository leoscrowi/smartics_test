#!/bin/bash

echo "STARTING entrypoint.sh"
python src/infrastructure/manage.py migrate
python src/infrastructure/manage.py collectstatic --noinput
echo "ENDING entrypoint.sh"
exec python src/infrastructure/manage.py runserver 0.0.0.0:8000