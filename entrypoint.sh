#!/bin/bash

python infrastructure/manage.py migrate
python infrastructure/manage.py collectstatic --noinput
exec "$@"