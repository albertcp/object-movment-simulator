# BDD Specification — GUI Layout and Object Data Display (v2)

> Derived from `spec.md` — Requirement 3 (modified)

---

```gherkin
Feature: GUI Layout and Object Data Display
  As an operator
  I want a clearly organized control panel with buttons in a fixed order, help text at the bottom of the panel, a simulation status indicator always in green, and a list of all objects with their data
  So that I can efficiently manage and monitor the simulation

  Background:
    Given the simulation application is running

  Scenario: Buttons are displayed in the correct order
    Then the control panel shows buttons in the following order from top to bottom:
      | Order | Button      |
      | 1     | Add Object  |
      | 2     | Edit Speed  |
      | 3     | Play        |
      | 4     | Reset       |

  Scenario: Edit Speed button is only enabled when an object is selected
    Given no object is selected on the map
    Then the Edit Speed button is disabled
    When the operator clicks on an object to select it
    Then the Edit Speed button becomes enabled

  Scenario: Simulation status is always displayed in green text below all buttons
    Given the simulation has not been started
    Then the status text "Stopped" appears below all buttons in green
    When the operator starts the simulation
    Then the status text changes to "Running" still in green below all buttons
    When the operator pauses the simulation
    Then the status text changes to "Paused" still in green
    When the simulation finishes
    Then the status text shows "Complete!" in green

  Scenario: Help text for Add Object appears at the bottom of the left panel
    Given the operator is not in placing mode
    Then no help text is shown at the bottom of the panel
    When the operator clicks Add Object to enter placing mode
    Then help text appears at the bottom of the left side panel describing how to place waypoints

  Scenario: All objects data is displayed below buttons and status
    Given the simulation has 2 objects with different properties
    Then the panel displays a list below the status showing each object's:
      | Field      |
      | Name       |
      | Speed      |
      | State      |
      | Position   |
      | Waypoints  |

  Scenario: Objects list updates when a new object is added
    Given the simulation has 1 object displayed in the panel
    When the operator adds a second object
    Then the objects list shows 2 entries

  Scenario: Objects list updates when simulation runs
    Given the simulation is running with 1 object
    When the object moves to a new position
    Then the displayed position updates to reflect the object's current location
```
