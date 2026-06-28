from __future__ import annotations

from controller.ui import Button, UIPanel
from logic.models import Object, ObjectState, Path, Position


class TestButton:
    def test_clicked_within_rect(self) -> None:
        btn = Button(x=10, y=10, text="Test")
        assert btn.clicked((20, 20)) is True

    def test_clicked_outside_rect(self) -> None:
        btn = Button(x=10, y=10, text="Test")
        assert btn.clicked((500, 500)) is False

    def test_update_sets_hovered(self) -> None:
        btn = Button(x=10, y=10, text="Test")
        btn.update((20, 20))
        assert btn._hovered is True

    def test_update_clears_hovered(self) -> None:
        btn = Button(x=10, y=10, text="Test")
        btn.update((500, 500))
        assert btn._hovered is False


class TestUIPanel:
    def test_initial_state(self) -> None:
        panel = UIPanel()
        assert panel.placing is False
        assert panel.pending_waypoints == []

    def test_placing_toggle_on_add_click(self) -> None:
        panel = UIPanel()
        result = panel.handle_click((15, 20))
        assert result is None
        assert panel.placing is True

    def test_add_waypoint(self) -> None:
        panel = UIPanel()
        panel.handle_click((15, 20))  # enter placing mode
        panel.add_waypoint(Position(x=100, y=200))
        assert len(panel.pending_waypoints) == 1
        assert panel.pending_waypoints[0] == Position(x=100, y=200)

    def test_remove_last_waypoint(self) -> None:
        panel = UIPanel()
        panel.handle_click((15, 20))
        panel.add_waypoint(Position(x=100, y=200))
        panel.add_waypoint(Position(x=300, y=400))
        panel.remove_last_waypoint()
        assert len(panel.pending_waypoints) == 1

    def test_clear_path(self) -> None:
        panel = UIPanel()
        panel.handle_click((15, 20))
        panel.add_waypoint(Position(x=100, y=200))
        panel.add_waypoint(Position(x=300, y=400))
        panel.clear_path()
        assert panel.pending_waypoints == []

    def test_finish_drawing_creates_object(self) -> None:
        panel = UIPanel()
        panel.handle_click((15, 20))
        panel.add_waypoint(Position(x=10, y=10))
        panel.add_waypoint(Position(x=20, y=20))
        result = panel.finish_drawing()
        assert result is not None
        action, obj = result
        assert action == "add_object"
        assert obj.id == "Object-1"
        assert obj.speed == 100.0
        assert obj.state == ObjectState.WAITING

    def test_finish_drawing_empty_returns_none(self) -> None:
        panel = UIPanel()
        panel.handle_click((15, 20))
        result = panel.finish_drawing()
        assert result is None
        assert panel.placing is False

    def test_play_button_click(self) -> None:
        panel = UIPanel()
        result = panel.handle_click((15, 120))
        assert result == "play"

    def test_reset_button_click(self) -> None:
        panel = UIPanel()
        result = panel.handle_click((15, 170))
        assert result == "reset"

    def test_set_selected_object(self) -> None:
        panel = UIPanel()
        obj = Object(
            id="c1",
            path=Path(waypoints=[Position(x=0, y=0)]),
            speed=50.0,
            current_position=Position(x=10, y=10),
        )
        panel.set_selected_object(obj)
        assert panel._selected_object is not None

    def test_disable_during_simulation(self) -> None:
        panel = UIPanel()
        panel.sync_state(running=True, paused=False)
        result = panel.handle_click((15, 20))  # add object
        assert result is None
        assert panel.placing is False

    def test_add_button_label(self) -> None:
        panel = UIPanel()
        assert panel._add_btn.text == "Add object"

    def test_add_click_creates_object_when_placing_with_waypoints(self) -> None:
        panel = UIPanel()
        panel.handle_click((15, 20))  # enter placing mode
        panel.add_waypoint(Position(x=10, y=10))
        panel.add_waypoint(Position(x=20, y=20))
        panel.add_waypoint(Position(x=30, y=30))
        result = panel.handle_click((15, 20))  # press Add button again
        assert isinstance(result, tuple)
        action, obj = result
        assert action == "add_object"
        assert obj.id == "Object-1"
        assert len(obj.path.waypoints) == 3
        assert obj.state == ObjectState.WAITING
        assert panel.placing is False  # exited placing mode

    def test_add_click_toggles_placing_without_waypoints(self) -> None:
        panel = UIPanel()
        # First click: enter placing mode
        panel.handle_click((15, 20))
        assert panel.placing is True
        # Second click: exit placing mode (no waypoints, no object)
        result = panel.handle_click((15, 20))
        assert result is None
        assert panel.placing is False

    def test_multiple_objects_creation_sequence(self) -> None:
        panel = UIPanel()
        # --- Create first object ---
        panel.handle_click((15, 20))  # enter placing
        panel.add_waypoint(Position(x=0, y=0))
        panel.add_waypoint(Position(x=50, y=50))
        result1 = panel.handle_click((15, 20))  # finish first object
        assert isinstance(result1, tuple)
        action1, obj1 = result1
        assert action1 == "add_object"
        assert obj1.id == "Object-1"
        assert panel.placing is False

        # --- Create second object ---
        panel.handle_click((15, 20))  # enter placing again
        panel.add_waypoint(Position(x=100, y=100))
        panel.add_waypoint(Position(x=200, y=200))
        panel.add_waypoint(Position(x=300, y=300))
        result2 = panel.handle_click((15, 20))  # finish second object
        assert isinstance(result2, tuple)
        action2, obj2 = result2
        assert action2 == "add_object"
        assert obj2.id == "Object-2"
        assert len(obj2.path.waypoints) == 3
        assert panel.placing is False

        # Objects are independent
        assert obj1.id != obj2.id
        assert len(obj1.path.waypoints) == 2
        assert len(obj2.path.waypoints) == 3

    def test_add_button_locked_in_placing_mode(self) -> None:
        """Button is 'locked' while placing: pressing it finalizes the object."""
        panel = UIPanel()
        panel.handle_click((15, 20))  # enter placing
        panel.add_waypoint(Position(x=10, y=10))
        panel.add_waypoint(Position(x=20, y=20))

        # While placing, button click creates object (does not just toggle)
        result = panel.handle_click((15, 20))
        assert isinstance(result, tuple)
        _, obj = result
        assert obj.id == "Object-1"

        # After creation, placing is exited - button is "unlocked"
        assert panel.placing is False

        # Now click again: enters placing mode fresh
        panel.handle_click((15, 20))
        assert panel.placing is True

    # ── Edit Speed button tests ──────────────────────────────────────────

    def test_edit_speed_button_exists(self) -> None:
        """Edit Speed button is present in the panel buttons."""
        panel = UIPanel()
        assert any(btn.text == "Edit Speed" for btn in panel._buttons)

    def test_edit_speed_button_click_returns_edit_speed(self) -> None:
        """Clicking Edit Speed with an object selected returns 'edit_speed'."""
        panel = UIPanel()
        obj = Object(
            id="test",
            path=Path(waypoints=[Position(x=0, y=0), Position(x=10, y=10)]),
            speed=100.0,
            current_position=Position(x=0, y=0),
        )
        panel.set_selected_object(obj)
        result = panel.handle_click((15, 70))
        assert result == "edit_speed"

    def test_edit_speed_no_object_returns_none(self) -> None:
        """Clicking Edit Speed without a selected object returns None."""
        panel = UIPanel()
        result = panel.handle_click((15, 70))
        assert result is None

    def test_edit_speed_enters_editing_mode(self) -> None:
        """handle_click sets editing speed state and loads current speed."""
        panel = UIPanel()
        obj = Object(
            id="test",
            path=Path(waypoints=[Position(x=0, y=0), Position(x=10, y=10)]),
            speed=100.0,
            current_position=Position(x=0, y=0),
        )
        panel.set_selected_object(obj)
        panel.handle_click((15, 70))
        assert panel._editing_speed is True
        assert panel._speed_input_text == "100.0"

    def test_edit_speed_during_simulation_returns_none(self) -> None:
        """Speed editing is not available while simulation is running."""
        panel = UIPanel()
        obj = Object(
            id="test",
            path=Path(waypoints=[Position(x=0, y=0), Position(x=10, y=10)]),
            speed=100.0,
            current_position=Position(x=0, y=0),
        )
        panel.set_selected_object(obj)
        panel.sync_state(running=True, paused=False)
        result = panel.handle_click((15, 70))
        assert result is None
        assert panel._editing_speed is False

    def test_edit_speed_not_available_while_placing(self) -> None:
        """Speed editing is not available while in placing mode."""
        panel = UIPanel()
        obj = Object(
            id="test",
            path=Path(waypoints=[Position(x=0, y=0), Position(x=10, y=10)]),
            speed=100.0,
            current_position=Position(x=0, y=0),
        )
        panel.set_selected_object(obj)
        panel._placing = True
        result = panel.handle_click((15, 70))
        assert result is None
        assert panel._editing_speed is False

    # ── Speed input tests ────────────────────────────────────────────────

    def test_speed_input_accepts_digits(self) -> None:
        """Typing digits updates the speed input text."""
        panel = UIPanel()
        panel._editing_speed = True
        panel._speed_input_text = ""
        panel.add_speed_input_char("5")
        assert panel._speed_input_text == "5"
        panel.add_speed_input_char("0")
        assert panel._speed_input_text == "50"

    def test_speed_input_accepts_decimal_point(self) -> None:
        """A single decimal point is accepted in the speed input."""
        panel = UIPanel()
        panel._editing_speed = True
        panel._speed_input_text = "10"
        panel.add_speed_input_char(".")
        assert panel._speed_input_text == "10."

    def test_speed_input_rejects_second_decimal(self) -> None:
        """Only one decimal point is allowed in the speed input."""
        panel = UIPanel()
        panel._editing_speed = True
        panel._speed_input_text = "10.5"
        panel.add_speed_input_char(".")
        assert panel._speed_input_text == "10.5"

    def test_speed_input_rejects_non_numeric(self) -> None:
        """Non-numeric characters are rejected in speed input."""
        panel = UIPanel()
        panel._editing_speed = True
        panel._speed_input_text = "10"
        panel.add_speed_input_char("a")
        assert panel._speed_input_text == "10"
        panel.add_speed_input_char("-")
        assert panel._speed_input_text == "10"
        panel.add_speed_input_char(" ")
        assert panel._speed_input_text == "10"

    def test_speed_input_backspace(self) -> None:
        """Backspace removes the last character from speed input."""
        panel = UIPanel()
        panel._editing_speed = True
        panel._speed_input_text = "100"
        panel.speed_input_backspace()
        assert panel._speed_input_text == "10"
        panel.speed_input_backspace()
        assert panel._speed_input_text == "1"
        panel.speed_input_backspace()
        assert panel._speed_input_text == ""

    def test_speed_input_backspace_empty_string(self) -> None:
        """Backspace on an empty string leaves it unchanged."""
        panel = UIPanel()
        panel._editing_speed = True
        panel._speed_input_text = ""
        panel.speed_input_backspace()
        assert panel._speed_input_text == ""

    def test_speed_input_does_nothing_when_not_editing(self) -> None:
        """add_speed_input_char does nothing when not in editing mode."""
        panel = UIPanel()
        panel._editing_speed = False
        panel._speed_input_text = ""
        panel.add_speed_input_char("5")
        assert panel._speed_input_text == ""

    def test_confirm_speed_edit_returns_float(self) -> None:
        """Confirming with valid input returns the speed as float."""
        panel = UIPanel()
        panel._editing_speed = True
        panel._speed_input_text = "50.5"
        speed = panel.confirm_speed_edit()
        assert speed == 50.5
        assert panel._editing_speed is False
        assert panel._speed_input_text == ""

    def test_confirm_speed_edit_integer_string(self) -> None:
        """Confirming with an integer string returns a float."""
        panel = UIPanel()
        panel._editing_speed = True
        panel._speed_input_text = "75"
        speed = panel.confirm_speed_edit()
        assert speed == 75.0
        assert panel._editing_speed is False

    def test_confirm_speed_edit_empty_returns_none(self) -> None:
        """Confirming with empty input returns None."""
        panel = UIPanel()
        panel._editing_speed = True
        panel._speed_input_text = ""
        speed = panel.confirm_speed_edit()
        assert speed is None
        assert panel._editing_speed is True  # stays in editing mode

    def test_confirm_speed_edit_zero_returns_none(self) -> None:
        """Speed of zero is invalid and returns None."""
        panel = UIPanel()
        panel._editing_speed = True
        panel._speed_input_text = "0"
        speed = panel.confirm_speed_edit()
        assert speed is None

    def test_confirm_speed_edit_negative_returns_none(self) -> None:
        """Negative speed is invalid and returns None."""
        panel = UIPanel()
        panel._editing_speed = True
        panel._speed_input_text = "-10"
        speed = panel.confirm_speed_edit()
        assert speed is None

    def test_confirm_speed_edit_just_decimal_returns_none(self) -> None:
        """A lone decimal point is invalid and returns None."""
        panel = UIPanel()
        panel._editing_speed = True
        panel._speed_input_text = "."
        speed = panel.confirm_speed_edit()
        assert speed is None

    def test_confirm_speed_edit_not_editing(self) -> None:
        """Calling confirm when not editing returns None."""
        panel = UIPanel()
        panel._editing_speed = False
        speed = panel.confirm_speed_edit()
        assert speed is None

    def test_cancel_speed_edit(self) -> None:
        """Cancelling speed editing clears the input state."""
        panel = UIPanel()
        panel._editing_speed = True
        panel._speed_input_text = "50.0"
        panel.cancel_speed_edit()
        assert panel._editing_speed is False
        assert panel._speed_input_text == ""

    def test_edit_speed_loads_custom_speed(self) -> None:
        """Speed input is pre-filled with the selected object's speed."""
        panel = UIPanel()
        obj = Object(
            id="test",
            path=Path(waypoints=[Position(x=0, y=0), Position(x=10, y=10)]),
            speed=75.0,
            current_position=Position(x=0, y=0),
        )
        panel.set_selected_object(obj)
        panel.handle_click((15, 70))
        assert panel._speed_input_text == "75.0"

    # ── Button order and objects display tests ───────────────────────────

    def test_button_order(self) -> None:
        """Buttons are displayed in the correct order."""
        panel = UIPanel()
        texts = [btn.text for btn in panel._buttons]
        assert texts == ["Add object", "Edit Speed", "Play", "Reset"]

    def test_set_objects_stores_objects(self) -> None:
        """set_objects stores all objects for display."""
        panel = UIPanel()
        objs = [
            Object(
                id="Obj-1",
                path=Path(waypoints=[Position(x=0, y=0)]),
                speed=50.0,
                current_position=Position(x=10, y=10),
            ),
            Object(
                id="Obj-2",
                path=Path(waypoints=[Position(x=0, y=0), Position(x=100, y=0)]),
                speed=100.0,
                current_position=Position(x=0, y=0),
            ),
        ]
        panel.set_objects(objs)
        assert len(panel._objects) == 2
        assert panel._objects[0].id == "Obj-1"
        assert panel._objects[1].id == "Obj-2"

    def test_set_objects_empty_list(self) -> None:
        """set_objects accepts an empty list."""
        panel = UIPanel()
        panel.set_objects([])
        assert panel._objects == []

    def test_set_objects_creates_independent_copy(self) -> None:
        """set_objects stores a copy of the list, not the original reference."""
        panel = UIPanel()
        original = [
            Object(
                id="test",
                path=Path(waypoints=[Position(x=0, y=0)]),
                speed=100.0,
                current_position=Position(x=5, y=5),
            ),
        ]
        panel.set_objects(original)
        original.pop()
        assert len(panel._objects) == 1
