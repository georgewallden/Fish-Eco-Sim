# agent/behavior.py
#
# Description:
# This module implements the agent's behavior state machine and the logic
# for each behavioral state. It defines the possible states an agent can
# be in (e.g., wandering, seeking food) and provides functions for determining
# state transitions and executing the actions associated with the current state.
# This module integrates sensing (using world data via agent/world methods),
# decision-making, and driving the movement logic from `agent.movement`.
#
# Key responsibilities of this file:
# - Define the set of possible behavior states.
# - Implement the logic for deciding when an agent should transition between states.
# - Implement the actions that an agent performs while in a specific state.
# - Provide helper functions for common behavioral tasks like sensing the environment
#   (e.g., finding targets) and determining movement towards a target.
# - Manage agent movement timing and energy costs within state execution.
#
# Design Philosophy/Notes:
# - Implements the State Machine pattern for agent behavior.
# - The `get_next_state` function handles all state transition logic.
# - The `execute_current_state` function dispatches to state-specific action logic.
# - Relies on agent state and traits (passed via the `agent` object).
# - Requires access to the `SimulationWorld` instance for sensing and potential
#   interaction (ideally via world methods).
# - Uses helper functions for specific tasks like finding targets or pathfinding.

# Imports Description:
# This section lists the modules imported by agent/behavior.py and their purpose.
# - random: Standard library, potentially needed for random components in behavior (e.g., random wandering direction if not handled by movement, or random decision tie-breaking).
# - math: Standard library, used for distance calculations (e.g., `math.sqrt` if using Euclidean distance, or simple arithmetic for squared distance).
# - config: Imports constants (`GRID_COLS`, `GRID_ROWS`) necessary for sensing calculations (e.g., wrap-around distance). May also need constants for behavior thresholds (e.g., energy levels for state changes).
# - agent.movement.move_agent: Imports the function to execute the agent's physical movement after its direction is set.
# - agent.movement.get_random_direction: Imports the helper for random directions, potentially for wandering state.
# - world.SimulationWorld: Type hint or access if needed (the world object is passed in).
# - world.food.FoodPellet: Type hint or access if needed (agents might target FoodPellet objects).

# Code Block Descriptions:
# This section provides detailed blueprints for the code blocks implemented below.

# 1. Class: AgentState
# Description:
# Defines the possible discrete behavior states that an agent can be in.
# Using a class with class attributes as constants provides a clear and
# organized way to represent these states.
# Attributes defined in this block:
# - WANDERING (str): State where the agent moves randomly or without a specific target.
# - SEEKING_FOOD (str): State where the agent is actively trying to find and move towards food.
# - FLEEING_PREDATOR (str): (Future) State where the agent detects a predator and attempts to move away safely.
# - SEEKING_MATE (str): (Future) State where the agent is looking for a mate for reproduction.
# - REPRODUCING (str): (Future) State where the agent is engaged in reproduction.
# - IDLE (str): (Future) State where the agent is inactive, perhaps conserving energy.
# Process:
# Defined as a simple class with string constants as attributes when the module is imported.
# Output:
# None. Defines constants representing behavior states.

# 2. Function: find_nearest_food (Helper)
# Description:
# Searches for the closest edible food pellet within the agent's vision range.
# This is a helper function used by decision-making logic (like `get_next_state`
# or state-specific logic in `execute_current_state`) when the agent needs to
# find a food target.
# Inputs:
#   - agent: The Agent instance performing the search. Type: agent.Agent.
#            Origin: Called by decision/sensing logic.
#            Restrictions: Must have `x`, `y`, and `traits.vision_range`.
#   - food_list: A list of active FoodPellet instances. Type: list[world.food.FoodPellet].
#                Origin: Passed from `SimulationWorld` (e.g., `world.food`).
#                Restrictions: Elements must have `x`, `y`, `energy_value`.
# Where Inputs Typically Come From: Called by `get_next_state` or state execution functions.
# Restrictions on Inputs: None.
# Other Relevant Info: Calculates distance considering horizontal wrap-around.
#
# Description of Algorithm/Process:
# 1. Initialize `nearest_food = None` and `min_dist_sq = float('inf')`.
# 2. Get agent's position and squared vision range.
# 3. Iterate through `food_list`.
# 4. For each `pellet`, check if edible (`energy_value > 0`).
# 5. Get pellet position and calculate `dx`, `dy`.
# 6. Adjust `dx` for horizontal wrap-around using `config.GRID_COLS`.
# 7. Calculate squared distance `dist_sq = dx**2 + dy**2`.
# 8. If `dist_sq <= vision_range_sq` AND `dist_sq < min_dist_sq`, update `min_dist_sq` and `nearest_food`.
# 9. Return `nearest_food`.
#
# Description of Output:
# A `FoodPellet` instance or `None`. Type: world.food.FoodPellet or NoneType.

