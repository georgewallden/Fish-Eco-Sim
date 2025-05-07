# agent/movement.py
#
# Description:
# This module is responsible for the physical movement of agents on the grid.
# It provides functions to get direction vectors, generate random directions,
# and update an agent's position based on its current direction while applying
# grid boundary rules (horizontal wrapping, vertical clamping).
#
# Key responsibilities of this file:
# - Define mappings between direction strings and coordinate changes (delta).
# - Provide a way to get a random valid direction.
# - Update an agent's grid coordinates based on its direction.
# - Implement boundary handling for the grid (wrap-around and clamping).
#
# Design Philosophy/Notes:
# - Purely a movement mechanics module; contains no decision-making logic.
# - The agent's direction is assumed to be set by calling code (like the
#   `agent.behavior` module or a default wandering logic).
# - Relies on `config.py` for grid dimensions.
# - Uses the Agent instance directly to read its current state (direction, position)
#   and modify its position.

# Imports Description:
# This section lists the modules imported by agent/movement.py and their purpose.
# - random: Standard library, needed for selecting a random direction in `get_random_direction`.
# - config: Imports constants (`GRID_COLS`, `GRID_ROWS`) required for applying boundary rules in `move_agent`.

# Code Block Descriptions:
# This section provides detailed blueprints for the code blocks implemented below.

# 1. Constant: DIRECTIONS
# Description:
# A dictionary mapping cardinal direction strings to corresponding grid
# coordinate changes (dx, dy). This is a lookup table for direction vectors.
# Attributes defined in this block:
# - DIRECTIONS (dict[str, tuple[int, int]]): Mapping from direction names to delta coordinates.
# Process:
# Defined as a global constant when the module is imported.
# Output:
# None. Defines a global constant available within the module.

# 2. Function: get_random_direction
# Description:
# Selects one of the defined cardinal directions randomly and returns its
# string representation.
# Inputs: None.
# Where Inputs Typically Come From: Called by `Agent.__init__` for initial direction, or by `move_agent` (conditionally) or `agent.behavior` for random wandering.
# Restrictions on Inputs: None.
# Other Relevant Info: Uses the `DIRECTIONS` constant and the `random` module.
#
# Description of Algorithm/Process:
# 1. Get a list of the keys (direction strings) from the `DIRECTIONS` dictionary.
# 2. Use `random.choice()` to randomly select one string from this list.
# 3. Return the selected direction string.
#
# Description of Output:
# A string representing one of the cardinal directions ("N", "S", "E", "W"). Type: str.
# Output Range: Limited to the keys of the `DIRECTIONS` dictionary.

# 3. Function: get_direction_delta
# Description:
# Returns the corresponding (dx, dy) tuple (coordinate change) for a given
# direction string by looking it up in the `DIRECTIONS` dictionary.
# Inputs:
#   - direction: A string representing the direction (e.g., "N", "S"). Type: str.
#                Origin: Typically the `agent.direction` attribute.
#                Restrictions: Expected to be one of the keys in `DIRECTIONS`.
# Where Inputs Typically Come From: Called by `move_agent`.
# Restrictions on Inputs: None.
# Other Relevant Info: Uses the `DIRECTIONS` constant. Provides a default (0,0) if the direction is unrecognized.
#
# Description of Algorithm/Process:
# 1. Use the `.get()` method on the `DIRECTIONS` dictionary to look up the input `direction`.
# 2. If the key is found, return its corresponding (dx, dy) tuple value.
# 3. If the key is not found, return the default value `(0, 0)`.
#
# Description of Output:
# A tuple of two integers representing the change in x and y grid coordinates. Type: tuple[int, int].
# Output Range: `(-1, 0)`, `(1, 0)`, `(0, -1)`, `(0, 1)`, or `(0, 0)`.

