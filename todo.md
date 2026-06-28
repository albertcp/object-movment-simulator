# Object Movement Simulator - Todo List

## Phase 1: Project Setup
- [x] Create project directory structure (`controller/`, `logic/`, `adapter/`, `tests/`)
- [x] Create `requirements.txt` with all dependencies (pygame, pydantic, etc.)
- [x] Initialize Python project (virtual environment, pyproject.toml if needed)

## Phase 2: Core Data Models (logic/)
- [x] Define `Contact` dataclass/model (position, path, speed, state)
- [x] Define `Path` dataclass/model (list of waypoints/coordinates)
- [x] Define `SimulationState` model (contacts list, running state, time)
- [x] Define `Position` dataclass (x, y coordinates)
- [x] Define message/event types for position updates

## Phase 3: Business Logic (logic/)
- [x] Implement `PathInterpolator` — computes position along a path at a given time
- [x] Implement `SimulationEngine` — manages simulation clock, updates all contact positions
- [x] Implement collision/arrival detection (stop when all contacts reach end)
- [x] Implement simulation pause/stop/reset logic

## Phase 4: Adapter Layer (adapter/)
- [x] Implement base `OutputAdapter` abstract class
- [x] Implement `JsonAdapter` — serializes contact positions to JSON messages
- [x] Implement `FileAdapter` — writes JSON messages to a file (optional)
- [x] Implement `NetworkAdapter` — sends JSON messages via WebSocket/UDP (optional)
- [x] Implement `ConsoleAdapter` — prints position updates to console (debug)
- [x] Implement position message format (JSON schema)

## Phase 5: Controller / UI (controller/)
- [x] Set up Pygame window and event loop
- [x] Implement canvas rendering (background, grid, axes)
- [x] Implement "Select Point" button — allows operator to click on canvas
- [x] Implement path drawing — draw lines as operator clicks points on canvas
- [x] Implement visual representation of contacts (colored circles/shapes)
- [x] Implement "Play" button — starts the simulation
- [x] Implement contact movement animation following their defined paths
- [x] Implement stop condition visualization (all contacts reached path end)
- [x] Implement UI controls (add contact, clear path, reset simulation)
- [x] Implement contact selection/management UI

## Phase 6: Integration
- [x] Wire up controller → logic → adapter pipeline
- [x] Connect Pygame events to simulation engine commands
- [x] Connect simulation engine to adapter output on each tick
- [x] Handle edge cases (empty paths, overlapping contacts, invalid points)

## Phase 7: Testing (tests/)
- [x] Write unit tests for `Position` and `Contact` models (6 tests)
- [x] Write unit tests for `PathInterpolator` (13 tests)
- [x] Write unit tests for `SimulationEngine` (15 tests)
- [x] Write unit tests for `JsonAdapter` / `FileAdapter` / `ConsoleAdapter` / `NetworkAdapter` (8 tests)
- [x] Write integration tests for full simulation cycle (5 tests)
- [x] Write tests for UI components (controller layer) — mock pygame (22+18 tests)
- [x] Achieve 90%+ test coverage (91%)

## Phase 8: Final Polish
- [x] Add type annotations to all modules
- [x] Run linter (ruff) and formatter (black) across the project
- [x] Run mypy for static type checking (--strict, 0 errors)
- [x] Run full test suite and verify coverage (95 tests, 91%)
- [x] Create `__init__.py` files for all packages
- [x] Final cleanup and README
- [x] Add `Simulator.py` launcher at project root
- [x] Add `run.sh` bash launcher script at project root
- [x] Add `Dockerfile` and `.dockerignore` for containerized execution
- [x] Rename `Contact` → `Object`, `ContactState` → `ObjectState` across all source and test files
- [x] Spec 1 — "Add object" button can be pressed multiple times to add multiple objects (6 new tests, 101 total)
- [x] Spec 2 — Edit object speed via a speed editing button and popup (32 new tests, 133 total)
- [x] Spec 3 — GUI layout: button order, status below buttons, all-objects data display (6 new tests, 139 total)
