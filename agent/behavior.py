# agent/behavior.py
#
# Description:
# This module houses the logic for agent decision-making, sensing the environment,
# and determining movement direction based on perceived information and the agent's
# internal state and traits. It defines functions that are called by the `Agent.update`
# method to drive complex, goal-oriented behaviors like seeking food.
#
# Key responsibilities of this file:
# - Implement functions for agents to sense the environment (e.g., finding nearby food).
# - Implement decision-making logic based on agent state and sensed environment.
# - Implement functions to calculate movement direction towards a target.
# - Determine and set an agent's target.
#
# Design Philosophy/Notes:
# - Separates complex behavioral logic from the core Agent state management (`agent.base`).
# - Relies on agent traits (`agent.traits`) to influence behavior (e.g., vision range).
# - Requires access to the `SimulationWorld` instance to sense the global environment,
#   ideally by calling dedicated sensing methods on the `world` object to reduce
#   direct coupling to the world's internal data structures (e.g., `world.food`).
#   (Initial implementation might access world internals directly, but future versions
#   should use world methods).
# - Focuses on *what* the agent decides to do and *where* it decides to go; the
#   actual position update is handled by `agent.movement`.

# Imports Description:
# This section lists the modules imported by agent/behavior.py and their purpose.
# - random: Standard library, potentially needed for random components in decision-making or wandering if not handled in movement. (Included in original, keep for now).
# - math: Standard library, potentially needed for distance calculations (e.g., `math.sqrt` if using Euclidean distance, though squared distance is faster). (Included in original sketch).
# - config: Imports constants (`GRID_COLS`, `GRID_ROWS`) necessary for calculating distances with world wrap-around. Also may need constants for behavior thresholds (e.g., energy level to seek food).
# - world.SimulationWorld: Type hint or access if needed (the world object is passed in).
# - world.food.FoodPellet: Type hint or access if needed (agents might target FoodPellet objects).

# Code Block Descriptions:
# This section provides detailed blueprints for the code blocks (functions)
# implemented below.

# 1. Function: find_nearest_food
# Description:
# Searches for the closest edible food pellet within the agent's vision range.
# Considers the agent's position and the vision range trait. Returns the first
# nearest food found, or None if no food is within range. Horizontal wrap-around
# is considered when calculating distance.
# Inputs:
#   - agent: The Agent instance performing the search. Type: agent.Agent.
#            Origin: Called by `decide_next_action`.
#            Restrictions: Must be a valid Agent object with `x`, `y` and `traits.vision_range` attributes.
#   - food_list: A list of active FoodPellet instances currently in the world. Type: list[world.food.FoodPellet].
#                Origin: Passed from the `SimulationWorld` instance (e.g., `world.food`).
#                Restrictions: Must be a list containing objects that have `x`, `y`, and `energy_value` attributes.
# Where Inputs Typically Come From: Called by `decide_next_action`, which receives `agent` and `world` and passes `world.food`.
# Restrictions on Inputs: None.
# Other Relevant Info: Calculates distance using grid coordinates. Squared distance comparison is used for efficiency. Uses `agent.traits.vision_range` and `config.GRID_COLS` for wrap-around distance check.
#
# Description of Algorithm/Process:
# 1. Initialize variables: `nearest_food = None` and `min_dist_sq = float('inf')` (a very large initial distance).
# 2. Get the agent's current position (`agent_x`, `agent_y`) and its squared vision range (`vision_range_sq = agent.traits.vision_range ** 2`).
# 3. Iterate through each `pellet` in the input `food_list`.
# 4. For each `pellet`, check if it's currently edible (`pellet.energy_value > 0`). If not, skip it.
# 5. Get the pellet's position (`pellet_x`, `pellet_y`).
# 6. Calculate the difference in coordinates (`dx = pellet_x - agent_x`, `dy = pellet_y - agent_y`).
# 7. Adjust `dx` to account for horizontal grid wrap-around: if moving left or right across the wrap boundary is shorter than moving straight, use the wrapped distance. This requires checking if `dx` is greater than half the grid width or less than negative half the grid width and adjusting `dx` accordingly (`if dx > GRID_COLS / 2: dx -= GRID_COLS`, `elif dx < -GRID_COLS / 2: dx += GRID_COLS`). Vertical wrap is not needed as per `agent.movement`.
# 8. Calculate the squared distance between the agent and the pellet: `dist_sq = dx**2 + dy**2`.
# 9. Check if `dist_sq` is within the agent's `vision_range_sq` AND if it's less than the current `min_dist_sq`.
# 10. If both conditions are true, update `min_dist_sq = dist_sq` and `nearest_food = pellet`.
# 11. After iterating through all food pellets, return the `nearest_food` object found (or None if none were within range).
#
# Description of Output:
# A `FoodPellet` instance representing the nearest edible food within vision, or `None`. Type: world.food.FoodPellet or NoneType.
# Output Range: A reference to an object from the input `food_list`, or `None`.

