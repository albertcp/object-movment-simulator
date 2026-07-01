# Spec-Driven Development Workflow

> How to manage requirements from creation to modification and deletion,
> maintaining full traceability and never touching previous specs.

---

## Principles

1. **Never modify a spec in `done/`.** Once a spec is implemented, it stays frozen as a historical record.
2. **Every change is a new spec.** Create a new folder in `specs/todo/` with a new number.
3. **The `traceability.md` is the bridge** between the human and the agent. The human writes what changes; the agent reads it and generates BDD, tests, and code.
4. **The human writes:** `spec.md`, `traceability.md`, `design_spec.md`.
5. **The agent writes:** `bdd_spec.md`, `todo.md`, tests, and code.

---

## Folder structure

```
specs/
  todo/           ← specs being implemented
    spec_5/
      spec.md             ← requirement (human)
      design_spec.md      ← system design, contracts, state machines (human)
      traceability.md     ← map of changes against previous specs (human)
      bdd_spec.md         ← Gherkin scenarios (agent)
      todo.md             ← task breakdown (agent)
  done/           ← specs already implemented
    spec_1/
    spec_2/
    ...
```

After implementation moves from `todo/` to `done/`.

---

## Case 1: Creating a new requirement

### 1.1 Human writes `spec.md`

The raw requirement, short and vague. Business language.

**`specs/todo/spec_5/spec.md`:**

```markdown
# Requirement 5 — Pause time display

When the simulation is paused, a text overlay shows how many
seconds the simulation has been running-paused. It updates in
real time while paused and disappears when resumed.
```

### 1.2 Human writes `traceability.md`

Since this is the first version (no previous spec), it's simple:

**`specs/todo/spec_5/traceability.md`:**

```markdown
## Traceability — Spec 5

This is a new requirement. No previous spec to base on.

Based on: (none)
```

### 1.3 Human writes `design_spec.md`

Detailed system design: state machines, interface contracts, decisions.

**`specs/todo/spec_5/design_spec.md`:**

```markdown
# System Design — Pause Time Display (Spec 5)

## State Machine — UIPanel (additions)
| State  | Event        | Action                    |
|--------|-------------|---------------------------|
| PAUSED | tick()      | increment paused_time     |
| PAUSED | draw()      | render paused_time overlay|

## Interface Contracts

### `UIPanel.sync_state(running, paused, complete, paused_time=0.0)`
```
if paused:
    show paused_time overlay on screen
    increment paused_time each frame
else:
    reset paused_time to 0
    hide overlay
```

### `render_pause_overlay(surface, paused_time)`
```
Render "Paused — 00:05" in center of canvas
Update every frame while paused
```

## Key Decisions
- Pause timer is managed in UIPanel, not engine.
- Format: MM:SS, updates every frame.
- Overlay disappears immediately on resume.
```

### 1.4 The agent receives the three files and produces:

**`bdd_spec.md`** — Gherkin scenarios:

```gherkin
Scenario: Pause timer starts at 0
  Given the simulation is running
  When the user pauses
  Then the timer displays "00:00"

Scenario: Pause timer increments while paused
  Given the simulation is paused
  When 5 seconds pass
  Then the timer displays "00:05"

Scenario: Pause timer resets on resume
  Given the simulation is paused
  And the timer displays "00:10"
  When the user resumes
  Then the timer disappears

Scenario: Pause timer resets on new pause
  Given the simulation is paused
  And the timer displays "00:10"
  When the user resumes
  And the user pauses again
  Then the timer displays "00:00"
```

**`todo.md`** — task breakdown:

```markdown
- [ ] Add `paused_time` field to UIPanel (float, default 0.0)
- [ ] Modify `sync_state()` to accept `paused_time`
- [ ] Add `render_pause_overlay()` method
- [ ] Call `render_pause_overlay()` from `draw()` when paused
- [ ] Increment `paused_time` each frame while paused
- [ ] Reset `paused_time` on resume
- [ ] Add tests for timer display in `test_ui.py`
- [ ] Add tests for timer increment in `test_ui.py`
- [ ] Add integration test in `test_app.py`
- [ ] Run tests, linter, mypy
```

