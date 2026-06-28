# Spec 1 — Tests

> Tests implemented to validate the "Add object" button multi-press behavior.

---

## Test Overview

**Total new tests**: 6  
**Total test count**: 101 (up from 95)  
**Coverage**: 91%

---

## Test Table

| # | Test Name | File | Class | What it Validates |
|---|-----------|------|-------|-------------------|
| 1 | `test_add_button_label` | `tests/test_ui.py` | `TestUIPanel` | The "Add Contact" button was renamed to "Add object" |
| 2 | `test_add_click_creates_object_when_placing_with_waypoints` | `tests/test_ui.py` | `TestUIPanel` | Pressing the Add button while in placing mode with waypoints finalizes the object and exits placing mode |
| 3 | `test_add_click_toggles_placing_without_waypoints` | `tests/test_ui.py` | `TestUIPanel` | Pressing Add without waypoints just toggles placing mode off (no object created) |
| 4 | `test_multiple_objects_creation_sequence` | `tests/test_ui.py` | `TestUIPanel` | Creates 2 objects sequentially via the Add button flow, verifying independent IDs and paths |
| 5 | `test_add_button_locked_in_placing_mode` | `tests/test_ui.py` | `TestUIPanel` | While placing, pressing Add finalizes the object (button is "locked"); after creation, pressing Add again enters placing mode fresh |
| 6 | `test_add_object_button_creates_engine_object` | `tests/test_app.py` | `TestApp` | Clicking Add button through the App event handler creates an object in the engine |
| 7 | `test_multiple_add_object_clicks_create_multiple_objects` | `tests/test_app.py` | `TestApp` | Multiple Add clicks through the App create multiple objects in the engine with correct IDs |

---

## BDD Scenario Coverage

| BDD Scenario (from `bdd_spec_1.md`) | Covered By |
|--------------------------------------|------------|
| Start drawing a path for the first object | `test_placing_toggle_on_add_click` (existing) |
| Complete drawing and create the first object | `test_add_click_creates_object_when_placing_with_waypoints` |
| Add a second object after the first one is created | `test_multiple_objects_creation_sequence` |
| Cancel drawing without placing waypoints | `test_add_click_toggles_placing_without_waypoints` |
| Button is locked while drawing path | `test_add_button_locked_in_placing_mode` |
