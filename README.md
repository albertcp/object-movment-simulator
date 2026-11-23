# Object Movement Simulator

A Pygame-based application for simulating object movement along predefined paths. Operators define waypoints, the simulation engine interpolates positions over time, and adapters output position data to JSON, files, or console.

## Architecture

Three-layer design:

- **`controller/`** — Pygame-based UI (window, canvas, controls)
- **`logic/`** — Simulation engine, path interpolation, object state tracking
- **`adapter/`** — Output layer (JSON, file, console, network)

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
./run.sh
.venv/bin/python Simulator.py
.venv/bin/python -m controller.app
```

### Docker

The image bundles Python 3.11, the app dependencies in `/app/.venv`, and the SDL2/X11
libraries pygame needs. The window is rendered through your host X server, so a display
must be available at runtime.

Build the image:

```bash
docker build -t object-movement-sim .
```

**Linux (X11):**

```bash
xhost +local:docker   # allow the container to use the local X server
docker run --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
  object-movement-sim
```

**macOS (XQuartz):** Docker Desktop cannot mount the macOS X11 socket, so XQuartz must
accept TCP connections.

```bash
brew install --cask xquartz
defaults write org.xquartz.X11 nolisten_tcp -bool false
# Log out/in (or restart XQuartz) so the setting applies, then keep XQuartz open.

docker run --rm \
  -e DISPLAY=host.docker.internal:0 \
  object-movement-sim
```

If the window does not appear, check that XQuartz is running and that
`defaults read org.xquartz.X11 nolisten_tcp` returns `0`. If XQuartz refuses the
connection, allow the container host with `xhost +` from an XQuartz terminal.

**Docker Compose (one command):** you do not need to choose a platform. `run-docker.sh`
detects the host OS, prepares the X11 access (Linux) or checks that XQuartz is running
(macOS), and then runs `docker compose up --build`.

```bash
./run-docker.sh
```

> **Podman as the engine (macOS):** if you use Podman instead of Docker Desktop,
> `podman machine start` exposes a Docker-compatible API on `/var/run/docker.sock`, so
> the same `docker`/`docker-compose` commands work unchanged. The `host.docker.internal`
> hostname is also resolved by Podman's VM, so the display setup is identical.

Manual equivalent if you prefer calling Compose yourself — the `DISPLAY` value is
inherited from your shell on Linux and defaults to `host.docker.internal:0` on macOS:

```bash
# Linux
xhost +local:docker && docker compose up --build

# macOS (XQuartz must be running)
docker compose up --build
```

## Tests

144 tests, 91% coverage. See [`tests.md`](tests.md) for the full test suite documentation.

```bash
.venv/bin/pytest --cov=.        # full suite with coverage
.venv/bin/ruff check .          # linting
.venv/bin/black --check .       # formatting
.venv/bin/mypy --strict .       # static types
```

## Future Improvements

- **Podman support** — Use Podman as an alternative container runtime for running the app
- **Persistent simulation state** — Save and load simulation configurations (waypoints, objects, state)
- **Real-time speed controls** — Slider or input to adjust simulation speed during playback
- **Object collision detection** — Detect and flag when objects intersect during movement
- **Waypoint snap-to-grid** — Improve precision when placing waypoints on the canvas
- **Headless mode** — Run the simulation without a display, outputting only to adapters
- **WebSocket adapter** — Replace the placeholder `NetworkAdapter` with a real WebSocket implementation

## Dependencies

- Python 3.9+
- Pygame 2.6+
- Pydantic 2.x
- pytest / pytest-cov (dev)
- ruff / black / mypy (dev)
