# Tests — Object Movement Simulator

> Full test suite documentation.

---

## Overview

| Metric | Value |
|--------|-------|
| **Total tests** | 139 |
| **Coverage** | 91% (≥90% target met) |
| **Framework** | pytest + pytest-cov |
| **Mocking** | Pygame mocked via `conftest.py` autouse fixtures |

---

## Test files

### `tests/test_models.py` — Data models (9 tests)

Validates `Position`, `Path`, `Object`, `ObjectState`, and `SimulationState` models.

| Test | What it Validates |
|------|-------------------|
| `test_creation` | Position accepts x, y coordinates |
| `test_defaults` | Position default values |
| `test_creation` | Path accepts waypoint list |
| `test_empty_path` | Path can be created with empty waypoints |
| `test_creation` | Object creation with required fields |
| `test_default_state` | Object defaults to WAITING state |
| `test_values` | ObjectState enum values (WAITING, MOVING, ARRIVED) |
| `test_creation` | SimulationState creation |
| `test_running_flag` | SimulationState running flag defaults to False |

### `tests/test_interpolator.py` — Path interpolation (13 tests)

Validates `PathInterpolator` math (segment length, interpolation, multi-segment paths, edge cases).

| Test | What it Validates |
|------|-------------------|
| `test_empty_path_returns_origin` | Empty path returns (0, 0) |
| `test_single_waypoint_stays_put` | Single waypoint stays at that point |
| `test_at_start_of_path` | At time 0, position is first waypoint |
| `test_mid_segment_horizontal` | Correct position mid-way along horizontal segment |
| `test_mid_segment_vertical` | Correct position mid-way along vertical segment |
| `test_diagonal_movement` | Correct position along diagonal |
| `test_beyond_path_returns_last_waypoint` | Beyond path end returns last waypoint |
| `test_multi_segment_path` | Position across multiple segments |
| `test_zero_length_segment` | Handles zero-length segments without division errors |
| `test_segment_length_calculation` | Correct Euclidean distance calculation |
| `test_interpolate_halfway` | Interpolation at t=0.5 returns midpoint |
| `test_interpolate_full` | Interpolation at t=1.0 returns end point |
| `test_interpolate_start` | Interpolation at t=0.0 returns start point |

### `tests/test_engine.py` — Simulation engine (18 tests)

Validates `SimulationEngine` (start, pause, resume, stop, reset, tick, arrival detection).

| Test | What it Validates |
|------|-------------------|
| `test_initial_state_is_stopped` | Engine starts in stopped state |
| `test_empty_objects_list` | Handles empty objects list |
| `test_start_sets_moving_state` | Start sets all objects to MOVING |
| `test_start_idempotent` | Start is idempotent |
| `test_pause_and_resume` | Pause/resume cycle works |
| `test_pause_when_not_running_does_nothing` | Pause is no-op when not running |
| `test_resume_when_not_paused_does_nothing` | Resume is no-op when not paused |
| `test_stop` | Stop halts simulation |
| `test_reset` | Reset restores initial positions |
| `test_tick_moves_object` | Tick advances object position |
| `test_tick_no_movement_when_paused` | No movement while paused |
| `test_tick_no_movement_when_stopped` | No movement while stopped |
| `test_arrival_detection` | Object state changes to ARRIVED at path end |
| `test_all_arrived_stops_simulation` | Simulation stops when all objects arrive |
| `test_mixed_arrival_status` | Mixed arrival status handled correctly |
| `test_tick_returns_objects_copy` | Tick returns a copy of objects list |
| `test_tick_with_no_objects` | Tick with empty objects list |
| `test_start_after_arrival_and_reset` | Reset then restart works |

### `tests/test_adapters.py` — Output adapters (8 tests)

Validates `JsonAdapter`, `FileAdapter`, `ConsoleAdapter`, `NetworkAdapter`.

| Test | What it Validates |
|------|-------------------|
| `test_send_to_stdout` | JsonAdapter writes JSON to stdout |
| `test_send_to_file` | JsonAdapter writes to file |
| `test_append_to_file` | JsonAdapter appends to file |
| `test_writes_json_line` | FileAdapter writes JSON line |
| `test_appends_multiple` | FileAdapter appends multiple lines |
| `test_accepts_pathlib_path` | FileAdapter accepts pathlib.Path |
| `test_prints_formatted` | ConsoleAdapter prints formatted output |
| `test_raises_not_implemented` | NetworkAdapter raises NotImplementedError |

