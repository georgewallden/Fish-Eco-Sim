# agent/behavior.py
#
# Description:
# This module implements the agent's behavior state machine and the logic
# for each behavioral state. It defines the possible states an agent can
# be in, and provides functions for determining state transitions (now driven
# by the agent's neural network) and executing the actions associated with
# the current state. This module integrates sensing (using world data via
# agent/world methods), decision-making (via the neural network), and
# driving the movement logic from `agent.movement`.
#
# Key responsibilities of this file:
# - Define the set of possible behavior states.
# - Implement helper functions for sensing the environment and creating the
#   observation vector for the neural network.
# - Implement the logic for deciding state transitions by feeding the observation
#   into the agent's neural network and interpreting the output.
# - Implement the actions that an agent performs while in a specific state,
#   including movement timing, executing movement, and applying energy costs
#   associated with state actions.
# - Provide helper functions for common behavioral tasks like finding targets
#   and determining movement towards a target.
#
# Design Philosophy/Notes:
# - Implements the State Machine pattern for agent behavior.
# - The `get_next_state` function is the interface where the neural network's
#   decision replaces hardcoded transition rules.
# - The `execute_current_state` function dispatches to state-specific action logic.
# - Relies on agent state, traits, and network (passed via the `agent` object).
# - Requires access to the `SimulationWorld` instance for sensing and potential
#   interaction (ideally via world methods).
# - The observation space and interpretation of network output are defined here.

# Imports Description:
# This section lists the modules imported by agent/behavior.py and their purpose.
# - random: Standard library, potentially needed for random components in behavior (e.g., random wandering direction if not handled by movement, or random decision tie-breaking).
# - math: Standard library, used for distance calculations.
# - numpy: Standard library for numerical operations, especially creating the observation vector.
# - config: Imports constants needed for sensing calculations (e.g., wrap-around distance), behavior thresholds, and notably the maximum energy for normalization.
# - agent.movement.move_agent: Imports the function to execute the agent's physical movement.
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
# Returns the nearest food found, or None. Horizontal wrap-around is considered.
# Inputs:
#   - agent: The Agent instance performing the search. Type: agent.Agent.
#   - food_list: A list of active FoodPellet instances. Type: list[world.food.FoodPellet].
# Where Inputs Typically Come From: Called by sensing/observation logic (`get_food_sensing_data_vector`).
# Restrictions on Inputs: None.
# Other Relevant Info: Calculates distance considering horizontal wrap-around.
#
# Description of Algorithm/Process:
# 1. Initialize `nearest_food = None` and `min_dist_sq = float('inf')`.
# 2. Get agent's position and squared vision range from `agent.traits`.
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

# 3. Function: get_food_sensing_data_vector (Helper)
# Description:
# Gathers specific numerical sensing data about food within the agent's vision
# and formats it as a NumPy array for the observation vector. For the minimal
# alpha net, this is just a binary flag indicating if food is seen.
# Inputs:
#   - agent: The Agent instance. Type: agent.Agent.
#   - world: The SimulationWorld instance (needed to access `world.food`). Type: world.SimulationWorld.
# Where Inputs Typically Come From: Called by `get_observation`.
# Restrictions on Inputs: None.
# Other Relevant Info: Calls `find_nearest_food`. The output format must match the expected portion of the network's input vector.
#
# Description of Algorithm/Process (Minimal Alpha Net):
# 1. Call `find_nearest_food(agent, world.food)`.
# 2. Check if the result is not `None` (meaning food was found).
# 3. Return a NumPy array `np.array([1.0])` if food was found, and `np.array([0.0])` if no food was found. (This provides a single binary input feature).
#
# Description of Output:
# A NumPy array representing the food sensing part of the observation vector.
# Type: numpy.ndarray. Output Range: `np.array([0.0])` or `np.array([1.0])`. Shape: `(1,)`.

