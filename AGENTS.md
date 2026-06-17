# Object Movement Simulator

Greenfield Python project. Completed. Planning in `InitialTask.md` and `todo.md`.

## Architecture

Three-layer package structure:

- **`controller/`** — Pygame UI (window, canvas, controls, event loop)
- **`logic/`** — simulation engine, path interpolation, object state tracking, arrival detection
- **`adapter/`** — output layer: JSON, file, console, network adapters

## Setup

- Python 3.11+ (runs on 3.9+)
- Virtual environment: `.venv/`
- `from __future__ import annotations` required in all source files for 3.9 compatibility
- pyproject.toml with ruff, black, mypy (strict), and pytest config

## Testing

- 95 tests, 91% coverage (≥90% target met)
- Pygame mocked in controller tests via `conftest.py` autouse fixture + `@patch` decorators
- `__init__.py` in all packages (required by test discovery)

## Commands

```bash
.venv/bin/pip install -r requirements.txt
./run.sh                                     # run application (bash wrapper)
.venv/bin/python Simulator.py                # run application
.venv/bin/python -m controller.app           # alternative entry point
docker build -t object-movement-sim . && docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix object-movement-sim  # Docker
.venv/bin/pytest --cov=.                      # test with coverage
.venv/bin/ruff check . && .venv/bin/black --check . && .venv/bin/mypy --strict .
```

## Key files

| File | Purpose |
|------|---------|
| `InitialTask.md` | Original requirements specification |
| `todo.md` | Task breakdown (all phases completed) |
| `README.md` | Project overview and usage |
| `controller/app.py` | Main app entry point and event loop |
| `controller/renderer.py` | Canvas rendering (grid, axes, objects) |
| `controller/ui.py` | UI panels, buttons, waypoint drawing |
| `logic/engine.py` | Simulation engine core |
| `logic/interpolator.py` | Path interpolation math |
| `logic/models.py` | Data models (Position, Path, Object) |
| `adapter/` | Output adapters (JSON, file, console, network) |
| `Dockerfile` | Container image for running the app |

## Rules

1. Always update `todo.md` when implementing a task
2. Always update `README.md` when a task is completed
2.1. Maintain README.md file up to date with last changes
3. Always update `requirements.txt` if a new dependency is added
4. Update todo sidebar on every change