# 4. Function: move_agent
# Description:
# Updates the grid position (`agent.x`, `agent.y`) of an agent based on its
# current direction. It applies horizontal wrap-around (moving off the left
# edge appears on the right) and vertical clamping (cannot move past the
# top or bottom edges). Includes a conditional random direction change if
# the agent has no target (basic wandering).
# Inputs:
#   - agent: The Agent instance to move. Type: agent.Agent.
#            Origin: Passed from `Agent.update()` when it's time for the agent to move.
#            Restrictions: Must be a valid Agent object with `x`, `y`, `direction`, and `target` attributes.
# Where Inputs Typically Come From: Called by `Agent.update()`.
# Restrictions on Inputs: None.
# Other Relevant Info: Modifies the `agent.x` and `agent.y` attributes. Uses `GRID_COLS` and `GRID_ROWS` from `config.py`. Calls `get_direction_delta` and potentially `get_random_direction`.
#
# Description of Algorithm/Process:
# 1. Get the coordinate change `(dx, dy)` corresponding to the agent's current `agent.direction` by calling `get_direction_delta(agent.direction)`.
# 2. Calculate the potential new grid position: `new_x = agent.x + dx`, `new_y = agent.y + dy`.
# 3. Apply horizontal wrap-around: Update `agent.x` to `new_x % GRID_COLS`. Python's modulo handles both positive and negative results correctly for wrapping.
# 4. Apply vertical clamping:
#    a. Check if `new_y` is greater than or equal to 0 AND less than `GRID_ROWS`.
#    b. If `new_y` is within the vertical bounds, update `agent.y = new_y`.
#    c. If `new_y` is outside the vertical bounds (less than 0 or >= `GRID_ROWS`), the agent's `agent.y` remains unchanged (it hits the "boundary").
# 5. (Conditional Random Movement): Check if the agent currently has `agent.target` set to `None` AND if a random chance (e.g., 10%) passes.
# 6. If the agent has no target and the random chance passes:
#    a. Call `get_random_direction()` and assign the result to `agent.direction`. This makes the agent wander randomly when not pursuing a target.
#
# Description of Output:
# None. Side effects include updating the agent's `x` and `y` position and potentially changing its `direction` if it has no target and the random chance occurs.


# --- START CODE IMPLEMENTATION ---

# Imports:
# Standard library imports first
import random

# Local package imports
# Import constants needed for boundary handling
from config import GRID_COLS, GRID_ROWS


### 1. Constant: DIRECTIONS Implementation ###
DIRECTIONS = {
    "N": (0, -1), # Up
    "S": (0, 1),  # Down
    "E": (1, 0),  # Right
    "W": (-1, 0), # Left
}


### 2. Function: get_random_direction Implementation ###
def get_random_direction():
    """Returns a random cardinal direction string."""
    return random.choice(list(DIRECTIONS.keys())) # Use keys() to get list of direction strings


### 3. Function: get_direction_delta Implementation ###
def get_direction_delta(direction):
    """Returns the (dx, dy) tuple for a given direction string."""
    # Use .get() with a default to handle potential invalid directions gracefully
    return DIRECTIONS.get(direction, (0, 0))


### 4. Function: move_agent Implementation ###
def move_agent(agent):
    """
    Calculates the agent's new position based on its direction.
    Applies border wrapping horizontally and clamping vertically.
    Includes conditional random direction change if the agent has no target.
    """
    # Get the coordinate change based on the agent's current direction
    dx, dy = get_direction_delta(agent.direction)

    # Calculate potential new position
    new_x = agent.x + dx
    new_y = agent.y + dy

    # Apply border rules
    # Horizontal wrap-around (left/right edges connect)
    # Python's % operator works correctly for both positive and negative new_x
    agent.x = new_x % GRID_COLS

    # Vertical clamping (cannot move past top/bottom edges)
    # Only update y if the new position is within the valid row range
    if 0 <= new_y < GRID_ROWS:
        agent.y = new_y
    # If new_y is outside the range, agent.y remains its current value

    # Optional: Chance to change direction randomly after moving
    # This adds a bit of randomness/wandering, but ONLY if the agent currently has no target.
    # If the agent has a target, the direction is set by behavior.move_towards_target
    if agent.target is None and random.random() < 0.1: # 10% chance to change direction if wandering
        agent.direction = get_random_direction()


# --- END CODE IMPLEMENTATION ---