# 4. Function: get_observation
# Description:
# Compiles all relevant information about the agent's internal state and its
# sensed environment into a single numerical vector (NumPy array) that serves
# as the input to the agent's neural network.
# Inputs:
#   - agent: The Agent instance. Type: agent.Agent.
#            Restrictions: Must have `traits.energy`, `traits.max_energy`.
#   - world: The SimulationWorld instance. Type: world.SimulationWorld.
#            Restrictions: Provides access to global data needed for sensing.
# Where Inputs Typically Come From: Called by `get_next_state`.
# Restrictions on Inputs: None.
# Other Relevant Info: Defines the structure and content of the neural network's input. Calls sensing helper functions.
#
# Description of Algorithm/Process (Minimal Alpha Net):
# 1. Get the agent's normalized energy: `normalized_energy = agent.traits.energy / agent.traits.max_energy`.
# 2. Call `get_food_sensing_data_vector(agent, world)` to get the food sensing part of the observation.
# 3. Combine the normalized energy and the food sensing vector into a single NumPy array.
#    - Create an array for internal state: `internal_state_vector = np.array([normalized_energy])`.
#    - Get the sensing vector: `sensing_vector = get_food_sensing_data_vector(agent, world)`.
#    - Concatenate them: `observation_vector = np.concatenate([internal_state_vector, sensing_vector])`.
# 4. Return the combined observation vector.
#
# Description of Output:
# A NumPy array representing the agent's observation. Type: numpy.ndarray.
# Output Range: Values typically between 0 and 1 (if normalized correctly). Shape: `(input_size,)` (e.g., `(2,)` for minimal net).

# 5. Function: get_next_state
# Description:
# Determines the agent's next behavior state by processing its observation
# through its neural network and interpreting the network's output.
# Inputs:
#   - agent: The Agent instance. Type: agent.Agent.
#            Restrictions: Must have `network` and `current_behavior_state` attributes.
#   - world: The SimulationWorld instance. Type: world.SimulationWorld.
#            Restrictions: Passed to `get_observation`.
# Where Inputs Typically Come From: Called by `Agent.update`.
# Restrictions on Inputs: `agent` must have a `network` attribute.
# Other Relevant Info: This is the core network integration point for state transitions.
#
# Description of Algorithm/Process (Minimal Alpha Net - Binary Output):
# 1. Get the agent's observation vector by calling `get_observation(agent, world)`.
# 2. Feed the observation into the agent's neural network: `network_output = agent.network.forward(observation)`.
# 3. Interpret the network's output (a single value between 0 and 1 due to sigmoid):
#    a. Define a threshold (e.g., 0.5).
#    b. If `network_output` (specifically, the single value in the output array `network_output[0, 0]`) is greater than the threshold:
#       i. The network is signaling to seek food. Set `next_state = AgentState.SEEKING_FOOD`.
#       ii. (Crucial for SEEKING_FOOD state) Find and set the `agent.target` if not already set or invalid. This needs to find the *nearest* food again, as the observation just said *if* food is seen, not *which* one. Call `find_nearest_food(agent, world.food)` and set `agent.target = found_food`. Handle the case where network wants to seek but no food is *actually* visible (agent might still transition but won't find a target). Let's refine: only transition to SEEKING_FOOD if network output > threshold *and* food is currently visible.
#    c. Else (`network_output <= threshold`):
#       i. The network is signaling to wander. Set `next_state = AgentState.WANDERING`.
#       ii. When transitioning *to* wandering, clear the agent's target: `agent.target = None`.
# 4. Return the determined `next_state`.
#
# Description of Output:
# A string representing the next behavior state. Type: str.
# Output Range: `AgentState.WANDERING` or `AgentState.SEEKING_FOOD` (for alpha net).

# 6. Function: execute_current_state
# Description:
# Executes the per-tick actions specific to the agent's current behavior state.
# This function dispatches the execution logic based on `agent.current_behavior_state`.
# This is where movement timing, calling `move_agent`, and applying energy costs
# associated with movement happen, but only for states where movement is active.
# Inputs:
#   - agent: The Agent instance. Type: agent.Agent.
#   - world: The SimulationWorld instance (for environment interaction like checking for reaching target). Type: world.SimulationWorld.
# Where Inputs Typically Come From: Called by `Agent.update()` during each tick after state transition.
# Restrictions on Inputs: None.
# Other Relevant Info: Manages movement timing. Calls `move_towards_target` or `get_random_direction`/sets direction based on state. Calls `move_agent`. Applies energy costs. Checks for energy death.
#
# Description of Algorithm/Process:
# 1. Check the value of `agent.current_behavior_state`.
# 2. --- Logic for AgentState.WANDERING ---
#    a. If the state is `AgentState.WANDERING`:
#       i. Increment movement timer.
#       ii. Check if time to move (`tick_counter >= interval`).
#       iii. If time to move:
#           - Reset `tick_counter`.
#           - Call `move_agent(agent)`. (Random direction change if no target is handled inside `move_agent` now).
#           - Apply energy drain per move (`agent.traits.energy_drain_per_move`).
#           - Check for energy death.
# 3. --- Logic for AgentState.SEEKING_FOOD ---
#    a. If the state is `AgentState.SEEKING_FOOD`:
#       i. Check if agent still has a valid food target (target is not None AND it's still in `world.food` or similar check). If target invalid, agent *should* transition state next tick via `get_next_state`, but for this tick, do nothing or revert to wandering? Let's rely on `get_next_state` to manage target validity and state transition. If target is None here, likely a bug or temporary state, just return.
#       ii. Increment movement timer.
#       iii. Check if time to move (`tick_counter >= interval`).
#       iv. If time to move:
#           - Reset `tick_counter`.
#           - Call `move_towards_target(agent)`. This updates `agent.direction`.
#           - Call `move_agent(agent)`. This applies position change.
#           - Apply energy drain per move (`agent.traits.energy_drain_per_move`).
#           - Check for energy death.
#           - Check if agent reached food target (same cell). If so, `SimulationWorld` handles eating, clear `agent.target`.
# 4. (Future) Add logic for other states.
#
# Description of Output:
# None. Side effects: updates agent's `tick_counter`, `direction`, `x`, `y`, `energy`, `alive`, and `target` based on the current state's logic.