# 3. Function: get_next_state
# Description:
# Determines the agent's next behavior state based on its current state,
# traits, and the environmental context provided by the world. This is the
# core state transition logic of the state machine.
# Inputs:
#   - agent: The Agent instance. Type: agent.Agent.
#            Origin: Called by `Agent.update`.
#            Restrictions: Must have `traits.energy`, `target`, `current_behavior_state` attributes.
#   - world: The SimulationWorld instance (for sensing). Type: world.SimulationWorld.
#            Origin: Passed from `Agent.update`.
#            Restrictions: Provides access to world data (like `world.food`).
# Where Inputs Typically Come From: Called by `Agent.update()` during each tick before executing state logic.
# Restrictions on Inputs: None.
# Other Relevant Info: Returns the state string the agent should be in for the *next* execution. Does NOT change `agent.current_behavior_state` directly (that's done in `Agent.update`).
#
# Description of Algorithm/Process:
# 1. Get the agent's current state: `current_state = agent.current_behavior_state`.
# 2. Based on the `current_state`, apply transition rules:
#    a. If `current_state` is `AgentState.WANDERING`:
#       i. Check if energy is below the food-seeking threshold (e.g., < 30.0).
#       ii. If energy is low, call `find_nearest_food(agent, world.food)`.
#       iii. If food is found, return `AgentState.SEEKING_FOOD`.
#       iv. If energy is low but no food is found, *or* energy is not low, remain in `AgentState.WANDERING`. Return `AgentState.WANDERING`.
#    b. If `current_state` is `AgentState.SEEKING_FOOD`:
#       i. Check if energy is high enough that food is no longer a priority (e.g., >= 50.0, initial max). If so, return `AgentState.WANDERING`.
#       ii. Check if the agent still has a `target` AND if that target is still valid/edible (e.g., `agent.target in world.food`). This implicitly covers cases where food was eaten by another agent or expired.
#       iii. If the agent has a valid food target, remain in `AgentState.SEEKING_FOOD`. Return `AgentState.SEEKING_FOOD`.
#       iv. If energy is still low but the agent's current target is no longer valid (cleared or eaten), call `find_nearest_food(agent, world.food)` again to see if a *new* food target is in range.
#       v. If a new food target is found, set `agent.target` to the new food and remain in `AgentState.SEEKING_FOOD`. Return `AgentState.SEEKING_FOOD`.
#       vi. If energy is low but *no* food (current or new) is found in vision, transition back to `AgentState.WANDERING` and clear the agent's target: `agent.target = None`. Return `AgentState.WANDERING`.
#    c. (Future) Add rules for other states (e.g., transition to `FLEEING_PREDATOR` if a predator is sensed while seeking food or wandering).
# 3. If the current state doesn't have specific transition rules that are met, default to returning the `current_state` (stay in the same state).
#
# Description of Output:
# A string representing the next behavior state for the agent. Type: str.
# Output Range: One of the constants defined in `AgentState`.