# 2. Function: decide_next_action
# Description:
# Determines the agent's primary goal or target for this tick based on its
# current state (e.g., energy level) and by sensing the environment. It
# might set the agent's `target` attribute to a food pellet, a mate, or
# potentially clear the target if the goal is met or no longer viable.
# Currently prioritizes finding food if energy is below a threshold.
# Inputs:
#   - agent: The Agent instance making the decision. Type: agent.Agent.
#            Origin: Called by `Agent.update`.
#            Restrictions: Must be a valid Agent object with `traits.energy` and `target` attributes.
#   - world: The SimulationWorld instance, needed for sensing the environment
#            (e.g., accessing `world.food`). Type: world.SimulationWorld.
#            Origin: Passed from `Agent.update`.
#            Restrictions: Must be a valid SimulationWorld object with accessible
#            environmental data (like `world.food`). (Ideally this would call
#            `world.get_food_in_range()` methods, but currently accesses `world.food` directly).
# Where Inputs Typically Come From: Called by `Agent.update()` during each tick.
# Restrictions on Inputs: None.
# Other Relevant Info: Modifies the agent's `target` attribute. Uses `agent.traits.energy`. Calls `find_nearest_food`.
#
# Description of Algorithm/Process:
# 1. Define an energy threshold below which the agent prioritizes seeking food (e.g., 30.0).
# 2. Check if the agent's current energy (`agent.traits.energy`) is below this threshold.
# 3. If energy is below the threshold:
#    a. Call `find_nearest_food(agent, world.food)` to search for food in the environment (accessing `world.food` directly for now).
#    b. If `find_nearest_food` returns a food object (`found_food` is not None):
#       i. Set the agent's target to the found food: `agent.target = found_food`.
#       ii. (Optional) Add debug print or visual cue.
#    c. If `find_nearest_food` returns `None` (no food found in vision), and the agent currently has a target (`agent.target is not None`), clear the target: `agent.target = None`. This happens if the previous target went out of range or was eaten by another agent.
# 4. Else (energy is not below the threshold, or energy is full):
#    a. (Current simple logic) If the agent *does* have a target AND that target is a food pellet (to avoid clearing other potential targets like mates later), potentially clear the target if energy is high enough. However, the simpler logic is to just let it eat if it's on the food. Let's keep the target until it's eaten for now.
#    b. If the agent has no target, no action is needed here; random wandering is handled in `move_agent`.
# 5. (Future): Add logic for other priorities: fleeing predators if seen, seeking mates if energy and age allow, random wandering if no high-priority goal.
#
# Description of Output:
# None. Side effect is potentially modifying the agent's `target` attribute.

