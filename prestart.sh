#! /usr/bin/env bash
echo "Running migrations..."
# Let the DB start
sleep 10;
# Run migrations
alembic upgrade head