# 4. Function: execute_current_state
# Description:
# Executes the per-tick actions specific to the agent's current behavior state.
# This function dispatches the execution logic based on `agent.current_behavior_state`.
# This is where movement timing, calling `move_agent`, and applying energy costs
# associated with movement happen, but only for states where movement is active.
# Inputs:
#   - agent: The Agent instance. Type: agent.Agent.
#            Origin: Called by `Agent.update` after state transition logic.
#            Restrictions: Must have `tick_counter`, `traits.move_interval_ticks`, `target`,
#                          `direction`, `x`, `y`, `traits.energy`, `traits.energy_drain_per_move`,
#                          and `current_behavior_state` attributes.
#   - world: The SimulationWorld instance (for environment interaction like checking for reaching target). Type: world.SimulationWorld.
#            Origin: Passed from `Agent.update`.
#            Restrictions: Potentially needed to check if agent is on target cell, etc.
# Where Inputs Typically Come From: Called by `Agent.update()` during each tick after state transition.
# Restrictions on Inputs: None.
# Other Relevant Info: Manages movement timing. Calls `move_towards_target` or `get_random_direction`/sets direction based on state. Calls `move_agent`. Applies energy costs. Checks for energy death.
#
# Description of Algorithm/Process:
# 1. Check the value of `agent.current_behavior_state`.
# 2. --- Logic for AgentState.WANDERING ---
#    a. If the state is `AgentState.WANDERING`:
#       i. Increment the movement timer: `agent.tick_counter += 1`.
#       ii. Check if it's time to move: `if agent.tick_counter >= agent.traits.move_interval_ticks:`.
#       iii. If it's time to move:
#           - Reset `agent.tick_counter` to 0.
#           - (Direction is handled by `move_agent`'s random chance if `agent.target` is None).
#           - Call `move_agent(agent)`. This function updates position and might change direction randomly if target is None.
#           - Apply energy drain per move: `agent.traits.energy -= agent.traits.energy_drain_per_move`.
#           - Check for energy death: `if agent.traits.energy <= 0: agent.alive = False`.
# 3. --- Logic for AgentState.SEEKING_FOOD ---
#    a. If the state is `AgentState.SEEKING_FOOD`:
#       i. Check if the agent still has a valid `target` (and it's food). This is important because the target might have been eaten by another agent or expired since the state transition occurred. If `agent.target is None` OR `agent.target not in world.food` (ideally check via a world method like `world.is_food_active(agent.target)`), the agent might need to transition *back* to wandering (this should primarily be handled by `get_next_state`, but a failsafe here can be useful, or simply rely on the target being None). If target is invalid, exit this state's execution.
#       ii. Increment the movement timer: `agent.tick_counter += 1`.
#       iii. Check if it's time to move: `if agent.tick_counter >= agent.traits.move_interval_ticks:`.
#       iv. If it's time to move:
#           - Reset `agent.tick_counter` to 0.
#           - Call `move_towards_target(agent)`. This updates `agent.direction`.
#           - Call `move_agent(agent)`. This applies the updated direction to position.
#           - Apply energy drain per move: `agent.traits.energy -= agent.traits.energy_drain_per_move`.
#           - Check for energy death: `if agent.traits.energy <= 0: agent.alive = False`.
#           - Check if the agent has reached its food target (same cell): `if agent.x == agent.target.x and agent.y == agent.target.y:`. If so, the `SimulationWorld` will handle the eating interaction and remove the food in its interaction phase. The agent should probably clear its target here: `agent.target = None`.
# 4. (Future) Add logic for other states (FLEEING_PREDATOR, SEEKING_MATE, REPRODUCING, IDLE). For example, FLEEING might use `move_towards_target` with a target coordinate calculated to be *away* from the predator. IDLE might just do energy drain per tick without movement.
#
# Description of Output:
# None. Side effects: updates agent's `tick_counter`, `direction`, `x`, `y`, `energy`, `alive`, and `target` based on the current state's logic.

