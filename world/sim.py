# world/sim.py
# Manages the overall simulation state and flow

class SimulationState:
    """
    Manages the simulation's control state: tick count, pause/play, stepping.
    """
    def __init__(self):
        """Initializes the simulation state."""
        self.tick_count = 0     # Current simulation tick number
        self.paused = False     # Whether the simulation is currently paused
        self.pending_ticks = 0  # Number of steps remaining when using step_once/step_many

    def is_running(self):
        """Checks if the simulation should currently perform a tick."""
        # Simulation runs if not paused OR if there are pending steps
        return not self.paused or self.pending_ticks > 0

    def increment_tick(self):
        """Increments the tick count and decrements pending steps."""
        self.tick_count += 1
        if self.pending_ticks > 0:
            self.pending_ticks -= 1

    def toggle_pause(self):
        """Toggles the paused state."""
        self.paused = not self.paused
        # When pausing, clear any pending steps so it doesn't suddenly jump after unpausing
        if self.paused:
            self.pending_ticks = 0

    def reset(self):
        """Resets the simulation state variables."""
        self.tick_count = 0
        self.paused = False
        self.pending_ticks = 0

    def step_once(self):
        """Queues a single simulation step."""
        # Ensure at least one step is pending if paused
        if self.paused:
             self.pending_ticks = max(1, self.pending_ticks + 1)


    def step_many(self, n):
        """Queues multiple simulation steps."""
        # Add n steps to pending, used when paused
        if self.paused and n > 0:
            self.pending_ticks += n

    def finish_step(self):
        """Called at the end of a simulation logic update to finalize step_once/many."""
        # This isn't strictly necessary with the current logic but could be used
        # if you needed to signal completion of a complex multi-stage tick.
        pass