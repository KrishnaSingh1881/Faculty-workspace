#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"
API_URL="${API_URL:-}"
FRONTEND_URL="${FRONTEND_URL:-http://127.0.0.1:5173}"

if [[ ! -x "$FRONTEND_DIR/node_modules/.bin/vite" ]]; then
  printf 'Frontend dependencies are missing. Run: cd "%s" && npm ci\n' "$FRONTEND_DIR" >&2
  exit 1
fi

api_healthy() {
  python - "$1" <<'PY'
import json
import sys
import urllib.request

try:
    with urllib.request.urlopen(sys.argv[1].rstrip("/") + "/api/health", timeout=2) as response:
        data = json.load(response)
    raise SystemExit(0 if data.get("status") == "ok" else 1)
except Exception:
    raise SystemExit(1)
PY
}

if [[ -n "$API_URL" ]]; then
  if ! api_healthy "$API_URL"; then
    printf 'The API at %s is not healthy. Check the backend before starting the UI.\n' "$API_URL" >&2
    exit 1
  fi
else
  for candidate in "http://127.0.0.1:8000" "http://127.0.0.1:8767"; do
    if api_healthy "$candidate"; then
      API_URL="$candidate"
      break
    fi
  done
fi

if [[ -z "$API_URL" ]]; then
  if [[ ! -f "$ROOT_DIR/.env" ]]; then
    printf 'No running API was found. Start the backend with Docker Compose after creating .env:\n  cp "%s/.env.example" "%s/.env"\n  # Set POSTGRES_PASSWORD, ADMIN_EMAIL, and ADMIN_PASSWORD in .env\n  docker compose up --build -d\n' "$ROOT_DIR" "$ROOT_DIR" >&2
    exit 1
  fi
  if ! command -v docker >/dev/null 2>&1; then
    printf 'Docker is required to start the backend. Start PostgreSQL and the API, then rerun this script.\n' >&2
    exit 1
  fi
  docker compose up --build -d
  API_URL="http://127.0.0.1:${WORKSPACE_PORT:-8000}"
  printf 'Waiting for the API at %s' "$API_URL"
  for _ in $(seq 1 60); do
    if api_healthy "$API_URL"; then
      printf '\n'
      break
    fi
    printf '.'
    sleep 1
  done
  if ! api_healthy "$API_URL"; then
    printf '\nAPI did not become healthy. Inspect it with: docker compose logs --tail=100 workspace\n' >&2
    exit 1
  fi
fi

if python - "$FRONTEND_URL" <<'PY'
import sys
import urllib.request

try:
    urllib.request.urlopen(sys.argv[1], timeout=2).close()
except Exception:
    raise SystemExit(1)
PY
then
  printf 'Workspace UI is already running at %s (API: %s).\n' "$FRONTEND_URL" "$API_URL"
  exit 0
fi

printf 'Starting workspace UI at %s (API: %s). Press Ctrl+C to stop the UI.\n' "$FRONTEND_URL" "$API_URL"
cd "$FRONTEND_DIR"
VITE_API_PROXY="$API_URL" npm run dev -- --host 127.0.0.1 --port "${FRONTEND_PORT:-5173}" --strictPort