# 7. Function: move_towards_target (Helper)
# Description:
# Adjusts the agent's `direction` attribute to point one step closer towards
# its current `target`. Used by state execution logic that involves target following.
# Inputs:
#   - agent: The Agent instance. Type: agent.Agent.
#   - target_x: The target's grid column index. Type: int.
#   - target_y: The target's grid row index. Type: int.
# Where Inputs Typically Come From: Called by `execute_current_state` (e.g., when in SEEKING_FOOD state). Uses `agent.target.x` and `agent.target.y`.
# Restrictions on Inputs: Target coordinates should be valid grid coordinates.
# Other Relevant Info: Modifies `agent.direction`. Uses `config.GRID_COLS` for wrap-around calculation.
#
# Description of Algorithm/Process:
# 1. Get agent coordinates.
# 2. Calculate raw differences `dx`, `dy` between agent and target coordinates.
# 3. Adjust `dx` for horizontal wrap-around using `config.GRID_COLS`.
# 4. Decide and set `agent.direction` ("N", "S", "E", "W") based on adjusted `dx` and `dy`, prioritizing the axis with the larger absolute difference unless one is zero.
#
# Description of Output:
# None. Side effect is modifying the agent's `direction`.


# --- START CODE IMPLEMENTATION ---
# Imports:
# Standard library imports first
import random
import math # Needed for distance calculations (or just arithmetic)
import numpy as np # Needed for observation vector

# Local package imports
# Import constants needed for sensing and movement calculations
from config import GRID_COLS, GRID_ROWS, BASE_ENERGY_DRAIN_PER_MOVE, BASE_ENERGY_DRAIN_PER_TICK, BASE_MAX_ENERGY
# Import movement functions used by state execution
from .movement import move_agent, get_random_direction
# Import World and FoodPellet for type hinting and access (if needed)
# from world.simulation_world import SimulationWorld
# from world.food import FoodPellet
# Import NeuralNetwork only if needed for type hinting or accessing its structure from behavior.py
# from .neural_net import NeuralNetwork


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
# This function is a helper called by sensing/observation logic
def find_nearest_food(agent, food_list):
    """
    Searches for the closest edible food pellet within the agent's vision range.
    Returns the nearest food object or None. Considers horizontal wrap-around.
    """
    nearest_food = None
    min_dist_sq = float('inf')

    agent_x, agent_y = agent.x, agent.y
    vision_range_sq = agent.traits.vision_range ** 2

    # Iterate through all food pellets in the world
    for pellet in food_list:
        # Check if food is edible (energy_value > 0) and a valid object
        if pellet is None or not hasattr(pellet, 'energy_value') or pellet.energy_value <= 0:
             continue # Skip invalid or eaten food

        pellet_x, pellet_y = pellet.x, pellet.y

        # Calculate difference in coordinates
        dx = pellet_x - agent_x
        dy = pellet_y - agent_y

        # Handle horizontal wrap-around for distance calculation
        if dx > GRID_COLS // 2:
            dx -= GRID_COLS
        elif dx < -GRID_COLS // 2:
            dx += GRID_COLS

        # Calculate squared Euclidean distance
        dist_sq = dx**2 + dy**2

        # Check if within vision range and closer than current nearest
        if dist_sq <= vision_range_sq and dist_sq < min_dist_sq:
            min_dist_sq = dist_sq
            nearest_food = pellet

    return nearest_food # Return the nearest food object found, or None

