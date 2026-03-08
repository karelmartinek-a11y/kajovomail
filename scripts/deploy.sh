#!/usr/bin/env bash
set -euo pipefail

WORKDIR=/opt/kajovomail/app
cd "$WORKDIR"

echo "Pulling latest code"
git pull

echo "Updating backend"
cd backend
alembic upgrade head

COMPOSE_FILE=../infra/docker-compose.prod.yml
if [ -f "$COMPOSE_FILE" ]; then
  docker compose -f "$COMPOSE_FILE" up -d --build backend worker
else
  echo "Missing $COMPOSE_FILE"
  exit 1
fi
