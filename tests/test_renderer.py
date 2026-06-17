from __future__ import annotations

from unittest.mock import MagicMock, patch

import pygame
import pytest

from controller.renderer import CanvasRenderer


@pytest.fixture
def surface() -> MagicMock:
    mock = MagicMock(spec=pygame.Surface)
    mock.get_width.return_value = 800
    mock.get_height.return_value = 600
    return mock


@pytest.fixture
def renderer(surface: MagicMock) -> CanvasRenderer:
    with patch("pygame.font.SysFont", return_value=MagicMock()):
        return CanvasRenderer(surface)


class TestCanvasRenderer:
    def test_initialization(self, renderer: CanvasRenderer) -> None:
        assert renderer._width == 800
        assert renderer._height == 600

    def test_draw_background(self, renderer: CanvasRenderer, surface: MagicMock) -> None:
        renderer.draw_background()
        surface.fill.assert_called_once()

    @patch("pygame.draw.line")
    def test_draw_grid(self, mock_line: MagicMock, renderer: CanvasRenderer) -> None:
        renderer.draw_grid()
        assert mock_line.call_count > 0

    @patch("pygame.draw.line")
    @patch("pygame.draw.polygon")
    def test_draw_axes(
        self, mock_poly: MagicMock, mock_line: MagicMock, renderer: CanvasRenderer
    ) -> None:
        renderer.draw_axes()

    @patch("pygame.draw.line")
    @patch("pygame.draw.polygon")
    def test_draw(
        self,
        mock_line: MagicMock,
        mock_poly: MagicMock,
        renderer: CanvasRenderer,
        surface: MagicMock,
    ) -> None:
        renderer.draw()
        assert surface.fill.call_count == 1
        assert mock_line.call_count > 0
