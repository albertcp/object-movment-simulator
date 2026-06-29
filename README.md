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

```bash
docker build -t object-movement-sim .
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix object-movement-sim
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
