# System Design — Pause Button (Spec 4)

> Based on `spec.md` (Req 4). Reviewed by human.

---

## 1. State Machine — SimulationEngine

| State | Event | Guard | Next State | Action |
|---|---|---|---|---|
| STOPPED | `start()` | — | RUNNING | reset elapsed_time, set all objects → MOVING |
| RUNNING | `pause()` | — | PAUSED | set paused flag |
| PAUSED | `resume()` | — | RUNNING | clear paused flag |
| RUNNING | all arrived | all(o.state == ARRIVED) | STOPPED | clear running flag |
| RUNNING | `stop()` | — | STOPPED | clear running + paused flags |
| PAUSED | `stop()` | — | STOPPED | clear running + paused flags |
| {any} | `reset()` | — | STOPPED | clear running+paused flags, reset elapsed_time, reset objects to initial positions |

**States**: `{STOPPED, RUNNING, PAUSED}`

---

## 2. State Machine — UIPanel Play Button Label

| Engine State | Button Text | Click Action |
|---|---|---|
| STOPPED | "Play" | `engine.start()` |
| RUNNING (not paused) | "Pause" | `engine.pause()` |
| PAUSED | "Resume" | `engine.resume()` |
| COMPLETE | "Play" | `engine.start()` |

The label is driven by `sync_state(running, paused, complete)` called from App each frame.

---

## 3. Interface Contracts

### `SimulationEngine.tick(dt: float) → list[Object]`

```
if not running or paused:
    return copy of internal objects (no movement)

elapsed_time += dt
for each object not ARRIVED:
    compute position via PathInterpolator at elapsed_time
    if at path end → set state = ARRIVED
if all arrived → running = False
return copy of internal objects
```

### `UIPanel.sync_state(running: bool, paused: bool, complete: bool) → None`

```
if running and paused:
    play_btn.text = "Resume"
elif running:
    play_btn.text = "Pause"
else:
    play_btn.text = "Play"
```

### `App.play_button_click()` — unified handler

```
state = engine.state
if not state.running:
    engine.start()
elif state.paused:
    engine.resume()
else:
    engine.pause()
```

This same logic is used by both mouse click (`_ui.handle_click → "play"`) and Space key.

---

## 4. Decision Table — Play Button Behavior

| Engine State | Button Shows | User Clicks | Result | Objects Move? |
|---|---|---|---|---|
| STOPPED | "Play" | Play | Engine starts | Yes |
| RUNNING | "Pause" | Pause | Engine pauses | No (tick no-op) |
| PAUSED | "Resume" | Resume | Engine resumes | Yes (from last position) |
| COMPLETE | "Play" | Play | Engine starts fresh | Yes (from beginning) |

---

## 5. Key Design Decisions

- **Single play/pause button**, not separate Play + Pause. The label changes to indicate the action. This reduces UI clutter.
- **No movement while paused**: `tick()` returns object copy without updating positions when `paused == True`. No special pause timer needed.
- **Reset clears pause**: `reset()` sets `paused = False`. A paused simulation that gets reset goes back to STOPPED cleanly.
- **Space key and button click share the same handler** in `App`. No duplicate logic.
- **`SimulationState` model** carries `paused: bool` so the UI can read it without coupling to engine internals.

---

## 6. Edge Cases

| Scenario | Expected Behavior |
|---|---|
| Pause when already paused | No-op (guard in engine) |
| Resume when not paused | No-op (guard in engine) |
| Pause before any start | No-op (engine not running) |
| Tick while paused | Returns objects unchanged |
| Pause while placing waypoints | Allowed (placing is independent of sim state) |
| Pause while editing speed | Speed popup stays open; pause acts on engine only |
