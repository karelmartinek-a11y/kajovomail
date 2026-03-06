@echo off
set PYTHONPATH=%CD%
set DATABASE_URL=sqlite+aiosqlite:///./backend/tests/test.db
set REDIS_URL=redis://localhost:6379/1
set SECRET_KEY=test-secret
set OPENAI_API_KEY=
python - <<'PY'
import os
print('DATABASE_URL', os.environ.get('DATABASE_URL'))
print('REDIS_URL', os.environ.get('REDIS_URL'))
PY
python -m pytest backend