# 3. Function: move_towards_target
# Description:
# Adjusts the agent's `direction` attribute to point one step closer towards
# its current `target`. Assumes the agent has a valid `target`. It calculates
# the required horizontal and vertical movement (dx, dy) considering horizontal
# grid wrap-around and prioritizes the axis with the largest difference.
# Inputs:
#   - agent: The Agent instance whose direction is being updated. Type: agent.Agent.
#            Origin: Called by `Agent.update` when the agent is ready to move AND has a target.
#            Restrictions: Must be a valid Agent object with `x`, `y`, `direction`, and `target` attributes. `agent.target` is assumed to be a valid object with `x` and `y` attributes.
# Where Inputs Typically Come From: Called by `Agent.update()`.
# Restrictions on Inputs: `agent.target` must not be `None`.
# Other Relevant Info: Modifies the agent's `direction`. Uses `config.GRID_COLS` for wrap-around calculation. Relies on `agent.movement.move_agent` to apply the updated direction.
#
# Description of Algorithm/Process:
# 1. Get the agent's current grid position (`agent_x`, `agent_y`).
# 2. Get the target's grid position (`target_x`, `target_y`) from `agent.target.x` and `agent.target.y`.
# 3. Calculate the raw coordinate differences: `dx = target_x - agent_x`, `dy = target_y - agent_y`.
# 4. Adjust `dx` to account for horizontal wrap-around: if the target is "closer" by wrapping around the horizontal edge, use the wrapped difference. Check if `dx` is greater than half the grid width or less than negative half the grid width (`if dx > GRID_COLS / 2: dx -= GRID_COLS`, `elif dx < -GRID_COLS / 2: dx += GRID_COLS`).
# 5. Decide the agent's new direction based on `dx` and `dy`:
#    a. If `dx` is non-zero AND the absolute horizontal difference is greater than or equal to the absolute vertical difference (`abs(dx) >= abs(dy)`) OR the vertical difference is zero (`dy == 0`): Prioritize horizontal movement.
#       - If `dx > 0`, set `agent.direction = "E"`.
#       - If `dx < 0`, set `agent.direction = "W"`.
#    b. Else (if `dy` is non-zero, which covers cases where vertical is prioritized, or only vertical is needed): Prioritize vertical movement.
#       - If `dy > 0`, set `agent.direction = "S"`.
#       - If `dy < 0`, set `agent.direction = "N"`.
#    c. If `dx` is 0 and `dy` is 0, the agent is already on the target square. The direction doesn't need to change for movement purposes, and the agent's direction can remain as is.
# 6. (Note: The actual movement to the new `x`, `y` coordinates happens when `agent.movement.move_agent` is called *after* this function in `Agent.update`).
#
# Description of Output:
# None. Side effect is modifying the agent's `direction` attribute to point towards its target.


# --- START CODE IMPLEMENTATION ---
# Imports:
# Standard library imports first
import random # Potentially needed for random decisions or wandering (if not handled by movement)
import math # Potentially needed for distance calculations (though squared distance is simple)

# Local package imports
from config import GRID_COLS, GRID_ROWS # Need grid bounds for wrap-around calculations and sensing
# from world.food import FoodPellet # Needed if checking isinstance(agent.target, FoodPellet)
# from world.simulation_world import SimulationWorld # Needed for type hinting world

### 1. Function: find_nearest_food Implementation ###
# Requires agent and food_list as inputs
def find_nearest_food(agent, food_list):
    """
    Searches for the closest edible food pellet within the agent's vision range.
    Returns the nearest food object or None.
    """
    nearest_food = None
    # Use float('inf') for initial minimum distance squared
    min_dist_sq = float('inf')

    agent_x, agent_y = agent.x, agent.y
    # Get vision range from agent's traits and square it for comparison
    vision_range_sq = agent.traits.vision_range ** 2

    # Iterate through all food pellets in the world
    for pellet in food_list:
        # Check if food is edible (energy_value > 0)
        if pellet.energy_value <= 0:
            continue

        pellet_x, pellet_y = pellet.x, pellet.y

        # Calculate difference in coordinates
        dx = pellet_x - agent_x
        dy = pellet_y - agent_y

        # --- Handle horizontal wrap-around for distance calculation ---
        # Check if wrapping horizontally is a shorter path
        # Only apply if the absolute difference is greater than half the grid width
        if dx > GRID_COLS // 2: # Integer division is fine here
            dx -= GRID_COLS
        elif dx < -GRID_COLS // 2:
            dx += GRID_COLS
        # Vertical wrap-around is not implemented in world/movement, so simple dy is fine

        # Calculate squared Euclidean distance
        dist_sq = dx**2 + dy**2

        # Check if within vision range and closer than current nearest
        if dist_sq <= vision_range_sq and dist_sq < min_dist_sq:
            min_dist_sq = dist_sq
            nearest_food = pellet

    return nearest_food # Return the nearest food object found, or None