# 5. Function: move_towards_target (Helper)
# Description:
# Adjusts the agent's `direction` attribute to point one step closer towards
# its current `target`. This is a helper function used by state execution logic
# (like the `SEEKING_FOOD` state) when the agent needs to move towards a specific point.
# Inputs:
#   - agent: The Agent instance. Type: agent.Agent.
#            Origin: Called by `execute_current_state` (e.g., when in SEEKING_FOOD state).
#            Restrictions: Must have `x`, `y`, `direction`, and a non-None `target` with `x` and `y` attributes.
# Where Inputs Typically Come From: Called by `execute_current_state`.
# Restrictions on Inputs: `agent.target` must not be `None`.
# Other Relevant Info: Modifies `agent.direction`. Uses `config.GRID_COLS` for wrap-around calculation.
#
# Description of Algorithm/Process:
# 1. Get agent and target coordinates.
# 2. Calculate raw differences `dx`, `dy`.
# 3. Adjust `dx` for horizontal wrap-around using `config.GRID_COLS`.
# 4. Decide and set `agent.direction` based on adjusted `dx` and `dy`, prioritizing the larger absolute difference unless one is zero.
#
# Description of Output:
# None. Side effect is modifying the agent's `direction`.


# --- START CODE IMPLEMENTATION ---
# Imports:
# Standard library imports first
import random
import math # Needed for distance calculations (or just arithmetic)

# Local package imports
# Import constants needed for sensing and movement calculations
from config import GRID_COLS, GRID_ROWS, BASE_ENERGY_DRAIN_PER_MOVE, BASE_ENERGY_DRAIN_PER_TICK, BASE_MAX_AGE_TICKS, BASE_VISION_RANGE
# Import movement functions used by state execution
from .movement import move_agent, get_random_direction
# Import World and FoodPellet for type hinting and access (if needed)
# from world.simulation_world import SimulationWorld
# from world.food import FoodPellet


### 1. Class: AgentState Implementation ###
# Define the possible behavior states as constants
class AgentState:
    WANDERING = "wandering"
    SEEKING_FOOD = "seeking_food"
    FLEEING_PREDATOR = "fleeing_predator" # Future
    SEEKING_MATE = "seeking_mate"     # Future
    REPRODUCING = "reproducing"       # Future
    IDLE = "idle"                     # Future


### 2. Function: find_nearest_food (Helper) Implementation ###
# Requires agent and food_list as inputs
def find_nearest_food(agent, food_list):
    """
    Searches for the closest edible food pellet within the agent's vision range.
    Returns the nearest food object or None. Considers horizontal wrap-around.
    """
    nearest_food = None
    # Use float('inf') for initial minimum distance squared
    min_dist_sq = float('inf')

    agent_x, agent_y = agent.x, agent.y
    # Get vision range from agent's traits and square it for comparison
    vision_range_sq = agent.traits.vision_range ** 2

    # Iterate through all food pellets in the world
    for pellet in food_list:
        # Check if food is edible (energy_value > 0). Also check if pellet object is valid (though world.food should only contain valid ones)
        if pellet is None or pellet.energy_value <= 0:
            continue

        pellet_x, pellet_y = pellet.x, pellet.y

        # Calculate difference in coordinates
        dx = pellet_x - agent_x
        dy = pellet_y - agent_y

        # --- Handle horizontal wrap-around for distance calculation ---
        # Check if wrapping horizontally is a shorter path
        # Only apply if the absolute difference is greater than half the grid width
        if dx > GRID_COLS // 2:
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


