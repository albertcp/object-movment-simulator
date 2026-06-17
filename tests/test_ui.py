from __future__ import annotations

from unittest.mock import MagicMock, patch

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
    @patch("pygame.font.SysFont")
    def test_initial_state(self, mock_font: MagicMock) -> None:
        panel = UIPanel()
        assert panel.placing is False
        assert panel.pending_waypoints == []

    @patch("pygame.font.SysFont")
    def test_placing_toggle_on_add_click(self, mock_font: MagicMock) -> None:
        panel = UIPanel()
        result = panel.handle_click((15, 20))
        assert result is None
        assert panel.placing is True

    @patch("pygame.font.SysFont")
    def test_placing_toggle_off(self, mock_font: MagicMock) -> None:
        panel = UIPanel()
        panel.handle_click((15, 20))
        panel.handle_click((15, 20))
        assert panel.placing is False

    @patch("pygame.font.SysFont")
    def test_add_waypoint(self, mock_font: MagicMock) -> None:
        panel = UIPanel()
        panel.handle_click((15, 20))  # enter placing mode
        panel.add_waypoint(Position(x=100, y=200))
        assert len(panel.pending_waypoints) == 1
        assert panel.pending_waypoints[0] == Position(x=100, y=200)

    @patch("pygame.font.SysFont")
    def test_remove_last_waypoint(self, mock_font: MagicMock) -> None:
        panel = UIPanel()
        panel.handle_click((15, 20))
        panel.add_waypoint(Position(x=100, y=200))
        panel.add_waypoint(Position(x=300, y=400))
        panel.remove_last_waypoint()
        assert len(panel.pending_waypoints) == 1

    @patch("pygame.font.SysFont")
    def test_clear_path(self, mock_font: MagicMock) -> None:
        panel = UIPanel()
        panel.handle_click((15, 20))
        panel.add_waypoint(Position(x=100, y=200))
        panel.add_waypoint(Position(x=300, y=400))
        panel.clear_path()
        assert panel.pending_waypoints == []

    @patch("pygame.font.SysFont")
    def test_finish_drawing_creates_object(self, mock_font: MagicMock) -> None:
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

    @patch("pygame.font.SysFont")
    def test_finish_drawing_empty_returns_none(self, mock_font: MagicMock) -> None:
        panel = UIPanel()
        panel.handle_click((15, 20))
        result = panel.finish_drawing()
        assert result is None
        assert panel.placing is False

    @patch("pygame.font.SysFont")
    def test_play_button_click(self, mock_font: MagicMock) -> None:
        panel = UIPanel()
        result = panel.handle_click((15, 70))
        assert result == "play"

    @patch("pygame.font.SysFont")
    def test_reset_button_click(self, mock_font: MagicMock) -> None:
        panel = UIPanel()
        result = panel.handle_click((15, 120))
        assert result == "reset"

    @patch("pygame.font.SysFont")
    def test_set_selected_object(self, mock_font: MagicMock) -> None:
        panel = UIPanel()
        obj = Object(
            id="c1",
            path=Path(waypoints=[Position(x=0, y=0)]),
            speed=50.0,
            current_position=Position(x=10, y=10),
        )
        panel.set_selected_object(obj)
        assert panel._selected_object is not None

    @patch("pygame.font.SysFont")
    def test_disable_during_simulation(self, mock_font: MagicMock) -> None:
        panel = UIPanel()
        panel.sync_state(running=True, paused=False)
        result = panel.handle_click((15, 20))  # add contact
        assert result is None
        assert panel.placing is False
