# BDD Specification — Add Object Button

> Derived from `spec.md` — Requirement 1

---

```gherkin
Feature: Add Object Button
  As an operator
  I want to press the "Add object" button multiple times to define paths for multiple objects
  So that I can set up several moving objects in the simulation before starting

  Background:
    Given the simulation application is running
    And no objects have been added yet

  Scenario: Start drawing a path for the first object
    When the operator presses the "Add object" button
    Then the application enters path-drawing mode
    And the "Add object" button is locked in active state

  Scenario: Complete drawing and create the first object
    Given the operator is in path-drawing mode
    And they have placed 2 or more waypoints on the canvas
    When they press the "Add object" button again
    Then the path is finalized for the object
    And a new object is added to the simulation
    And path-drawing mode is exited

  Scenario: Add a second object after the first one is created
    Given one object has been created and added to the simulation
    When the operator presses the "Add object" button
    Then the application enters path-drawing mode again
    And the operator can define a path for a second object

  Scenario: Cancel drawing without placing waypoints
    Given the operator is in path-drawing mode
    And no waypoints have been placed on the canvas
    When they press the "Add object" button
    Then path-drawing mode is exited
    And no object is created

  Scenario: Button is locked while drawing path
    Given the operator is in path-drawing mode
    When they press the "Add object" button
    Then the drawing is finalized (if waypoints exist)
    Or path-drawing mode is cancelled (if no waypoints)
    And the button returns to normal (non-locked) state
```
