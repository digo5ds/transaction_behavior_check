#!/bin/bash
# entrypoint.sh

until pg_isready -h postgres -p 5432 -U "$POSTGRES_USER"; do
  echo "Aguardando PostgreSQL iniciar..."
  sleep 2
done

echo "PostgreSQL está pronto!"

# Executa as migrações existentes.
alembic upgrade head

python app/migrate.py

# Inicia o comando principal do container.
exec "$@"