Then the agent enters the TDD loop (unit tests → code → refactor) until all tests BDD + unit pass.

When finished, the folder moves to `specs/done/spec_5/`.

---

## Case 2: Modifying an existing requirement

Example: The pause button now must also show elapsed time while paused.

### 2.1 Human writes `spec.md`

**`specs/todo/spec_6/spec.md`:**

```markdown
# Requirement 6 — Pause with time display (replaces spec_4)

The pause button now shows elapsed paused time on screen.
Same behavior as spec_4, but with a live timer overlay.
```

### 2.2 Human writes `traceability.md`

**`specs/todo/spec_6/traceability.md`:**

```markdown
## Traceability — Spec 6

Based on: spec_4 (specs/done/spec_4/)
Base BDD: spec_4/bdd_spec.md
Base design: spec_4/design_spec.md
Base tests: spec_4/tests.md

### Changes
| Element | Source | Action | Notes |
|---|---|---|---|
| Pause stops movement | bdd_spec_4.md | REUSE | Test already exists |
| Resume maintains position | bdd_spec_4.md | REUSE | Test already exists |
| No movement while paused | bdd_spec_4.md | REUSE | Test already exists |
| Reset clears pause | bdd_spec_4.md | REUSE | Test already exists |
| Time shown during pause | — | CREATE | New scenario + test |
| State machine | design_spec_4.md | REUSE | Unchanged |
| `sync_state()` contract | design_spec_4.md | MODIFY | Add `paused_time` param |
| `tick()` while paused | design_spec_4.md | REUSE | No movement unchanged |
```

> The agent will read:
> - `spec_6/spec.md` — what the new behavior should be
> - `spec_4/bdd_spec.md` — the existing scenarios to reuse
> - `spec_4/design_spec.md` — the existing design to modify
> - `spec_6/traceability.md` — the exact map of what to keep, modify, and create

### 2.3 Human writes `design_spec.md`

Only the deltas (what changes from spec_4):

**`specs/todo/spec_6/design_spec.md`:**

```markdown
# System Design — Pause with Time Display (Spec 6)

> Modifies spec_4/design_spec.md. Everything not listed here is unchanged.

## Modified Contracts

### UIPanel.sync_state(running, paused, complete, paused_time: float = 0.0)
```
  NEW: paused_time param — elapsed seconds while paused
  When paused: render paused_time as overlay on canvas
  When resumed/stopped: hide overlay, reset paused_time to 0
```

## New Elements

### PauseTimer (internal to UIPanel)
```
  Field: _paused_time: float = 0.0
  Incremented each frame in _update() when _sim_paused
  Reset on resume, stop, reset
```

### Overlay rendering
```
  Format: "Paused — MM:SS"
  Position: center of canvas
  Font: monospace, size 30, green text
  Only visible when _sim_paused is True
```
```

### 2.4 The agent produces

**`bdd_spec.md`** with 4 REUSE scenarios + 1 NEW scenario = 5 scenarios total.

Then enters TDD loop. When finished, `spec_6/` moves to `done/`.

---

## Case 3: Removing a requirement

Example: The pause button feature is removed entirely.

### 3.1 Human writes `spec.md`

**`specs/todo/spec_7/spec.md`:**

```markdown
# Requirement 7 — Remove pause button

The pause button is removed. Play button only starts the simulation.
Once started, the simulation runs until all objects arrive.
```

### 3.2 Human writes `traceability.md`

**`specs/todo/spec_7/traceability.md`:**