### 3. Function: get_next_state Implementation ###
# Requires agent and world as inputs
def get_next_state(agent, world):
    """
    Determines the agent's next behavior state based on its current state,
    traits, and the environmental context. This is the state transition logic.
    """
    current_state = agent.current_behavior_state
    next_state = current_state # Assume stay in current state unless a rule triggers transition

    # Define energy threshold for seeking food (using a constant from config, or a value based on traits)
    # Using BASE_MAX_AGE_TICKS / 2 as an example threshold for relative age
    energy_threshold_for_seeking_food = 30.0 # Or calculate based on self.traits.max_energy (if added)

    # --- State Transition Rules ---
    # Rules are checked in priority order (e.g., fleeing predators is usually highest priority)

    # Rule: Transition to SEEKING_FOOD if energy is low AND food is visible
    # This rule can apply from WANDERING or potentially other non-critical states
    if agent.traits.energy < energy_threshold_for_seeking_food:
        # Need to find food within vision to transition to SEEKING_FOOD
        # Access world.food directly for now as planned
        # FUTURE: Use world.get_food_in_range(agent.x, agent.y, agent.traits.vision_range)
        food_in_sight = find_nearest_food(agent, world.food)

        if food_in_sight:
            next_state = AgentState.SEEKING_FOOD
            # When transitioning TO seeking food, set the target
            # Note: If already seeking, decide_next_action might reset the target if the old one is gone,
            # so setting it here on transition might be redundant, but is explicit.
            if current_state != AgentState.SEEKING_FOOD:
                 agent.target = food_in_sight # Set target only on transition to this state

    # Rule: Transition out of SEEKING_FOOD if energy is sufficient OR target is gone and no new food found
    # This rule should be checked AFTER the SEEKING_FOOD entry rule, as energy might become sufficient *while* seeking
    if current_state == AgentState.SEEKING_FOOD:
        # If energy is now high enough, stop seeking food
        if agent.traits.energy >= energy_threshold_for_seeking_food:
             next_state = AgentState.WANDERING
             agent.target = None # Clear target when leaving seeking state

        # If energy is *still* low, but the current target is no longer valid/visible,
        # try finding a *new* food target. If no new food is found, transition back to wandering.
        # Check if target is still in world.food (simple check, assumes world.food is authoritative)
        # Or check if agent.target is None (cleared by eating or previous logic)
        elif agent.target is None or (agent.target not in world.food and agent.target.energy_value > 0): # Check if target is not in world.food and wasn't eaten
            # Energy is still low, but current target is gone. Look for a NEW target.
            food_in_sight_again = find_nearest_food(agent, world.food)
            if food_in_sight_again:
                 agent.target = food_in_sight_again # Set new target, stay in SEEKING_FOOD state
                 next_state = AgentState.SEEKING_FOOD # Explicitly stay in this state
            else:
                 # No food found in sight, transition back to wandering
                 next_state = AgentState.WANDERING
                 agent.target = None # Clear target

    # Rule: Default transition - If no other rule triggers, stay in the current state.
    # (This is handled implicitly by initializing next_state = current_state at the start)

    # Future Rules: Check for predators, mates, etc. and set priorities
    # e.g., if current_state is not FLEEING_PREDATOR and predator_in_sight: next_state = AgentState.FLEEING_PREDATOR

    return next_state # Return the determined next state


