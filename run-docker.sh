#!/usr/bin/env bash
# Launch the simulator in Docker, adapting the X11 setup to the host OS.
#
#   Linux  -> allows the local X server for the container.
#   macOS  -> requires XQuartz running (TCP display via host.docker.internal).
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v docker >/dev/null 2>&1; then
  echo "error: docker is not installed or not on PATH" >&2
  exit 1
fi

if docker compose version >/dev/null 2>&1; then
  COMPOSE=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE=(docker-compose)
else
  echo "error: Docker Compose is not available" >&2
  exit 1
fi

case "$(uname -s)" in
  Linux)
    if command -v xhost >/dev/null 2>&1; then
      xhost +local:docker >/dev/null
    else
      echo "warning: xhost not found; make sure the X server accepts the container" >&2
    fi
    ;;
  Darwin)
    if ! pgrep -f "XQuartz.app/Contents/MacOS/X11.bin" >/dev/null 2>&1; then
      echo "error: XQuartz is not running" >&2
      echo "install it with 'brew install --cask xquartz' and keep it open" >&2
      exit 1
    fi
    ;;
  *)
    echo "error: unsupported OS '$(uname -s)'; run 'docker compose up --build' manually" >&2
    exit 1
    ;;
esac

exec "${COMPOSE[@]}" up --build "$@"
