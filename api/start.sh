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

# Start gunicorn in background and capture PID
sh -c "gunicorn $GUNICORN_CMD_ARGS api.app:app" &
GUNICORN_PID=$!

# Wait for health endpoint to become available (max 60s)
HEALTH_URL="http://localhost:${PORT:-5000}/api/health"
echo "Waiting for health endpoint: $HEALTH_URL"
TRIES=0
MAX_TRIES=60
until curl -sSf "$HEALTH_URL" >/dev/null 2>&1; do
	TRIES=$((TRIES+1))
	echo "Health check attempt $TRIES/$MAX_TRIES - waiting..."
	if [ "$TRIES" -ge "$MAX_TRIES" ]; then
		echo "Health endpoint did not become healthy in time; exiting with failure"
		kill "$GUNICORN_PID" 2>/dev/null || true
		wait "$GUNICORN_PID" 2>/dev/null || true
		exit 1
	fi
	sleep 1
done
echo "Health endpoint is available"

# Wait for gunicorn process (keeps the container alive and captures exit code)
wait "$GUNICORN_PID"
