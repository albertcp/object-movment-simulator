from __future__ import annotations

from typing import Iterator
from unittest.mock import MagicMock, patch

import pygame
import pytest


@pytest.fixture(autouse=True)
def _mock_pygame_init() -> Iterator[None]:
    with patch("pygame.init"):
        yield


@pytest.fixture(autouse=True)
def _mock_pygame_font() -> Iterator[None]:
    """Replace pygame.font (MissingModule) with a working mock."""
    mock_font_mod = MagicMock()
    mock_font_mod.SysFont.return_value = MagicMock()
    with patch.object(pygame, "font", mock_font_mod):
        yield


@pytest.fixture(autouse=True)
def _reset_object_counter() -> None:
    """Reset the UIPanel class-level object counter before each test."""
    from controller.ui import UIPanel

    UIPanel._object_counter = 0


@pytest.fixture
def mock_surface() -> MagicMock:
    surface = MagicMock(spec=pygame.Surface)
    surface.get_width.return_value = 800
    surface.get_height.return_value = 600
    return surface