### `tests/test_integration.py` — Integration tests (5 tests)

End-to-end simulation cycle tests.

| Test | What it Validates |
|------|-------------------|
| `test_single_object_full_path` | Single object moves through full path |
| `test_multiple_objects_independent_paths` | Multiple objects move independently |
| `test_start_pause_resume_flow` | Full start → pause → resume → completion flow |
| `test_file_output_end_to_end` | Adapter output through full simulation |
| `test_reset_and_restart` | Reset after completion and restart |

### `tests/test_renderer.py` — Canvas renderer (5 tests)

Validates `CanvasRenderer` with mocked Pygame.

| Test | What it Validates |
|------|-------------------|
| `test_initialization` | Renderer initializes with surface |
| `test_draw_background` | Background fill is called |
| `test_draw_grid` | Grid lines are drawn |
| `test_draw_axes` | Axes and labels are drawn |
| `test_draw` | Full draw sequence runs |

### `tests/test_ui.py` — UI panel (44 tests)

Validates `Button` and `UIPanel` (button clicks, placing mode, waypoints, multi-object, speed editing, button order, objects list).

**Button tests (4):**
| Test | What it Validates |
|------|-------------------|
| `test_clicked_within_rect` | Click inside button rect returns True |
| `test_clicked_outside_rect` | Click outside button rect returns False |
| `test_update_sets_hovered` | Hover state set on mouse over |
| `test_update_clears_hovered` | Hover state cleared on mouse leave |

**UIPanel — core tests (14):**
| Test | What it Validates |
|------|-------------------|
| `test_initial_state` | Panel starts with placing=False, no waypoints |
| `test_placing_toggle_on_add_click` | Add button toggles placing mode |
| `test_add_waypoint` | Waypoints can be added |
| `test_remove_last_waypoint` | Last waypoint can be removed |
| `test_clear_path` | All waypoints cleared |
| `test_finish_drawing_creates_object` | Finish drawing creates Object with correct defaults |
| `test_finish_drawing_empty_returns_none` | Finish drawing with no waypoints returns None |
| `test_play_button_click` | Play button returns "play" |
| `test_reset_button_click` | Reset button returns "reset" |
| `test_set_selected_object` | Selected object can be set |
| `test_disable_during_simulation` | Add button disabled during running sim |
| `test_add_button_label` | Button text is "Add object" |
| `test_add_click_creates_object_when_placing_with_waypoints` | Add click with waypoints creates object |
| `test_add_click_toggles_placing_without_waypoints` | Add click without waypoints toggles placing off |

**UIPanel — multi-object tests (4):**
| Test | What it Validates |
|------|-------------------|
| `test_multiple_objects_creation_sequence` | Creates 2 objects with independent IDs and paths |
| `test_add_button_locked_in_placing_mode` | Button is "locked" while placing: pressing finalizes the object |

**UIPanel — speed editing tests (22):**
| Test | What it Validates |
|------|-------------------|
| `test_edit_speed_button_exists` | "Edit Speed" button added to panel |
| `test_edit_speed_button_click_returns_edit_speed` | Click with selected object returns "edit_speed" |
| `test_edit_speed_no_object_returns_none` | Click without selection returns None |
| `test_edit_speed_enters_editing_mode` | Click enters editing with pre-filled speed |
| `test_edit_speed_during_simulation_returns_none` | Disabled during running sim |
| `test_edit_speed_not_available_while_placing` | Disabled in placing mode |
| `test_speed_input_accepts_digits` | Digits update input |
| `test_speed_input_accepts_decimal_point` | One decimal point accepted |
| `test_speed_input_rejects_second_decimal` | Second decimal rejected |
| `test_speed_input_rejects_non_numeric` | Non-numeric chars rejected |
| `test_speed_input_backspace` | Backspace removes char |
| `test_speed_input_backspace_empty_string` | Backspace on empty no-op |
| `test_speed_input_does_nothing_when_not_editing` | Input no-op when not editing |
| `test_confirm_speed_edit_returns_float` | Valid input returns float |
| `test_confirm_speed_edit_integer_string` | Integer string parsed as float |
| `test_confirm_speed_edit_empty_returns_none` | Empty returns None |
| `test_confirm_speed_edit_zero_returns_none` | Zero invalid |
| `test_confirm_speed_edit_negative_returns_none` | Negative invalid |
| `test_confirm_speed_edit_just_decimal_returns_none` | Lone decimal invalid |
| `test_confirm_speed_edit_not_editing` | Confirm no-op when not editing |
| `test_cancel_speed_edit` | Cancel clears state |
| `test_edit_speed_loads_custom_speed` | Pre-fills with actual object speed |

