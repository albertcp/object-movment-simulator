# Spec 2 — Tests

> Tests implemented to validate the "Edit Speed" button and speed editing popup behavior.

---

## Test Overview

**Total new tests**: 32  
**Total test count**: 133 (up from 101)  
**Coverage**: 91%

---

## Test Table

### `tests/test_ui.py` — UIPanel speed editing tests

| # | Test Name | What it Validates |
|---|-----------|-------------------|
| 1 | `test_edit_speed_button_exists` | The "Edit Speed" button is added to the panel buttons |
| 2 | `test_edit_speed_button_click_returns_edit_speed` | Clicking Edit Speed with a selected object returns `"edit_speed"` |
| 3 | `test_edit_speed_no_object_returns_none` | Clicking Edit Speed without a selected object returns None |
| 4 | `test_edit_speed_enters_editing_mode` | Clicking Edit Speed enters editing mode with the object's current speed pre-filled |
| 5 | `test_edit_speed_during_simulation_returns_none` | Edit Speed is disabled while simulation is running |
| 6 | `test_edit_speed_not_available_while_placing` | Edit Speed is disabled while in placing/drawing mode |
| 7 | `test_speed_input_accepts_digits` | Typing digits updates the speed input text |
| 8 | `test_speed_input_accepts_decimal_point` | A single decimal point is accepted |
| 9 | `test_speed_input_rejects_second_decimal` | A second decimal point is rejected |
| 10 | `test_speed_input_rejects_non_numeric` | Non-numeric characters (letters, symbols, spaces) are rejected |
| 11 | `test_speed_input_backspace` | Backspace removes the last character |
| 12 | `test_speed_input_backspace_empty_string` | Backspace on empty string does nothing |
| 13 | `test_speed_input_does_nothing_when_not_editing` | Input methods are no-ops when not in editing mode |
| 14 | `test_confirm_speed_edit_returns_float` | Confirm returns the speed as a float and exits editing mode |
| 15 | `test_confirm_speed_edit_integer_string` | Integer string "75" is parsed as 75.0 |
| 16 | `test_confirm_speed_edit_empty_returns_none` | Empty input returns None |
| 17 | `test_confirm_speed_edit_zero_returns_none` | Speed of 0 is invalid |
| 18 | `test_confirm_speed_edit_negative_returns_none` | Negative speed is invalid |
| 19 | `test_confirm_speed_edit_just_decimal_returns_none` | A lone decimal point is invalid |
| 20 | `test_confirm_speed_edit_not_editing` | Confirm when not editing returns None |
| 21 | `test_cancel_speed_edit` | Cancel clears editing state and input text |
| 22 | `test_edit_speed_loads_custom_speed` | Pre-fills with the selected object's actual speed |

### `tests/test_app.py` — App integration tests

| # | Test Name | What it Validates |
|---|-----------|-------------------|
| 23 | `test_edit_speed_click_enters_editing_mode` | Clicking Edit Speed through App enters editing mode |
| 24 | `test_edit_speed_click_without_selection_does_nothing` | Without selection, Edit Speed click has no effect |
| 25 | `test_edit_speed_keyboard_digit_updates_input` | Typing digits updates the speed input text |
| 26 | `test_edit_speed_keyboard_decimal_updates_input` | Decimal point accepted in speed input |
| 27 | `test_edit_speed_keyboard_non_numeric_ignored` | Non-numeric keys are ignored |
| 28 | `test_edit_speed_keyboard_backspace_removes_char` | Backspace removes last character |
| 29 | `test_edit_speed_enter_updates_engine_speed` | Enter confirms the speed and updates engine object |
| 30 | `test_edit_speed_enter_invalid_value_keeps_editing` | Enter with invalid value keeps editing active |
| 31 | `test_edit_speed_escape_cancels` | Escape cancels editing, speed unchanged |
| 32 | `test_edit_speed_updated_speed_used_in_tick` | After editing, the object moves at the new speed |

---

## BDD Scenario Coverage

| BDD Scenario (from `bdd_spec_2.md`) | Covered By |
|--------------------------------------|------------|
| Edit Speed button is visible when an object is selected | `test_edit_speed_button_exists`, `test_edit_speed_button_click_returns_edit_speed` |
| Clicking Edit Speed opens a popup with the current speed | `test_edit_speed_enters_editing_mode`, `test_edit_speed_loads_custom_speed` |
| Operator types a new speed value | `test_speed_input_accepts_digits`, `test_speed_input_accepts_decimal_point` |
| Operator confirms the new speed | `test_confirm_speed_edit_returns_float`, `test_edit_speed_enter_updates_engine_speed` |
| Operator cancels speed editing | `test_cancel_speed_edit`, `test_edit_speed_escape_cancels` |
| Object moves at the new speed when simulation starts | `test_edit_speed_updated_speed_used_in_tick` |
| Non-numeric input is rejected during speed editing | `test_speed_input_rejects_non_numeric`, `test_speed_input_rejects_second_decimal` |
| Speed editing is not available during simulation | `test_edit_speed_during_simulation_returns_none` |
| Speed editing is not available while placing waypoints | `test_edit_speed_not_available_while_placing` |
