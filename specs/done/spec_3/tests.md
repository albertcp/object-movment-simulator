# Spec 3 — Tests

> Tests implemented to validate the GUI layout, button order, and all-objects data display.

---

## Test Overview

**Total new tests**: 6  
**Total test count**: 139 (up from 133)  
**Coverage**: 91%

---

## Test Table

### `tests/test_ui.py` — UIPanel tests

| # | Test Name | What it Validates |
|---|-----------|-------------------|
| 1 | `test_button_order` | Buttons list order is [Add object, Edit Speed, Play, Reset] |
| 2 | `test_set_objects_stores_objects` | `set_objects` stores the list of objects for display |
| 3 | `test_set_objects_empty_list` | `set_objects` accepts an empty list |
| 4 | `test_set_objects_creates_independent_copy` | `set_objects` stores a copy (mutating the original doesn't affect internal list) |

**Updated tests** (positions changed due to reorder):

| Test | Old Position | New Position |
|------|-------------|-------------|
| `test_play_button_click` | (15, 70) | (15, 120) |
| `test_reset_button_click` | (15, 120) | (15, 170) |
| `test_edit_speed_button_click_returns_edit_speed` | (15, 170) | (15, 70) |
| `test_edit_speed_no_object_returns_none` | (15, 170) | (15, 70) |
| `test_edit_speed_enters_editing_mode` | (15, 170) | (15, 70) |
| `test_edit_speed_during_simulation_returns_none` | (15, 170) | (15, 70) |
| `test_edit_speed_not_available_while_placing` | (15, 170) | (15, 70) |
| `test_edit_speed_loads_custom_speed` | (15, 170) | (15, 70) |

### `tests/test_app.py` — App integration tests

| # | Test Name | What it Validates |
|---|-----------|-------------------|
| 5 | `test_objects_list_passed_to_ui` | App passes engine objects to UIPanel via `set_objects` |
| 6 | `test_objects_list_updates_with_engine_changes` | Adding an object updates the UI objects list |

**Updated tests** (Edit Speed button position changed):

| Test | Old Position | New Position |
|------|-------------|-------------|
| `test_edit_speed_click_enters_editing_mode` | (15, 170) | (15, 70) |
| `test_edit_speed_click_without_selection_does_nothing` | (15, 170) | (15, 70) |

---

## BDD Scenario Coverage

| BDD Scenario (from `bdd_spec_3.md`) | Covered By |
|--------------------------------------|------------|
| Buttons are displayed in the correct order | `test_button_order` |
| Edit Speed button is only enabled when an object is selected | `test_edit_speed_button_click_returns_edit_speed`, `test_edit_speed_no_object_returns_none` |
| Simulation status is displayed below all buttons | Visual layout (status_y = 215) |
| All objects data is displayed below buttons and status | `test_set_objects_stores_objects`, `test_objects_list_passed_to_ui` |
| Objects list updates when a new object is added | `test_objects_list_updates_with_engine_changes` |
| Objects list updates when simulation runs | `test_objects_list_passed_to_ui` (position reflects current state) |
