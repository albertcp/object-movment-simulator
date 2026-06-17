from __future__ import annotations

import pygame

from logic.models import Object, ObjectState, Path, Position

BUTTON_WIDTH = 160
BUTTON_HEIGHT = 40
PANEL_WIDTH = 180
PANEL_BG = (40, 40, 40)
BUTTON_COLOR = (60, 60, 60)
BUTTON_HOVER = (80, 80, 80)
BUTTON_TEXT = (220, 220, 220)
BUTTON_ACTIVE = (50, 100, 150)
FONT_SIZE = 16


class Button:
    def __init__(self, x: int, y: int, text: str) -> None:
        self.rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.text = text
        self._hovered = False

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, active: bool = False) -> None:
        color = BUTTON_ACTIVE if active else (BUTTON_HOVER if self._hovered else BUTTON_COLOR)
        pygame.draw.rect(surface, color, self.rect, border_radius=4)
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 1, border_radius=4)
        label = font.render(self.text, True, BUTTON_TEXT)
        surface.blit(label, (self.rect.x + 10, self.rect.y + 12))

    def update(self, mouse_pos: tuple[int, int]) -> None:
        self._hovered = self.rect.collidepoint(mouse_pos)

    def clicked(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)


class UIPanel:
    _object_counter: int = 0

    def __init__(self) -> None:
        self._font = pygame.font.SysFont("monospace", FONT_SIZE)
        btn_x = 10
        btn_y = 10
        self._add_btn = Button(btn_x, btn_y, "Add Contact")
        self._play_btn = Button(btn_x, btn_y + 50, "Play")
        self._reset_btn = Button(btn_x, btn_y + 100, "Reset")
        self._buttons = [self._add_btn, self._play_btn, self._reset_btn]
        self._placing = False
        self._pending_waypoints: list[Position] = []
        self._sim_running = False
        self._sim_paused = False
        self._sim_complete = False
        self._selected_object: Object | None = None

    @property
    def placing(self) -> bool:
        return self._placing

    @property
    def pending_waypoints(self) -> list[Position]:
        return list(self._pending_waypoints)

    def sync_state(self, running: bool, paused: bool, complete: bool = False) -> None:
        self._sim_complete = complete
        self._sim_running = running
        self._sim_paused = paused
        if running and paused:
            self._play_btn.text = "Resume"
        elif running:
            self._play_btn.text = "Pause"
        else:
            self._play_btn.text = "Play"

    def draw(self, surface: pygame.Surface) -> None:
        panel_rect = pygame.Rect(0, 0, PANEL_WIDTH, surface.get_height())
        pygame.draw.rect(surface, PANEL_BG, panel_rect)
        line_bottom = surface.get_height()
        pygame.draw.line(surface, (60, 60, 60), (PANEL_WIDTH, 0), (PANEL_WIDTH, line_bottom))

        for btn in self._buttons:
            active = btn is self._add_btn and self._placing
            btn.draw(surface, self._font, active=active)

        # Simulation status
        status_y = 160
        if self._sim_complete:
            status_color = (100, 220, 100)
            status_text = "Complete!"
        elif self._sim_running and not self._sim_paused:
            status_color = (100, 220, 100)
            status_text = "Running"
        elif self._sim_paused:
            status_color = (220, 220, 100)
            status_text = "Paused"
        else:
            status_color = (180, 180, 180)
            status_text = "Stopped"
        status = self._font.render(status_text, True, status_color)
        surface.blit(status, (15, status_y))

        # Selected object info
        if self._selected_object and not self._placing:
            info_y = 240
            lines = [
                f"ID: {self._selected_object.id}",
                f"State: {self._selected_object.state.value}",
                f"Speed: {self._selected_object.speed}",
                f"Position: ({int(self._selected_object.current_position.x)}, "
                f"{int(self._selected_object.current_position.y)})",
                f"Waypoints: {len(self._selected_object.path.waypoints)}",
            ]
            for line in lines:
                label = self._font.render(line, True, (180, 180, 180))
                surface.blit(label, (15, info_y))
                info_y += 18

        if self._placing:
            y_offset = 190
            info = self._font.render(f"Points: {len(self._pending_waypoints)}", True, BUTTON_TEXT)
            surface.blit(info, (15, y_offset))
            hint = self._font.render("Click canvas to add", True, (140, 140, 140))
            surface.blit(hint, (15, y_offset + 20))
            hint2 = self._font.render("Right-click to finish", True, (140, 140, 140))
            surface.blit(hint2, (15, y_offset + 40))
            hint3 = self._font.render("Backspace to undo", True, (140, 140, 140))
            surface.blit(hint3, (15, y_offset + 60))

    def update(self, mouse_pos: tuple[int, int]) -> None:
        for btn in self._buttons:
            btn.update(mouse_pos)

    AddObjectResult = tuple[str, Object]

    def handle_click(self, mouse_pos: tuple[int, int]) -> str | AddObjectResult | None:
        if self._add_btn.clicked(mouse_pos):
            if self._sim_running and not self._sim_paused:
                return None
            if self._placing and self._pending_waypoints:
                obj = self._finish_object()
                self._placing = False
                return ("add_object", obj)
            self._placing = not self._placing
            if not self._placing:
                self._pending_waypoints.clear()
            return None

        if self._play_btn.clicked(mouse_pos):
            return "play"

        if self._reset_btn.clicked(mouse_pos):
            self._pending_waypoints.clear()
            self._placing = False
            return "reset"

        return None

    def add_waypoint(self, pos: Position) -> None:
        self._pending_waypoints.append(pos)

    def remove_last_waypoint(self) -> None:
        if self._pending_waypoints:
            self._pending_waypoints.pop()

    def set_selected_object(self, obj: Object | None) -> None:
        self._selected_object = obj

    def clear_path(self) -> None:
        self._pending_waypoints.clear()

    def finish_drawing(self) -> AddObjectResult | None:
        if self._pending_waypoints:
            obj = self._finish_object()
            self._placing = False
            return ("add_object", obj)
        self._placing = False
        return None

    def _finish_object(self) -> Object:
        UIPanel._object_counter += 1
        first = self._pending_waypoints[0]
        return Object(
            id=f"Object-{UIPanel._object_counter}",
            path=Path(waypoints=list(self._pending_waypoints)),
            speed=100.0,
            current_position=first,
            state=ObjectState.WAITING,
        )