### 3. Function: get_food_sensing_data_vector (Helper) Implementation ###
# Requires agent and world as inputs
# This function is a helper called by get_observation
def get_food_sensing_data_vector(agent, world):
    """
    Gathers specific numerical sensing data about food within the agent's vision
    and formats it as a NumPy array for the observation vector.
    Minimal alpha net: [sees_food_flag].
    """
    # Call find_nearest_food to see if any food is visible
    # Access world.food directly for now as planned
    # FUTURE: Use world.get_food_in_range(agent.x, agent.y, agent.traits.vision_range)
    food_in_sight = find_nearest_food(agent, world.food)

    # For the minimal alpha net, just return a flag: 1.0 if food is seen, 0.0 otherwise
    sees_food_flag = 1.0 if food_in_sight is not None else 0.0

    # Optional: Add relative direction/distance if needed for more complex nets later
    # if food_in_sight:
    #     dx = food_in_sight.x - agent.x
    #     dy = food_in_sight.y - agent.y
    #     if dx > GRID_COLS // 2: dx -= GRID_COLS
    #     elif dx < -GRID_COLS // 2: dx += GRID_COLS
    #     distance = math.sqrt(dx**2 + dy**2) # Using actual distance now if needed
    #     return np.array([sees_food_flag, dx, dy, distance]) # Example extended vector
    # else:
    #      return np.array([sees_food_flag, 0.0, 0.0, 0.0]) # Return zeros if no food seen


    return np.array([sees_food_flag]) # Return the minimal vector


### 4. Function: get_observation Implementation ###
# Requires agent and world as inputs
# This function is called by get_next_state
def get_observation(agent, world):
    """
    Compiles all relevant information (internal state + sensing) into a single
    numerical observation vector (NumPy array) for the neural network.
    Minimal alpha net observation: [normalized_energy, sees_food_flag].
    """
    # Internal State: Normalized Energy
    # Use the max_energy trait for normalization
    normalized_energy = agent.traits.energy / agent.traits.max_energy if agent.traits.max_energy > 0 else 0.0
    internal_state_vector = np.array([normalized_energy])

    # Sensed Environment: Food Information
    sensing_vector = get_food_sensing_data_vector(agent, world)

    # Combine vectors
    observation_vector = np.concatenate([internal_state_vector, sensing_vector])

    return observation_vector


### 5. Function: get_next_state Implementation ###
# Requires agent and world as inputs
# This function is called by Agent.update to determine state transition
def get_next_state(agent, world):
    """
    Determines the agent's next behavior state by processing its observation
    through its neural network and interpreting the output.
    """
    # Get the current observation vector
    observation = get_observation(agent, world)

    # Feed the observation into the agent's neural network
    # The network returns a numpy array, e.g., [[output_value]]
    network_output = agent.network.forward(observation)

    # Interpret the network's output (a single value between 0 and 1)
    # Let's use a threshold (e.g., 0.5) to decide between Wandering and Seeking
    decision_threshold = 0.5
    network_decision_value = network_output[0, 0] # Get the scalar value from the output array

    # Default next state is to stay in current state, but we'll override based on network
    next_state = agent.current_behavior_state

    # --- Network Output Interpretation / State Transition Logic ---
    # If the network output is above the threshold AND food is actually visible,
    # transition to SEEKING_FOOD. Otherwise, transition/stay in WANDERING.

    # Re-check if food is visible - crucial! The network output is based on the observation,
    # but we should only transition to SEEKING_FOOD if there is *actually* a target to seek.
    # Access world.food directly for this check as planned.
    # FUTURE: Use world.get_food_in_range()
    food_is_currently_visible = find_nearest_food(agent, world.food) is not None

    if network_decision_value > decision_threshold and food_is_currently_visible:
        next_state = AgentState.SEEKING_FOOD
        # When transitioning TO seeking food, find and set the target.
        # find_nearest_food is called again here because the observation only said *if* food is seen, not *which* one.
        agent.target = find_nearest_food(agent, world.food)
        # Optional Debug: if agent.current_behavior_state != next_state: print(f"Agent {id(agent)} Network decides SEEKING_FOOD at tick {world.state.tick_count}. Output: {network_decision_value:.2f}. Energy: {agent.traits.energy:.1f}. Target: ({agent.target.x},{agent.target.y})")

    else:
        # Network output <= threshold OR no food visible, transition/stay in WANDERING
        next_state = AgentState.WANDERING
        # When transitioning TO wandering, clear the target
        if agent.current_behavior_state != AgentState.WANDERING:
            agent.target = None
            # Optional Debug: print(f"Agent {id(agent)} Network decides WANDERING at tick {world.state.tick_count}. Output: {network_decision_value:.2f}. Energy: {agent.traits.energy:.1f}.")

    # Return the determined next state
    return next_state


