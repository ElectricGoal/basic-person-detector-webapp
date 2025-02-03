#!/bin/sh
set -e

# Wait for PostgreSQL to be ready
until pg_isready -h db -p 5432 -U postgres; do
  echo "Waiting for database connection..."
  sleep 2
done

# Once the DB is ready, run the command to start your backend app
exec "$@"