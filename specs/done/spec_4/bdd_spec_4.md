# BDD Specification - Pause Button

## Feature: Simulation Pause and Resume
  As a user running a simulation
  I want to pause and resume the simulation via the play/pause button
  So that I can inspect the state of objects at any point during the simulation

### Background:
  Given the simulation has at least one object with a valid path
  And the simulation has been started

### Scenario: Pause button is available only when simulation is running
  Given the simulation is running
  When the user clicks the play/pause button
  Then the simulation pauses
  And no movement is registered while paused

### Scenario: Pause button cannot pause a stopped simulation
  Given the simulation has not been started
  When the user clicks the play/pause button
  Then the simulation starts instead of pausing

### Scenario: Resume from paused state maintains position
  Given the simulation is running
  When the user pauses the simulation
  And then the user resumes the simulation
  Then the simulation continues from the same point where it was paused
  And movement resumes from that position

### Scenario: No movement while paused
  Given the simulation is running
  When the user pauses the simulation
  And time passes in the simulation
  Then no object moves from its current position

### Scenario: Reset clears pause state
  Given the simulation is paused
  When the user resets the simulation
  Then the simulation is stopped
  And the pause state is cleared