### 6. Function: execute_current_state Implementation ###
# Requires agent and world as inputs
# This function is called by Agent.update after state transition
def execute_current_state(agent, world):
    """
    Executes the per-tick actions corresponding to the agent's current behavior state.
    Handles movement timing, calling move functions, and applying energy costs.
    """
    state = agent.current_behavior_state

    # Logic for different states
    if state == AgentState.WANDERING:
        # --- Movement Timing ---
        agent.tick_counter += 1
        # Check if it's time for the agent to move based on its speed trait
        if agent.tick_counter >= agent.traits.move_interval_ticks:
            agent.tick_counter = 0 # Reset counter

            # --- Movement Execution ---
            # Direction is handled by move_agent's random chance if agent.target is None
            move_agent(agent) # Call the movement function from agent.movement

            # --- Energy Drain per Move ---
            # Apply energy drain per move (using trait value from AgentTraits)
            agent.traits.energy -= agent.traits.energy_drain_per_move

            # --- Energy Death Check ---
            # Check if energy level is now <= 0
            if agent.traits.energy <= 0:
                agent.alive = False
                # Optional Debug: print(f"Agent {id(agent)} died from lack of energy while wandering at tick {world.state.tick_count}.")
                return # Agent died, stop execution for this tick


    elif state == AgentState.SEEKING_FOOD:
        # Check if agent still has a target. If not, it should transition out next tick.
        # If target is None here, do nothing for this tick.
        # Check if target is still in world.food (simple check) and edible
        target_is_still_valid = agent.target is not None and hasattr(agent.target, 'energy_value') and agent.target.energy_value > 0 and agent.target in world.food # Check if it's still in the world's active list
        if not target_is_still_valid:
             # Target became invalid since get_next_state decided. Rely on get_next_state
             # to transition out next tick. For now, just stop trying to move.
             # Optional Debug: print(f"Agent {id(agent)} in SEEKING_FOOD state but target became invalid. Tick {world.state.tick_count}.")
             agent.target = None # Ensure target is None if invalid
             return # Do nothing for this tick if target is invalid


        # --- Movement Timing ---
        agent.tick_counter += 1
        # Check if it's time for the agent to move based on its speed trait
        if agent.tick_counter >= agent.traits.move_interval_ticks:
            agent.tick_counter = 0 # Reset counter

            # --- Movement Direction & Execution ---
            # Agent has a target, so calculate direction towards it using helper
            # Pass the target coordinates explicitly
            move_towards_target(agent, agent.target.x, agent.target.y) # Updates agent.direction

            # Call the movement function
            move_agent(agent) # Applies the updated direction to position from agent.movement

            # --- Energy Drain per Move ---
            # Apply energy drain per move (using trait value from AgentTraits)
            agent.traits.energy -= agent.traits.energy_drain_per_move

            # --- Energy Death Check ---
            # Check if energy level is now <= 0
            if agent.traits.energy <= 0:
                agent.alive = False
                # Optional Debug: print(f"Agent {id(agent)} died from lack of energy while seeking food at tick {world.state.tick_count}.")
                return # Agent died

            # --- Check if Target Reached ---
            # If agent reached the target food cell (same coordinates)
            # Eating interaction handled by world._handle_agent_food_interaction later
            if agent.target is not None and agent.x == agent.target.x and agent.y == agent.target.y:
                 # The eating logic in world._handle_agent_food_interaction will set food.energy_value = 0.
                 # Clear the agent's target immediately in its state execution to signal goal reached.
                 # The state transition logic (get_next_state) will handle moving out of SEEKING_FOOD next tick.
                 agent.target = None
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

    # Note: Passive Energy drain per tick (`agent.traits.energy_drain_per_tick`) could be
    # implemented here within relevant states (e.g., always drains except maybe while eating?)
    # or handled in Agent.update if it's truly universal. Let's keep it out of here for now
    # unless a state specifically implies different passive drain (like IDLE).


### 7. Function: move_towards_target (Helper) Implementation ###
# Requires agent and target coordinates as inputs
# This is a helper function called by execute_current_state for states that need to move towards a target
def move_towards_target(agent, target_x, target_y):
     """
     Adjusts the agent's direction to move one step closer towards the given target coordinates.
     """
     # Import necessary constants locally for calculations if needed
     from config import GRID_COLS

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