### 2. Function: decide_next_action Implementation ###
# Requires agent and world as inputs
def decide_next_action(agent, world):
    """
    Determines the agent's primary goal or target for this tick based on its state and environment.
    Sets agent.target accordingly.
    """
    # Import necessary types locally for checks if needed (optional, can use duck typing)
    # from world.food import FoodPellet # Example import for isinstance check

    # Define energy threshold for seeking food
    # Use a value relative to potential max energy, or a fixed value.
    # Using fixed 30.0 for now, based on initial energy 50.0.
    energy_threshold_for_seeking_food = 30.0

    # Prioritize finding food if energy is below threshold
    if agent.traits.energy < energy_threshold_for_seeking_food:
        # Look for nearest food within vision range
        # Currently accessing world.food directly as per plan.
        # FUTURE: Use world.get_food_in_range(agent.x, agent.y, agent.traits.vision_range)
        found_food = find_nearest_food(agent, world.food)

        # If food is found within vision, set it as the target
        if found_food:
            agent.target = found_food
            # Optional Debug: print(f"Agent {id(agent)} at ({agent.x},{agent.y}) targeted food at ({found_food.x},{found_food.y}). Energy: {agent.traits.energy:.1f}") # Debug

        # If no food is found in vision, and agent was previously targeting *something*, clear the target
        # This makes the agent stop pursuing a target that is no longer visible or accessible
        elif agent.target is not None:
             agent.target = None
             # Optional Debug: print(f"Agent {id(agent)} at ({agent.x},{agent.y}) lost target. Energy: {agent.traits.energy:.1f}") # Debug

    # Optional: If energy is high enough, maybe clear food target and wander or seek mate (future)
    # For now, agents keep targeting food until they eat it or lose sight of it.
    # The eat method in agent.base can clear the target if food is eaten.
    # The logic above clears target if it goes out of sight.
    # So, no explicit "stop seeking food if energy is full" needed here yet.

    # If agent has no target after this logic, it will default to random wandering in move_agent.


### 3. Function: move_towards_target Implementation ###
# Requires agent as input (it has agent.target)
def move_towards_target(agent):
     """
     Adjusts the agent's direction to move one step closer towards its current target.
     Assumes agent.target is not None.
     """
     # Import necessary constants locally for calculations if needed
     from config import GRID_COLS
     # No need to import get_direction_delta or DIRECTIONS here, move_agent uses the final direction string

     # Defensive check, although Agent.update should only call this if target is not None
     if agent.target is None:
         # print("Warning: move_towards_target called with no target.") # Debug
         return

     target_x, target_y = agent.target.x, agent.target.y
     agent_x, agent_y = agent.x, agent.y

     # Calculate difference in coordinates
     dx = target_x - agent_x
     dy = target_y - agent_y

     # --- Handle horizontal wrap-around for direction decision ---
     # Check if moving the other way across the grid boundary is shorter
     if dx > GRID_COLS // 2: # Use integer division //
         dx -= GRID_COLS
     elif dx < -GRID_COLS // 2:
         dx += GRID_COLS

     # Decide direction based on adjusted dx and dy
     # Prioritize the axis with the largest difference, unless one axis difference is zero (already aligned)
     if dx != 0 and (abs(dx) >= abs(dy) or dy == 0):
         # Prioritize horizontal movement (or only horizontal movement needed)
         if dx > 0:
             agent.direction = "E" # Target is to the East
         else: # dx < 0
             agent.direction = "W" # Target is to the West
     elif dy != 0: # Prioritize vertical movement (or only vertical movement needed)
          if dy > 0:
              agent.direction = "S" # Target is to the South
          else: # dy < 0
              agent.direction = "N" # Target is to the North
     # If dx == 0 and dy == 0, agent is already on the target square.
     # The direction doesn't need to change for movement, agent stays put or moves randomly (if target cleared).
     # We don't need an 'else' here because the direction remains its current value if no new direction is chosen.


# --- END CODE IMPLEMENTATION ---