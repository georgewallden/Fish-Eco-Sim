# world/sim.py
#
# Description:
# This module defines the `SimulationState` class, which is responsible for
# managing the control flow of the simulation. It tracks the current tick
# count, whether the simulation is paused, and handles logic for single or
# multiple simulation steps when paused. It separates the simulation control
# state from the simulation world content itself.
#
# Key responsibilities of this file:
# - Define the `SimulationState` class.
# - Track the current simulation tick count.
# - Manage the paused/running state.
# - Handle pending steps for manual tick advancement.
#
# Design Philosophy/Notes:
# - Encapsulates the simulation's state machine for playback control.
# - Provides methods for querying and modifying the state from other modules
#   (primarily `SimulationWorld`).

# Imports Description:
# This file does not require any imports from other modules within the project
# or from standard libraries in its current implementation.

# Code Block Descriptions:
# This section provides detailed blueprints for the code blocks implemented below.

# 1. Class: SimulationState
# Description:
# Manages the state of the simulation related to its execution flow:
# current tick number, whether it is paused, and how many pending steps
# are queued for execution when paused.
#
# Attributes:
# - tick_count (int): The total number of simulation ticks that have occurred since the last reset.
# - paused (bool): True if the simulation is currently paused, False otherwise.
# - pending_ticks (int): The number of simulation ticks remaining to be executed when in a paused state (used for stepping).
#
# Primary Role: Control the advancement and state (paused/running) of the simulation loop.

# 1.1 Method: __init__
# Description:
# Constructor for the SimulationState class. Initializes all state variables
# to their default starting values (tick count to 0, paused to False,
# pending ticks to 0).
# Inputs:
#   - self: The instance being initialized.
# Where Inputs Typically Come From: Called by `SimulationWorld.__init__` when the simulation world is created or reset.
# Restrictions on Inputs: None.
# Other Relevant Info: Sets the initial state of the simulation control.
#
# Description of Algorithm/Process:
# 1. Initialize `self.tick_count` to 0.
# 2. Initialize `self.paused` to `False`.
# 3. Initialize `self.pending_ticks` to 0.
#
# Description of Output:
# None. Side effect is initializing the state attributes of the `self` object.

# 1.2 Method: is_running
# Description:
# Checks and returns whether the simulation logic should proceed with a tick
# in the current frame. This occurs if the simulation is not paused OR if
# there are pending steps queued (allowing stepping even when paused).
# Inputs:
#   - self: The SimulationState instance.
# Where Inputs Typically Come From: Called by `SimulationWorld.update()` at the beginning of the tick logic.
# Restrictions on Inputs: None.
# Other Relevant Info: Determines if `SimulationWorld.update()`'s core logic block should execute.
#
# Description of Algorithm/Process:
# 1. Return the result of the boolean expression `not self.paused or self.pending_ticks > 0`.
#    This means it returns True if `self.paused` is False, or if `self.pending_ticks` is greater than 0.
#
# Description of Output:
# A boolean value indicating if the simulation should execute a tick. Type: bool.
# Output Range: `True` or `False`.

# 1.3 Method: increment_tick
# Description:
# Advances the simulation's internal tick counter and decrements the count of
# pending steps if any are queued. This should be called once at the start
# of the simulation logic for a tick.
# Inputs:
#   - self: The SimulationState instance.
# Where Inputs Typically Come From: Called by `SimulationWorld.update()` after confirming `is_running()` is True.
# Restrictions on Inputs: None.
# Other Relevant Info: Modifies `self.tick_count` and `self.pending_ticks`.
#
# Description of Algorithm/Process:
# 1. Increment `self.tick_count` by 1.
# 2. Check if `self.pending_ticks` is greater than 0.
# 3. If it is, decrement `self.pending_ticks` by 1.
#
# Description of Output:
# None. Side effects are incrementing `self.tick_count` and potentially decrementing `self.pending_ticks`.

# 1.4 Method: toggle_pause
# Description:
# Switches the `paused` state of the simulation. If currently running, it
# pauses, and if currently paused, it resumes. When pausing, any pending
# steps are cleared to prevent unexpected jumps upon unpausing.
# Inputs:
#   - self: The SimulationState instance.
# Where Inputs Typically Come From: Called by the UI's button handling logic (`ui.buttons::handle_button_click`).
# Restrictions on Inputs: None.
# Other Relevant Info: Directly modifies `self.paused` and `self.pending_ticks`.
#
# Description of Algorithm/Process:
# 1. Flip the boolean value of `self.paused` (if True becomes False, if False becomes True).
# 2. Check if the simulation just became paused (`self.paused` is now True).
# 3. If it became paused, set `self.pending_ticks` to 0.
#
# Description of Output:
# None. Side effect is toggling the simulation's paused state and potentially clearing pending steps.

# 1.5 Method: reset
# Description:
# Resets the simulation control state back to its initial values: tick count
# to 0, paused to False, and pending steps to 0.
# Inputs:
#   - self: The SimulationState instance.
# Where Inputs Typically Come From: Called by `SimulationWorld.__init__()` (or a future dedicated `reset` method) when the overall world is reset.
# Restrictions on Inputs: None.
# Other Relevant Info: Mirrors the initialization logic.
#
# Description of Algorithm/Process:
# 1. Set `self.tick_count` to 0.
# 2. Set `self.paused` to `False`.
# 3. Set `self.pending_ticks` to 0.
#
# Description of Output:
# None. Side effect is resetting the state attributes of the `self` object.

