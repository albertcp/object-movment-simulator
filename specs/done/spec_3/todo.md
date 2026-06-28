# Spec 3 — GUI Layout and Object Data Display

## Tasks

- [x] Generate BDD spec file (`bdd_spec_3.md`) describing GUI layout behavior
- [x] Reorder buttons: Add Object → Edit Speed → Play → Reset in `controller/ui.py`
- [x] Move simulation status text below all buttons
- [x] Replace selected-object info with all-objects list display (Name, speed, state, position, waypoints)
- [x] Add `set_objects()` method to `UIPanel` for syncing engine objects to UI
- [x] Wire `set_objects()` call in `App._draw()` so objects display updates each frame
- [x] Update existing tests for new button click positions (Play, Reset, Edit Speed)
- [x] Add unit tests for button order and `set_objects` in `tests/test_ui.py`
- [x] Add integration tests for objects list in `tests/test_app.py`
- [x] Run tests, linters, and type checker
- [x] Move spec folder from `specs/todo/` → `specs/done/`
- [x] Update `README.md` and project root `todo.md`
