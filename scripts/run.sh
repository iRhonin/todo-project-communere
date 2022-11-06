#!/bin/bash
alembic upgrade head
gunicorn -b 0.0.0.0:4321 --workers 2 wsgi:app -t 60
