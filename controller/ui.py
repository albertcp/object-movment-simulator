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
BUTTON_DISABLED = (40, 40, 45)
FONT_SIZE = 16
POPUP_WIDTH = 320
POPUP_HEIGHT = 180


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
        self._add_btn = Button(btn_x, btn_y, "Add object")
        self._edit_speed_btn = Button(btn_x, btn_y + 50, "Edit Speed")
        self._play_btn = Button(btn_x, btn_y + 100, "Play")
        self._reset_btn = Button(btn_x, btn_y + 150, "Reset")
        self._buttons = [self._add_btn, self._edit_speed_btn, self._play_btn, self._reset_btn]
        self._placing = False
        self._pending_waypoints: list[Position] = []
        self._sim_running = False
        self._sim_paused = False
        self._sim_complete = False
        self._selected_object: Object | None = None
        self._objects: list[Object] = []
        self._editing_speed = False
        self._speed_input_text: str = ""

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
            if btn is self._edit_speed_btn:
                # Edit Speed button is active/clickable only when an object is
                # selected, not in placing mode, and simulation is not running
                active = (
                    self._selected_object is not None
                    and not self._placing
                    and not self._sim_running
                )
                btn.draw(surface, self._font, active=active)
            else:
                active = btn is self._add_btn and self._placing
                btn.draw(surface, self._font, active=active)

        # Simulation status (below all buttons)
        status_y = 215
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

        # All objects data (below buttons and state)
        if self._objects and not self._placing:
            info_y = 245
            section = self._font.render("Objects:", True, (180, 220, 180))
            surface.blit(section, (15, info_y))
            info_y += 20

            for obj in self._objects:
                lines = [
                    f"{obj.id}",
                    f"  S:{obj.speed}  {obj.state.value}",
                    f"  ({int(obj.current_position.x)},{int(obj.current_position.y)})"
                    f"  W:{len(obj.path.waypoints)}",
                ]
                for i, line in enumerate(lines):
                    color = (220, 220, 220) if i == 0 else (170, 170, 170)
                    label = self._font.render(line, True, color)
                    surface.blit(label, (15, info_y))
                    info_y += 17
                info_y += 3

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

        # Speed editing popup
        if self._editing_speed:
            popup_x = (surface.get_width() - POPUP_WIDTH) // 2
            popup_y = (surface.get_height() - POPUP_HEIGHT) // 2
            self._draw_speed_popup(surface, popup_x, popup_y)

    def _draw_speed_popup(self, surface: pygame.Surface, x: int, y: int) -> None:
        """Draw the speed editing popup overlay."""
        # Semi-transparent overlay behind popup
        overlay = pygame.Surface((POPUP_WIDTH, POPUP_HEIGHT), pygame.SRCALPHA)
        overlay.fill((50, 50, 55, 240))
        surface.blit(overlay, (x, y))
        pygame.draw.rect(surface, (120, 120, 120), (x, y, POPUP_WIDTH, POPUP_HEIGHT), 2)

        title = self._font.render("Edit Speed (m/s):", True, (220, 220, 220))
        surface.blit(title, (x + 15, y + 20))

        # Input field background
        input_rect = pygame.Rect(x + 15, y + 50, POPUP_WIDTH - 30, 35)
        pygame.draw.rect(surface, (30, 30, 30), input_rect)
        pygame.draw.rect(surface, (180, 200, 220), input_rect, 1)

        # Input text with blinking cursor
        cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
        display_text = self._speed_input_text + cursor
        input_render = self._font.render(display_text, True, (220, 220, 220))
        surface.blit(input_render, (x + 20, y + 57))

        # Unit label
        unit = self._font.render("m/s", True, (160, 160, 160))
        surface.blit(unit, (x + POPUP_WIDTH - 45, y + 57))

        # Instructions
        info = self._font.render("Enter to confirm, Esc to cancel", True, (140, 140, 140))
        surface.blit(info, (x + 15, y + 100))

        # Preview of new speed
        try:
            preview_val = float(self._speed_input_text) if self._speed_input_text else 0
            preview_str = f"Speed: {preview_val:.1f} m/s"
        except ValueError:
            preview_str = "Invalid speed"
        preview = self._font.render(preview_str, True, (180, 200, 180))
        surface.blit(preview, (x + 15, y + 130))

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
                self._pending_waypoints.clear()
                self._placing = False
                return ("add_object", obj)
            self._placing = not self._placing
            if not self._placing:
                self._pending_waypoints.clear()
            return None

        if self._play_btn.clicked(mouse_pos):
            return "play"

        if self._edit_speed_btn.clicked(mouse_pos):
            if self._selected_object and not self._placing and not self._sim_running:
                self._editing_speed = True
                self._speed_input_text = str(self._selected_object.speed)
                return "edit_speed"
            return None

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

    def set_objects(self, objects: list[Object]) -> None:
        self._objects = list(objects)

    def clear_path(self) -> None:
        self._pending_waypoints.clear()

    @property
    def editing_speed(self) -> bool:
        return self._editing_speed

    @property
    def speed_input_text(self) -> str:
        return self._speed_input_text

    def add_speed_input_char(self, char: str) -> None:
        """Append a character to the speed input if valid."""
        if not self._editing_speed:
            return
        # Only allow digits and at most one decimal point
        if char.isdigit():
            self._speed_input_text += char
        elif char == "." and "." not in self._speed_input_text:
            self._speed_input_text += char

    def speed_input_backspace(self) -> None:
        """Remove the last character from the speed input."""
        if not self._editing_speed:
            return
        self._speed_input_text = self._speed_input_text[:-1]

    def confirm_speed_edit(self) -> float | None:
        """Return the validated speed float, or None if invalid."""
        if not self._editing_speed:
            return None
        text = self._speed_input_text.strip()
        if not text or text == ".":
            return None
        try:
            speed = float(text)
            if speed <= 0:
                return None
            self._editing_speed = False
            self._speed_input_text = ""
            return speed
        except ValueError:
            return None

    def cancel_speed_edit(self) -> None:
        """Cancel speed editing and reset input state."""
        self._editing_speed = False
        self._speed_input_text = ""

    def finish_drawing(self) -> AddObjectResult | None:
        if self._pending_waypoints:
            obj = self._finish_object()
            self._pending_waypoints.clear()
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
