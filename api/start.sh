#!/usr/bin/env sh
set -e

# Print environment and model list for debugging
echo "Starting SpamShield API..."
echo "PORT=${PORT:-5000}"
echo "Python: $(python -V 2>&1)"
echo "pip: $(pip -V 2>&1)"
echo "Working dir: $(pwd)"
ls -la /app || true
ls -la /app/models || true

GUNICORN_CMD_ARGS="--workers ${GUNICORN_WORKERS:-2} --bind 0.0.0.0:${PORT:-5000} --timeout ${GUNICORN_TIMEOUT:-30} --log-level info --access-logfile - --error-logfile -"
echo "Launching gunicorn: $GUNICORN_CMD_ARGS api.app:app"

exec sh -c "gunicorn $GUNICORN_CMD_ARGS api.app:app"
