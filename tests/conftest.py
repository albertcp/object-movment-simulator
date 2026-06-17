from __future__ import annotations

from typing import Iterator
from unittest.mock import MagicMock, patch

import pygame
import pytest


@pytest.fixture(autouse=True)
def _mock_pygame_init() -> Iterator[None]:
    with patch("pygame.init"):
        yield


@pytest.fixture
def mock_surface() -> MagicMock:
    surface = MagicMock(spec=pygame.Surface)
    surface.get_width.return_value = 800
    surface.get_height.return_value = 600
    return surface
