from __future__ import annotations

import pygame


class CanvasRenderer:
    BG_COLOR = (30, 30, 30)
    GRID_COLOR = (55, 55, 55)
    AXIS_COLOR = (180, 180, 180)
    TICK_COLOR = (140, 140, 140)
    LABEL_COLOR = (160, 160, 160)
    GRID_SPACING = 50
    TICK_SIZE = 6
    FONT_SIZE = 14

    def __init__(self, surface: pygame.Surface) -> None:
        self._surface = surface
        self._width = surface.get_width()
        self._height = surface.get_height()
        self._font = pygame.font.SysFont("monospace", self.FONT_SIZE)

    def draw_background(self) -> None:
        self._surface.fill(self.BG_COLOR)

    def draw_grid(self) -> None:
        for x in range(0, self._width, self.GRID_SPACING):
            pygame.draw.line(self._surface, self.GRID_COLOR, (x, 0), (x, self._height))
        for y in range(0, self._height, self.GRID_SPACING):
            pygame.draw.line(self._surface, self.GRID_COLOR, (0, y), (self._width, y))

    def draw_axes(self) -> None:
        mid_x = self._width // 2
        mid_y = self._height // 2

        # X axis
        pygame.draw.line(self._surface, self.AXIS_COLOR, (0, mid_y), (self._width, mid_y), 2)
        # arrow right
        tip = (self._width - 10, mid_y)
        left = (self._width - 18, mid_y - 6)
        right = (self._width - 18, mid_y + 6)
        pygame.draw.polygon(self._surface, self.AXIS_COLOR, [tip, left, right])
        # X label
        x_label = self._font.render("X", True, self.LABEL_COLOR)
        self._surface.blit(x_label, (self._width - 24, mid_y + 8))

        # Y axis
        pygame.draw.line(self._surface, self.AXIS_COLOR, (mid_x, 0), (mid_x, self._height), 2)
        # arrow up
        pygame.draw.polygon(
            self._surface,
            self.AXIS_COLOR,
            [(mid_x, 10), (mid_x - 6, 18), (mid_x + 6, 18)],
        )
        # Y label
        y_label = self._font.render("Y", True, self.LABEL_COLOR)
        self._surface.blit(y_label, (mid_x + 8, 4))

        # Tick marks on X axis
        for x in range(self.GRID_SPACING, self._width, self.GRID_SPACING):
            top = (x, mid_y - self.TICK_SIZE)
            bottom = (x, mid_y + self.TICK_SIZE)
            pygame.draw.line(self._surface, self.TICK_COLOR, top, bottom)
            if x % 100 == 0:
                label = self._font.render(str(x), True, self.LABEL_COLOR)
                self._surface.blit(label, (x - label.get_width() // 2, mid_y + self.TICK_SIZE + 2))

        # Tick marks on Y axis
        for y in range(self.GRID_SPACING, self._height, self.GRID_SPACING):
            left = (mid_x - self.TICK_SIZE, y)
            right = (mid_x + self.TICK_SIZE, y)
            pygame.draw.line(self._surface, self.TICK_COLOR, left, right)
            if y % 100 == 0:
                label = self._font.render(str(y), True, self.LABEL_COLOR)
                self._surface.blit(label, (mid_x + self.TICK_SIZE + 2, y - label.get_height() // 2))

    def draw(self) -> None:
        self.draw_background()
        self.draw_grid()
        self.draw_axes()
