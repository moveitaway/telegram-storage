#!/usr/bin/env sh

export PYTHONPATH="${PYTHONPATH}:/app"

alembic upgrade head