# 1.6 Method: step_once
# Description:
# Queues a single simulation step to be executed, primarily used when the
# simulation is paused to advance it by one tick. If already running, it
# doesn't prevent the next tick, but ensures at least one additional tick
# happens if paused.
# Inputs:
#   - self: The SimulationState instance.
# Where Inputs Typically Come From: Called by the UI's button handling logic (`ui.buttons::handle_button_click`) for the "Tick Once" button.
# Restrictions on Inputs: None.
# Other Relevant Info: Modifies `self.pending_ticks`.
#
# Description of Algorithm/Process:
# 1. Check if the simulation is currently `self.paused`.
# 2. If it is paused, increment `self.pending_ticks` by 1. (The `max(1, self.pending_ticks + 1)` logic from the original code is slightly redundant but harmless; simply `self.pending_ticks += 1` inside the `if` is sufficient if you only queue steps when paused).
#
# Description of Output:
# None. Side effect is incrementing `self.pending_ticks` if paused.

# 1.7 Method: step_many
# Description:
# Queues a specified number of simulation steps to be executed, used when
# the simulation is paused to advance it by multiple ticks at once.
# Inputs:
#   - self: The SimulationState instance.
#   - n: The number of ticks to queue. Type: int. Origin: Passed from `ui.buttons::handle_button_click` based on the selected tick jump value. Restrictions: Should be a non-negative integer.
# Where Inputs Typically Come From: Called by the UI's button handling logic (`ui.buttons::handle_button_click`) for the "Run N Ticks" button.
# Restrictions on Inputs: `n` should be >= 0.
# Other Relevant Info: Modifies `self.pending_ticks`. Only queues steps if paused and `n > 0`.
#
# Description of Algorithm/Process:
# 1. Check if the simulation is currently `self.paused` AND if `n` is greater than 0.
# 2. If both conditions are true, add `n` to `self.pending_ticks`.
#
# Description of Output:
# None. Side effect is increasing `self.pending_ticks` if paused and `n > 0`.

# 1.8 Method: finish_step
# Description:
# A placeholder method. In more complex simulation loops with multiple stages
# per tick, this could be used to signal completion of a step. In the current
# simple tick structure, its functionality is minimal as `increment_tick`
# already handles the pending count.
# Inputs:
#   - self: The SimulationState instance.
# Where Inputs Typically Come From: Called by `SimulationWorld.update()` at the end of the tick logic.
# Restrictions on Inputs: None.
# Other Relevant Info: Currently, this method performs no operation (`pass`).
#
# Description of Algorithm/Process:
# 1. Performs no operation.
#
# Description of Output:
# None. No side effects in the current implementation.


# --- START CODE IMPLEMENTATION ---

### 1. Class: SimulationState Implementation ###
class SimulationState:
    ### 1.1 Method: __init__ Implementation ###
    def __init__(self):
        """Initializes the simulation state."""
        self.tick_count = 0     # Current simulation tick number
        self.paused = False     # Whether the simulation is currently paused
        self.pending_ticks = 0  # Number of steps remaining when using step_once/step_many

    ### 1.2 Method: is_running Implementation ###
    def is_running(self):
        """Checks if the simulation should currently perform a tick."""
        # Simulation runs if not paused OR if there are pending steps
        return not self.paused or self.pending_ticks > 0

    ### 1.3 Method: increment_tick Implementation ###
    def increment_tick(self):
        """Increments the tick count and decrements pending steps."""
        self.tick_count += 1
        if self.pending_ticks > 0:
            self.pending_ticks -= 1

    ### 1.4 Method: toggle_pause Implementation ###
    def toggle_pause(self):
        """Toggles the paused state."""
        self.paused = not self.paused
        # When pausing, clear any pending steps so it doesn't suddenly jump after unpausing
        if self.paused:
            self.pending_ticks = 0

    ### 1.5 Method: reset Implementation ###
    def reset(self):
        """Resets the simulation state variables."""
        self.tick_count = 0
        self.paused = False
        self.pending_ticks = 0

    ### 1.6 Method: step_once Implementation ###
    def step_once(self):
        """Queues a single simulation step."""
        # Ensure at least one step is pending if paused
        # Original code was max(1, self.pending_ticks + 1), but simpler increment works if only called when paused
        if self.paused:
             self.pending_ticks += 1


    ### 1.7 Method: step_many Implementation ###
    def step_many(self, n):
        """Queues multiple simulation steps."""
        # Add n steps to pending, used when paused, only if n > 0
        if self.paused and n > 0:
            self.pending_ticks += n

    ### 1.8 Method: finish_step Implementation ###
    def finish_step(self):
        """Called at the end of a simulation logic update to finalize step_once/many."""
        # This isn't strictly necessary with the current logic but could be used
        # if you needed to signal completion of a complex multi-stage tick.
        pass


# --- END CODE IMPLEMENTATION ---