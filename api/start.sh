#!/usr/bin/env sh
set -e

echo "Starting SpamShield API..."
echo "PORT=${PORT:-5000}"
echo "Python: $(python -V 2>&1)"
echo "Working dir: $(pwd)"
ls -la /app || true
ls -la /app/models || true

# Start gunicorn directly - let Railway handle healthchecks
exec gunicorn \
  --workers ${GUNICORN_WORKERS:-2} \
  --bind 0.0.0.0:${PORT:-5000} \
  --timeout ${GUNICORN_TIMEOUT:-120} \
  --log-level info \
  --access-logfile - \
  --error-logfile - \
  app:app
