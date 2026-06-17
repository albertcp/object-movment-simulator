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

```bash
.venv/bin/pytest --cov=.
```

95 tests, 91% coverage. All checks pass:

```bash
.venv/bin/ruff check .
.venv/bin/black --check .
.venv/bin/mypy --strict .
```

## Dependencies

- Python 3.9+
- Pygame 2.6+
- Pydantic 2.x
- pytest / pytest-cov (dev)
- ruff / black / mypy (dev)
