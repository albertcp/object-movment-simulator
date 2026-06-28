# BDD Specification — Edit Object Speed

> Derived from `spec.md` — Requirement 2

---

```gherkin
Feature: Edit Object Speed
  As an operator
  I want to modify the speed of a selected object before starting the simulation
  So that each object can move at its desired velocity in meters per second

  Background:
    Given the simulation application is running
    And at least one object has been created with a default speed

  Scenario: Edit Speed button is visible when an object is selected
    Given an object is placed on the map
    When the operator clicks on the object to select it
    Then the "Edit Speed" button appears in the control panel

  Scenario: Clicking Edit Speed opens a popup with the current speed
    Given an object is selected
    When the operator clicks the "Edit Speed" button
    Then a popup is displayed showing the current speed in meters per second
    And the speed value is pre-filled ready for editing

  Scenario: Operator types a new speed value
    Given the speed editing popup is open with the current speed shown
    When the operator types a valid numeric speed value
    Then the input field updates with the new value

  Scenario: Operator confirms the new speed
    Given the speed editing popup is open
    And the operator has typed a new speed value
    When they press Enter
    Then the popup closes
    And the object's speed is updated to the new value

  Scenario: Operator cancels speed editing
    Given the speed editing popup is open
    And the operator has typed a new speed value
    When they press Escape
    Then the popup closes
    And the object's speed remains unchanged

  Scenario: Object moves at the new speed when simulation starts
    Given an object has its speed modified to a new value
    When the operator presses the start button
    Then the object moves along its path at the new speed
    And the position is computed using the updated speed value

  Scenario: Non-numeric input is rejected during speed editing
    Given the speed editing popup is open
    When the operator types a non-numeric character
    Then the character is ignored
    And the speed input remains unchanged

  Scenario: Speed editing is not available during simulation
    Given the simulation is running
    When the operator selects an object and clicks "Edit Speed"
    Then no speed editing popup appears
    And the object's speed cannot be modified

  Scenario: Speed editing is not available while placing waypoints
    Given the operator is in path-drawing mode
    When they click "Edit Speed"
    Then no speed editing popup appears
```