### 4. Function: execute_current_state Implementation ###
# Requires agent and world as inputs
def execute_current_state(agent, world):
    """
    Executes the per-tick actions corresponding to the agent's current behavior state.
    Handles movement timing, calling move functions, and applying energy costs.
    """
    state = agent.current_behavior_state

    # Logic for different states
    if state == AgentState.WANDERING:
        # --- Movement Timing (Moved from Agent.update) ---
        agent.tick_counter += 1
        # Check if it's time for the agent to move based on its speed trait
        if agent.tick_counter >= agent.traits.move_interval_ticks:
            agent.tick_counter = 0 # Reset counter

            # --- Movement Execution (Moved from Agent.update) ---
            # Direction is handled by move_agent's random chance if agent.target is None
            move_agent(agent) # Call the movement function

            # --- Energy Drain (Moved from Agent.update) ---
            # Apply energy drain per move (using trait value)
            agent.traits.energy -= agent.traits.energy_drain_per_move

            # --- Energy Death Check (Moved from Agent.update) ---
            # Check if energy level is now <= 0
            if agent.traits.energy <= 0:
                agent.alive = False
                # Optional Debug: print(f"Agent {id(agent)} died from lack of energy while wandering at tick {world.state.tick_count}.")


    elif state == AgentState.SEEKING_FOOD:
        # Check if agent still has a target. If not, maybe it should transition out (handled by get_next_state)
        # but also defensively exit execution if target somehow invalid here.
        # Check if target is still in world.food (simple check)
        if agent.target is None or (hasattr(agent.target, 'energy_value') and agent.target.energy_value <= 0):
             # Target is invalid (gone, eaten, or depleted). Get_next_state should transition out next tick,
             # but for this tick, do nothing or transition to wandering immediately?
             # Let's just do nothing for this tick, rely on get_next_state to fix next time.
             # Optional: agent.current_behavior_state = AgentState.WANDERING # Force transition? No, let get_next_state decide.
             # Optional Debug: print(f"Agent {id(agent)} in SEEKING_FOOD state but target invalid. Tick {world.state.tick_count}.")
             return # Do nothing if target is invalid

        # --- Movement Timing (Moved from Agent.update, specific to state) ---
        agent.tick_counter += 1
        # Check if it's time for the agent to move based on its speed trait
        if agent.tick_counter >= agent.traits.move_interval_ticks:
            agent.tick_counter = 0 # Reset counter

            # --- Movement Direction & Execution (Moved from Agent.update, specific to state) ---
            # Agent has a target, so calculate direction towards it using helper
            move_towards_target(agent) # Updates agent.direction

            # Call the movement function
            move_agent(agent) # Applies the updated direction to position

            # --- Energy Drain (Moved from Agent.update, specific to state) ---
            # Apply energy drain per move (using trait value)
            agent.traits.energy -= agent.traits.energy_drain_per_move

            # --- Energy Death Check (Moved from Agent.update, specific to state) ---
            # Check if energy level is now <= 0
            if agent.traits.energy <= 0:
                agent.alive = False
                # Optional Debug: print(f"Agent {id(agent)} died from lack of energy while seeking food at tick {world.state.tick_count}.")
                return # Agent died

            # --- Check if Target Reached ---
            # If agent reached the target food cell
            if agent.target is not None and agent.x == agent.target.x and agent.y == agent.target.y:
                 # The eating logic is handled by world._handle_agent_food_interaction
                 # which happens after agent updates. That logic also sets food.energy_value = 0.
                 # Clear the agent's target immediately to signal goal reached.
                 agent.target = None
                 # The agent will likely transition to WANDERING in the next tick's get_next_state call
                 # due to target being None or energy being high enough after eating.
                 # Optional Debug: print(f"Agent {id(agent)} reached food target at ({agent.x},{agent.y}) at tick {world.state.tick_count}. Clearing target.")


    # --- Future State Logic Placeholders ---
    elif state == AgentState.FLEEING_PREDATOR:
        pass # Implement fleeing logic
    elif state == AgentState.SEEKING_MATE:
        pass # Implement seeking mate logic
    elif state == AgentState.REPRODUCING:
        pass # Implement reproduction logic (might not move)
    elif state == AgentState.IDLE:
        pass # Implement idle logic (maybe just passive energy drain)

    # Optional: Passive Energy drain per tick (if implemented and not handled per-state)
    # If this drain applies regardless of state or movement, it could be here.
    # However, it might be more state-specific (e.g., IDLE drains less, REPRODUCING drains more).
    # Consider implementing it within each state's logic above if state-dependent,
    # or in Agent.update if truly universal. Let's assume state-dependent for now
    # and keep it out of this general dispatcher.


### 5. Function: move_towards_target (Helper) Implementation ###
# Requires agent as input (it has agent.target)
# This is a helper function called by execute_current_state for states that need to move towards a target
def move_towards_target(agent):
     """
     Adjusts the agent's direction to move one step closer towards its current target.
     Assumes agent.target is not None and valid.
     """
     # Import necessary constants locally for calculations if needed
     from config import GRID_COLS

     # Defensive check, although execute_current_state should only call this if target exists
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
     if dx > GRID_COLS // 2:
         dx -= GRID_COLS
     elif dx < -GRID_COLS // 2:
         dx += GRID_COLS

     # Decide direction based on adjusted dx and dy
     # Prioritize the axis with the largest difference, unless one axis difference is zero (already aligned)
     # This logic ensures the agent moves primarily horizontally or vertically towards the target.
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
     # Direction doesn't need to change for movement.


# --- END CODE IMPLEMENTATION ---