**UIPanel — button order and objects display (4):**
| Test | What it Validates |
|------|-------------------|
| `test_button_order` | Buttons are [Add object, Edit Speed, Play, Reset] |
| `test_set_objects_stores_objects` | `set_objects` stores all objects |
| `test_set_objects_empty_list` | `set_objects` accepts empty list |
| `test_set_objects_creates_independent_copy` | `set_objects` stores a copy of the list |

### `tests/test_app.py` — App integration (38 tests)

Validates `App` event handling, simulation lifecycle, drawing, adapter output, and speed editing integration.

| Test | What it Validates |
|------|-------------------|
| `test_initialization` | App initializes with UI and engine |
| `test_handle_space_starts_simulation` | Space key starts simulation |
| `test_handle_space_pauses` | Space key pauses running sim |
| `test_handle_space_resumes` | Space key resumes paused sim |
| `test_handle_r_resets` | R key resets simulation |
| `test_handle_delete_removes_object` | Delete key removes selected object |
| `test_handle_delete_blocked_during_simulation` | Delete blocked while running |
| `test_hit_test_object_hits` | Hit detection finds object |
| `test_hit_test_object_misses` | Hit detection misses when far |
| `test_hit_test_object_no_objects` | Hit detection with empty engine |
| `test_mouse_click_selects_object` | Click selects object |
| `test_mouse_click_on_panel_ignored` | Click on panel ignored for selection |
| `test_mouse_click_adds_waypoint` | Click adds waypoint in placing mode |
| `test_add_object_button_creates_engine_object` | Add button creates engine object |
| `test_multiple_add_object_clicks_create_multiple_objects` | Multiple clicks create multiple objects |
| `test_update_sends_messages` | Update sends adapter messages |
| `test_update_no_messages_when_stopped` | No messages when stopped |
| `test_update_updates_objects` | Update advances object positions |
| `test_draw_complete_overlay` | Complete overlay drawn |
| `test_draw_object_path` | Object path drawn |
| `test_draw_object` | Object circle drawn |
| `test_draw_object_arrived` | Arrived object drawn lighter |
| `test_draw_object_selected` | Selected object has highlight |
| `test_edit_speed_click_enters_editing_mode` | Edit Speed click enters editing |
| `test_edit_speed_click_without_selection_does_nothing` | No selection = no editing |
| `test_edit_speed_keyboard_digit_updates_input` | Digit key updates input |
| `test_edit_speed_keyboard_decimal_updates_input` | Decimal key updates input |
| `test_edit_speed_keyboard_non_numeric_ignored` | Non-numeric ignored |
| `test_edit_speed_keyboard_backspace_removes_char` | Backspace removes char |
| `test_edit_speed_enter_updates_engine_speed` | Enter confirms and updates engine |
| `test_edit_speed_enter_invalid_value_keeps_editing` | Invalid value keeps editing |
| `test_edit_speed_escape_cancels` | Escape cancels, speed unchanged |
| `test_edit_speed_updated_speed_used_in_tick` | New speed used in movement |
| `test_objects_list_passed_to_ui` | App passes engine objects to UIPanel |
| `test_objects_list_updates_with_engine_changes` | Adding an object updates the UI list |

---

## Running tests

```bash
.venv/bin/pytest --cov=.                     # full suite with coverage
.venv/bin/pytest -x                           # stop on first failure
.venv/bin/pytest tests/test_ui.py             # single file
.venv/bin/pytest -k "speed"                   # filter by keyword
```

## Quality gates

All quality checks pass:

```bash
.venv/bin/ruff check .
.venv/bin/black --check .
.venv/bin/mypy --strict .
```
