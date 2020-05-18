#!/bin/bash

source ./venv/bin/activate &&
exec env CORS_ALLOWED_ORIGINS="EXTERNAL_DOMAIN" gunicorn --pythonpath ./venv/lib/python3.5/site-packages --worker-class eventlet -w 1 main:app -b 127.0.0.1:8001 --log-level INFO --access-logfile -