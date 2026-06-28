from __future__ import annotations

import sys

import pygame

from adapter.base import OutputAdapter
from controller.renderer import CanvasRenderer
from controller.ui import UIPanel
from logic.engine import SimulationEngine
from logic.messages import PositionMessage
from logic.models import Object, Position

OBJECT_COLORS = [
    (0, 200, 255),
    (255, 180, 0),
    (100, 220, 100),
    (255, 100, 100),
    (200, 130, 255),
    (255, 200, 100),
    (100, 255, 200),
    (255, 150, 200),
]
OBJECT_RADIUS = 10
OBJECT_BORDER = 2


class App:
    WIDTH = 1024
    HEIGHT = 768
    FPS = 60

    def __init__(
        self, engine: SimulationEngine, adapters: list[OutputAdapter] | None = None
    ) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Object Movement Simulator")
        self._clock = pygame.time.Clock()
        self._running = True
        self._engine = engine
        self._adapters = adapters or []
        self._renderer = CanvasRenderer(self._screen)
        self._ui = UIPanel()
        self._was_running = False
        self._sim_complete = False
        self._selected_index: int | None = None

    def run(self) -> None:
        while self._running:
            dt = self._clock.tick(self.FPS) / 1000.0

            mouse_pos = pygame.mouse.get_pos()
            self._ui.update(mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                self._handle_event(event)

            self._update(dt)
            self._draw()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def _handle_event(self, event: pygame.event.Event) -> None:
        # Speed editing mode: intercept keyboard events
        if self._ui.editing_speed and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                speed = self._ui.confirm_speed_edit()
                if speed is not None and self._selected_index is not None:
                    state_objects = list(self._engine.state.objects)
                    if 0 <= self._selected_index < len(state_objects):
                        updated_obj = state_objects[self._selected_index].model_copy()
                        updated_obj.speed = speed
                        state_objects[self._selected_index] = updated_obj
                        self._engine = SimulationEngine(state_objects)
            elif event.key == pygame.K_ESCAPE:
                self._ui.cancel_speed_edit()
            elif event.key == pygame.K_BACKSPACE:
                self._ui.speed_input_backspace()
            else:
                # Route printable characters to speed input
                if event.unicode and event.unicode.isprintable():
                    self._ui.add_speed_input_char(event.unicode)
            return  # Consume keyboard events during speed editing

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                state = self._engine.state
                if not state.running:
                    self._sim_complete = False
                    self._engine.start()
                elif state.paused:
                    self._engine.resume()
                else:
                    self._engine.pause()
            elif event.key == pygame.K_r:
                self._engine.reset()
            elif event.key == pygame.K_ESCAPE:
                self._ui.finish_drawing()
            elif event.key == pygame.K_BACKSPACE and self._ui.placing:
                self._ui.remove_last_waypoint()
            elif event.key == pygame.K_c and self._ui.placing:
                self._ui.clear_path()
            elif event.key == pygame.K_DELETE and self._selected_index is not None:
                if self._engine.state.running:
                    return
                objects = list(self._engine.state.objects)
                if 0 <= self._selected_index < len(objects):
                    objects.pop(self._selected_index)
                    self._engine = SimulationEngine(objects)
                    self._selected_index = None

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                result = self._ui.handle_click(event.pos)
                if result == "play":
                    self._sim_complete = False
                    self._engine.start()
                elif result == "reset":
                    self._sim_complete = False
                    self._engine.reset()
                elif isinstance(result, tuple) and result[0] == "add_object":
                    obj: Object = result[1]
                    new_objects = list(self._engine.state.objects) + [obj]
                    self._engine = SimulationEngine(new_objects)
                    self._sim_complete = False
                elif event.pos[0] > 180:
                    if self._ui.placing:
                        x = max(0, event.pos[0])
                        y = max(0, event.pos[1])
                        self._ui.add_waypoint(Position(x=float(x), y=float(y)))
                    else:
                        self._selected_index = self._hit_test_object(event.pos)
            elif event.button == 3 and self._ui.placing:
                add_result = self._ui.finish_drawing()
                if add_result:
                    _, obj = add_result
                    new = list(self._engine.state.objects) + [obj]
                    self._engine = SimulationEngine(new)
                    self._sim_complete = False

    def _update(self, dt: float) -> None:
        objects = self._engine.tick(dt)
        state = self._engine.state
        if state.running:
            for obj in objects:
                msg = PositionMessage(
                    object_id=obj.id,
                    x=obj.current_position.x,
                    y=obj.current_position.y,
                    timestamp=state.elapsed_time,
                )
                for adapter in self._adapters:
                    adapter.send(msg)

    def _hit_test_object(self, pos: tuple[int, int]) -> int | None:
        state = self._engine.state
        for i, obj in enumerate(state.objects):
            dx = pos[0] - int(obj.current_position.x)
            dy = pos[1] - int(obj.current_position.y)
            if dx * dx + dy * dy <= (OBJECT_RADIUS + OBJECT_BORDER + 4) ** 2:
                return i
        return None

    def _draw(self) -> None:
        self._renderer.draw()

        state = self._engine.state
        if not self._sim_complete:
            all_arrived = bool(state.objects) and all(
                o.state.value == "arrived" for o in state.objects
            )
            self._sim_complete = self._was_running and not state.running and all_arrived
        self._was_running = state.running

        for i, obj in enumerate(state.objects):
            self._draw_object_path(obj)
            self._draw_object(obj, i)

        if self._sim_complete:
            self._draw_complete_overlay()

        # Draw pending waypoints while placing
        for wp in self._ui.pending_waypoints:
            pygame.draw.circle(self._screen, (255, 200, 0), (int(wp.x), int(wp.y)), 5)
        if len(self._ui.pending_waypoints) > 1:
            pts = [(int(wp.x), int(wp.y)) for wp in self._ui.pending_waypoints]
            pygame.draw.lines(self._screen, (255, 200, 0), False, pts, 2)

        selected = (
            state.objects[self._selected_index]
            if self._selected_index is not None and self._selected_index < len(state.objects)
            else None
        )
        self._ui.sync_state(state.running, state.paused, complete=self._sim_complete)
        self._ui.set_selected_object(selected)
        self._ui.set_objects(state.objects)
        self._ui.draw(self._screen)

    def _draw_complete_overlay(self) -> None:
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 0))
        font = pygame.font.SysFont("monospace", 40)
        text = font.render("Simulation Complete", True, (100, 220, 100))
        rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 20))
        self._screen.blit(text, rect)
        sub = pygame.font.SysFont("monospace", 18).render(
            "All objects have arrived", True, (180, 180, 180)
        )
        sub_rect = sub.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 20))
        self._screen.blit(sub, sub_rect)

    def _draw_object_path(self, obj: Object) -> None:
        waypoints = obj.path.waypoints
        if len(waypoints) < 2:
            return
        pts = [(int(wp.x), int(wp.y)) for wp in waypoints]
        pygame.draw.lines(self._screen, (80, 80, 120), False, pts, 1)
        for wp in waypoints:
            pygame.draw.circle(self._screen, (100, 100, 140), (int(wp.x), int(wp.y)), 3)

    def _draw_object(self, obj: Object, index: int) -> None:
        color = OBJECT_COLORS[index % len(OBJECT_COLORS)]
        if obj.state.value == "arrived":
            color = tuple(min(c + 80, 255) for c in color)  # type: ignore[assignment]
        x = int(obj.current_position.x)
        y = int(obj.current_position.y)

        # Selection highlight
        if self._selected_index == index:
            radius = OBJECT_RADIUS + OBJECT_BORDER + 3
            pygame.draw.circle(self._screen, (255, 255, 0), (x, y), radius, 2)

        # Outer border
        pygame.draw.circle(self._screen, (255, 255, 255), (x, y), OBJECT_RADIUS + OBJECT_BORDER)
        # Inner fill
        pygame.draw.circle(self._screen, color, (x, y), OBJECT_RADIUS)

        # Label
        label = pygame.font.SysFont("monospace", 12).render(obj.id, True, (200, 200, 200))
        self._screen.blit(label, (x + 14, y - 8))