```markdown
## Traceability — Spec 7

Based on: spec_4 (specs/done/spec_4/)
Base BDD: spec_4/bdd_spec.md
Base design: spec_4/design_spec.md
Base tests: spec_4/tests.md

### Removed (DELETE)
| Element | Source | Action | Notes |
|---|---|---|---|
| Pause stops movement | bdd_spec_4.md | DELETE | Remove test |
| Resume maintains position | bdd_spec_4.md | DELETE | Remove test |
| No movement while paused | bdd_spec_4.md | DELETE | Remove test |
| Reset clears pause | bdd_spec_4.md | DELETE | Remove test |
| State PAUSED in engine | design_spec_4.md | DELETE | Remove state and transitions |
| `engine.pause()` method | design_spec_4.md | DELETE | Remove method |
| `engine.resume()` method | design_spec_4.md | DELETE | Remove method |
| `engine._paused` field | design_spec_4.md | DELETE | Remove field |
| `sync_state()` pause labels | design_spec_4.md | DELETE | Simplify: always "Play" |
| Space key pause handler | design_spec_4.md | DELETE | Space only starts |
| Play button pause handler | design_spec_4.md | DELETE | Play only starts |

### Kept (REUSE)
| Element | Source | Action | Notes |
|---|---|---|---|
| Engine start/stop/reset | design_spec_4.md | REUSE | Unchanged |
| Background | design_spec_4.md | REUSE | Unchanged |
| All spec_1/2/3 features | — | REUSE | Unrelated |
```

### 3.3 Human writes `design_spec.md`

**`specs/todo/spec_7/design_spec.md`:**

```markdown
# System Design — Remove Pause (Spec 7)

> Removes pause from spec_4/design_spec.md.

## State Machine — SimulationEngine (simplified)
| State | Event | Guard | Next State | Action |
|---|---|---|---|---|
| STOPPED | start() | — | RUNNING | reset, set objects → MOVING |
| RUNNING | all arrived | — | STOPPED | clear running |
| {any} | stop() | — | STOPPED | stop |
| {any} | reset() | — | STOPPED | reset everything |

Removed: PAUSED state entirely.

## Interface Contracts

### SimulationEngine
```
  Removed:
  - _paused field
  - pause() method
  - resume() method
  
  Simplified:
  - tick() now checks only `self._running` (no paused check)
  - stop() clears only running flag, no paused flag
  - reset() clears only running flag, no paused flag
```

### UIPanel.sync_state(running, paused: bool = False, complete=False)
```
  simplified: label changes from "Pause"/"Resume"/"Play" to always "Play"
  paused_time removed; paused parameter kept for backward compat but ignored
```

### App.play_button_click() — simplified
```
  Same as before but without pause/resume branch:
  if not state.running → engine.start()
  (pause removed)
```
```

### 3.4 The agent produces

**`bdd_spec.md`** with only the kept scenarios from spec_4 (background, etc.). No pause scenarios.

Tests for pause (from spec_4) are removed. Engine code is cleaned up (methods removed).

---

## Summary: What each person/agent does per case

| Step | Creation | Modification | Deletion |
|---|---|---|---|
| **Human writes** | `spec.md` + `design_spec.md` + `traceability.md` | `spec.md` + `design_spec.md` (deltas) + `traceability.md` | `spec.md` + `design_spec.md` (removals) + `traceability.md` |
| **traceability.md includes** | `Based on: (none)` | `REUSE`, `MODIFY`, `CREATE` rows | `DELETE` and `REUSE` rows |
| **design_spec.md** | Full design | Only modified parts | Only removals |
| **Agent reads** | spec.md + design_spec.md | traceability.md + spec_4/bdd_spec.md + spec_4/design_spec.md | traceability.md + spec_4/bdd_spec.md + spec_4/design_spec.md |
| **Agent writes** | bdd_spec.md + todo.md + tests + code | bdd_spec.md (full) + todo.md + tests + code (modified) | bdd_spec.md (full, minus deleted) + todo.md + tests removed + code cleaned |
| **spec_4 (old)** | — | Unchanged in done/ | Unchanged in done/ |
| **New spec** | Moves to done/ | Moves to done/ | Moves to done/ |

## Key rule to remember

> **Previous specs never change.** They are historical records of what was required, designed, and implemented at that point in time. When a requirement changes, a new spec captures that change. The `traceability.md` connects the dots.
