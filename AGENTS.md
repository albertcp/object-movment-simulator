# Object Movement Simulator

Greenfield Python project. Completed. Planning in `InitialTask.md` and `todo.md`.

## Architecture

Three-layer package structure:

- **`controller/`** — Pygame UI (window, canvas, controls, event loop)
- **`logic/`** — simulation engine, path interpolation, object state tracking, arrival detection
- **`adapter/`** — output layer: JSON, file, console, network adapters

## Setup

- **All Python commands MUST run inside the project virtual environment (`.venv/`).**
  Never use the system/global `python`, `pip`, `pytest`, `ruff`, `black`, or `mypy`.
  Use the explicit interpreter path (`.venv/bin/python`) or activate the venv first.
- Virtual environment location: `.venv/` at the repo root.
- Create it only if missing: `python3 -m venv .venv`
- Install dependencies into it: `.venv/bin/pip install -r requirements.txt`
- Python 3.11+ (runs on 3.9+)
- `from __future__ import annotations` required in all source files for 3.9 compatibility
- pyproject.toml with ruff, black, mypy (strict), and pytest config

## Testing

- 95 tests, 91% coverage (≥90% target met)
- Pygame mocked in controller tests via `conftest.py` autouse fixture + `@patch` decorators
- `__init__.py` in all packages (required by test discovery)

## Commands

All commands below assume the repo root and run through `.venv/`.

```bash
python3 -m venv .venv                        # create venv (only if missing)
.venv/bin/pip install -r requirements.txt    # install dependencies
./run.sh                                     # run application (bash wrapper, uses .venv)
.venv/bin/python Simulator.py                # run application
.venv/bin/python -m controller.app           # alternative entry point
docker build -t object-movement-sim . && docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix object-movement-sim  # Docker
docker compose up --build                     # Docker via compose (Linux/macOS)
./run-docker.sh                               # Docker launcher (auto-detects OS + X11)
.venv/bin/pytest --cov=.                     # test with coverage
.venv/bin/ruff check . && .venv/bin/black --check . && .venv/bin/mypy --strict .
```

Do not call `python`, `pytest`, `ruff`, `black`, or `mypy` without the `.venv/bin/`
prefix (or an activated `.venv`). If a tool is missing, install it into `.venv/`,
never globally.

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
| `docker-compose.yml` | One-command build/run (Linux X11 and macOS XQuartz) |
| `run-docker.sh` | Docker launcher that detects the host OS and sets up X11 |

## Rules
The agent must follow the following rules on each task:
1. Always update `todo.md` when implementing a task
2. Always update `README.md` when a task is completed
2.1. Maintain README.md file up to date with last changes
3. Always update `requirements.txt` if a new dependency is added
4. Update todo sidebar on every change
5. When specs are implemented via `specs` folder, you must follow the following rules:
5.1. You must generate a `todo.md` file registeting all tasks that need to be done for the specification requested. 
5.2. This `todo.md` file needs to be generated on the same folder. And these steps are mandatory
5.3. After all `todo.md` tasks are finished, move spec_n folder into `done` folder.
6. Please, request permission to installed any package or installed something
7. Always run Python tooling from `.venv/` (e.g. `.venv/bin/python`, `.venv/bin/pytest`,
   `.venv/bin/ruff`). Never use the global interpreter, and never install packages globally.
   If `.venv/` is missing, create it first with `python3 -m venv .venv`.
