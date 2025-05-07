# agent/base.py
#
# Description:
# This file defines the core `Agent` class, which represents an individual
# fish-like entity in the simulation. It encapsulates the agent's fundamental
# state (position, direction, traits, alive status, target) and orchestrates
# its actions during a simulation tick. It delegates specific functionalities
# like movement mechanics, rendering, and complex decision-making (behavior)
# to other modules within the 'agent' package.
#
# Key responsibilities of this file:
# - Define the `Agent` class structure.
# - Hold the state of an individual agent.
# - Manage the agent's lifecycle within a simulation tick (aging, energy drain, death).
# - Trigger movement based on an internal timer.
# - Delegate sensing, decision-making, and movement direction logic to the `behavior` module.
# - Delegate position updates to the `movement` module.
# - Delegate visual representation to the `render` module.
# - Handle consumption of food.
#
# Design Philosophy/Notes:
# - Acts as the primary representation of an individual entity.
# - Follows a compositional pattern, using instances of `AgentTraits` and calling
#   functions from `agent.movement`, `agent.render`, and `agent.behavior`.
# - The `update` method is the central method for the agent's actions each tick.
# - Includes a `target` attribute to support goal-directed behavior.
# - Accepts the `SimulationWorld` instance in its `update` method to enable
#   sensing the environment via dedicated world methods (reducing direct coupling to world internals).

# Imports Description:
# This section lists the modules imported by agent/base.py and their purpose.
# - random: Standard library, used for initial random direction generation.
# - .traits.AgentTraits: Imports the class that holds the agent's characteristics and stats.
# - .movement.move_agent: Imports the function that applies movement based on direction and handles boundaries.
# - .movement.get_random_direction: Imports the helper function for getting initial/random directions.
# - .render.draw_agent: Imports the function for drawing the agent's visual representation.
# - . import behavior: Imports the `agent.behavior` module as a whole to access its decision-making and target-based movement functions. This import is needed to delegate decision-making and target-based movement direction.
# - config: (Implicitly used by imported modules, not directly needed in current `base.py` methods, but good to list if any constants were used here). For consistency, we can mention if any config values were directly used here. (Currently none are used directly in base.py methods).

# Code Block Descriptions:
# This section provides detailed blueprints for the code blocks (class and methods)
# implemented below.

# 1. Class: Agent
# Description:
# Represents a single active entity in the simulation. An agent exists at a specific
# grid location, has a direction, a set of traits defining its abilities and state,
# and manages its own lifecycle events like aging, energy levels, and movement timing.
# It can also track a target for goal-oriented behavior.
#
# Attributes:
# - x (int): The agent's current grid column index.
# - y (int): The agent's current grid row index.
# - direction (str): The agent's current cardinal direction ("N", "S", "E", "W").
# - traits (AgentTraits): An instance of the AgentTraits class holding the agent's stats and properties.
# - tick_counter (int): Counter used to track ticks for determining when the agent should move based on its speed trait (`traits.move_interval_ticks`).
# - alive (bool): True if the agent is currently alive, False if dead (due to age or energy).
# - target (object or None): A reference to an object (like a FoodPellet or another Agent) that the agent is currently trying to move towards. None if the agent has no target.
#
# Primary Role: Represent an individual simulation participant and manage its per-tick actions based on state, traits, and environment (via behavior module).

# 1.1 Method: __init__
# Description:
# Constructor for the Agent class. Initializes a new agent instance at a given
# grid position with default traits and state. Sets an initial random direction
# and initializes internal counters and state flags.
# Inputs:
#   - self: The instance being initialized.
#   - x: The initial grid column index for the agent. Type: int.
#        Origin: Passed by `SimulationWorld` during spawning.
#        Restrictions: 0 <= x < GRID_COLS (caller's responsibility).
#   - y: The initial grid row index for the agent. Type: int.
#        Origin: Passed by `SimulationWorld` during spawning.
#        Restrictions: 0 <= y < GRID_ROWS (caller's responsibility).
# Where Inputs Typically Come From: Called by `SimulationWorld`'s spawning methods (`_spawn_initial_agents`, future reproduction logic).
# Restrictions on Inputs: Caller should ensure valid grid coordinates based on `config.py`.
# Other Relevant Info: Creates and assigns an instance of `AgentTraits`.
#
# Description of Algorithm/Process:
# 1. Store the provided `x` and `y` as the agent's starting position (`self.x`, `self.y`).
# 2. Get a random initial direction string by calling `get_random_direction()` from `agent.movement` and assign it to `self.direction`.
# 3. Create a new instance of `AgentTraits()` and assign it to `self.traits`. This initializes traits using default values from `config.py`.
# 4. Initialize the internal movement timer counter `self.tick_counter` to 0.
# 5. Set the initial survival status `self.alive` to `True`.
# 6. Initialize the agent's `self.target` attribute to `None`.
#
# Description of Output:
# None. Side effect is initializing the state attributes of the `self` object with starting values.

# 1.2 Method: update
# Description:
# Advances the agent's state for a single simulation tick. This is the main
# method called by the `SimulationWorld` each tick for every alive agent.
# It handles aging, checks for death (age/energy), triggers behavior/decision
# making logic, manages the movement timer, initiates movement, and applies
# energy costs. **Accepts the `world` instance to enable sensing/behavior.**
# Inputs:
#   - self: The Agent instance being updated.
#   - world: The SimulationWorld instance. Type: world.SimulationWorld.
#            Origin: Passed from `SimulationWorld.update()`.
#            Restrictions: Must be a valid SimulationWorld object (needed by behavior functions called by this method to access global state like `world.food` or call world sensing methods).
# Where Inputs Typically Come From: Called by `SimulationWorld.update()` once per simulation tick for each agent in the `world.agents` list.
# Restrictions on Inputs: None.
# Other Relevant Info: Orchestrates calls to methods/functions in other agent modules (`behavior`, `movement`). Handles agent state transitions like dying due to age or lack of energy.
#
# Description of Algorithm/Process:
# 1. Check if `self.alive` is `False`. If the agent is already dead, return immediately as dead agents do not update.
# 2. Increment the agent's age: `self.traits.age += 1`.
# 3. Check if the agent's age has reached or exceeded its maximum lifespan (`self.traits.age >= self.traits.max_age`). If so, set `self.alive` to `False` and return immediately (dies of old age).
# 4. Call the behavior function `behavior.decide_next_action(self, world)`, passing the agent instance and the world instance. This function is responsible for determining the agent's goal (like finding food) and potentially setting or clearing `self.target`.
# 5. Increment the agent's internal movement timer: `self.tick_counter += 1`.
# 6. Check if the movement timer has reached or exceeded the agent's movement speed interval (`self.tick_counter >= self.traits.move_interval_ticks`). This determines if the agent is ready to attempt a move this tick.
# 7. If it is time for the agent to move (`tick_counter >= self.traits.move_interval_ticks`):
#    a. Reset the `self.tick_counter` to 0 to start timing for the next move.
#    b. If the agent currently has a `target` (`self.target is not None`):
#       i. Call the behavior function `behavior.move_towards_target(self)`. This function calculates the direction towards `self.target` and updates the agent's `self.direction` attribute.
#       ii. (Optional/Future) Add logic here or in behavior.py to check if the agent has reached its target *before* moving, and handle the target interaction (e.g., consuming food, triggering reproduction). Clearing the target might also happen here if the target is reached.
#    c. If the agent has no `target` (`self.target is None`):
#       i. (Implicit) The `move_agent` function called next will use the agent's current direction. The current `move_agent` includes a chance for random direction change if there's no target, providing basic wandering behavior.
#    d. Call the movement function `move_agent(self)` from `agent.movement`. This function uses the agent's current `self.direction` to calculate its new grid position (`self.x`, `self.y`) and applies horizontal wrap-around and vertical clamping boundary rules.
#    e. Drain energy for the movement cost: `self.traits.energy -= self.traits.energy_drain_per_move`. **<-- FIXED LINE** Use the energy drain value stored *on the traits object*.
#    f. Check if the agent's energy level is now less than or equal to 0. If so, set `self.alive` to `False` and return immediately (dies from lack of energy).
# 8. (Optional/Future) Implement a constant energy drain per tick regardless of movement: `self.traits.energy -= self.traits.energy_drain_per_tick`. If this is implemented, check for energy death after this drain as well.
# 9. (Future): Add logic here or delegate to behavior.py for other tick-based agent processes like scanning for threats/mates (if not tied to `decide_next_action`), managing reproduction cooldowns, etc.
#
# Description of Output:
# None. This method modifies the state of the `self` agent object directly.
# Side effects include changing the agent's `age`, `alive` status, `energy`, `x`, `y`, `direction`, `tick_counter`, and `target`.

# 1.3 Method: eat
# Description:
# Allows the agent to consume a food source, increasing its energy level. This
# method is called by the `SimulationWorld` when an agent interacts with food.
# Inputs:
#   - self: The Agent instance performing the eating action.
#   - food: The FoodPellet instance being eaten. Type: world.food.FoodPellet.
#           Origin: Passed by `SimulationWorld::_handle_agent_food_interaction`.
#           Restrictions: Must be a valid `FoodPellet` object or similar structure
#           with an `energy_value` attribute that can be consumed (set to 0).
# Where Inputs Typically Come From: Called by `SimulationWorld`'s interaction handling loop (`_handle_agent_food_interaction`).
# Restrictions on Inputs: The `food` object must have an `energy_value` attribute.
# Other Relevant Info: Increases the agent's energy and effectively consumes the food's energy value by setting it to 0. The food object is removed from the world list externally by `SimulationWorld`.
#
# Description of Algorithm/Process:
# 1. Check if the input `food` object is valid (not None, though this check might be redundant if called correctly) and if its `energy_value` is greater than 0 (meaning it hasn't been eaten already this tick).
# 2. If the food is valid and edible, add `food.energy_value` to the agent's current energy level: `self.traits.energy += food.energy_value`.
# 3. Set the food object's `energy_value` to 0. This prevents it from being eaten again in the same tick and signals to the `SimulationWorld`'s removal logic that it is depleted.
# 4. (Optional): Implement logic to cap the agent's energy at a maximum value if a `max_energy` trait is added to `AgentTraits`.
# 5. (Optional): If the consumed food was the agent's current `self.target`, set `self.target` to `None` as the goal has been achieved.
#
# Description of Output:
# None. Side effects include increasing the agent's `energy` attribute and setting the input `food` object's `energy_value` to 0.

# 1.4 Method: draw
# Description:
# Instructs the rendering module to draw the agent on the provided Pygame surface.
# It acts as a simple pass-through to the dedicated drawing function in `agent.render`,
# providing the agent instance and its selection status.
# Inputs:
#   - self: The Agent instance to be drawn.
#   - surface: The pygame surface object to draw on. Type: pygame.Surface.
#              Origin: Passed from `SimulationWorld.draw()`.
#              Restrictions: Must be a valid pygame Surface.
#   - is_selected (optional): A boolean flag indicating if this agent is currently selected in the UI. Type: bool.
#                           Origin: Passed from `SimulationWorld.draw()`.
#                           Restrictions: Must be True or False. Default: False.
# Where Inputs Typically Come From: Called by `SimulationWorld.draw()`.
# Restrictions on Inputs: None.
# Other Relevant Info: Delegates the actual drawing logic entirely to `agent.render::draw_agent`.
#
# Description of Algorithm/Process:
# 1. Call the external function `draw_agent()` from the `agent.render` module.
# 2. Pass the `self` agent instance (so the renderer knows its position, state, etc.), the `surface` to draw on, and the `is_selected` boolean flag (to draw a selection indicator if needed).
#
# Description of Output:
# None. Side effect is the agent's visual representation appearing on the provided `surface` via the renderer.


# --- START CODE IMPLEMENTATION ---

# Imports:
# Standard library imports first
import random # Needed for initial random direction

# Local package imports
# Import the traits class
from .traits import AgentTraits
# Import movement logic functions
from .movement import move_agent, get_random_direction
# Import rendering logic function
from .render import draw_agent
# Import the behavior module (contains decision-making, sensing, target movement)
from . import behavior

# No direct imports from config needed here, traits and movement handle it


### 1. Class: Agent Implementation ###
class Agent:
    ### 1.1 Method: __init__ Implementation ###
    def __init__(self, x, y):
        """
        Initializes a new agent at a given grid position.
        """
        # Position
        self.x = x
        self.y = y

        # Use helper from movement module for initial random direction
        self.direction = get_random_direction()

        # Assign initial traits (from AgentTraits class, which uses config)
        self.traits = AgentTraits()

        # Internal state
        self.tick_counter = 0       # Counter to track ticks for move interval
        self.alive = True           # Agent's survival status

        # Field to store the agent's current target for goal-directed movement
        self.target = None # Can hold reference to FoodPellet, another Agent, etc.


    ### 1.2 Method: update Implementation ###
    # Add 'world' as an input parameter here as planned for sensing/behavior
    def update(self, world):
        """
        Updates the agent's state for a single simulation tick.
        Handles aging, energy drain, behavior timing, and movement.
        Requires the world instance for sensing.
        """
        if not self.alive:
            return # Dead agents don't update

        # Age the agent
        self.traits.age += 1
        # Check for old age death
        if self.traits.age >= self.traits.max_age:
            self.alive = False
            # Optional Debug: print(f"Agent {id(self)} died of old age at tick {world.state.tick_count}.")
            return # Agent dies of old age

        # --- Behavior/Decision Making ---
        # Call behavior logic to decide action or set/clear target
        # Pass self (the agent) and world (for sensing environment)
        behavior.decide_next_action(self, world)

        # Handle movement based on interval
        self.tick_counter += 1
        if self.tick_counter >= self.traits.move_interval_ticks:
            self.tick_counter = 0 # Reset counter

            # If agent has a target, decide movement direction based on target
            # Otherwise, movement.py handles default random changes if no target
            if self.target:
                 # Update agent's direction towards target using behavior logic
                 behavior.move_towards_target(self)
                 # Optional: Check if target is reached here and clear target if needed
                 # Reaching logic might depend on target type (e.g., same cell for food)
                 # The eating logic currently happens in world, which also effectively 'removes' the food target

            # Call the movement logic function to update agent's position
            # move_agent uses the agent's current direction and applies world boundaries
            move_agent(self)

            # Energy drain happens *per move*
            # Use the energy drain value stored on the traits object.
            self.traits.energy -= self.traits.energy_drain_per_move # <-- FIXED LINE

            # Check energy level after paying movement cost
            if self.traits.energy <= 0:
                self.alive = False
                # Optional Debug: print(f"Agent {id(self)} died from lack of energy at tick {world.state.tick_count}.")
                return # Agent dies from lack of energy

        # Optional: Energy drain per tick (if implemented in AgentTraits and config)
        # if self.traits.energy_drain_per_tick > 0: # Check if this drain is active via traits
        #     self.traits.energy -= self.traits.energy_drain_per_tick
        #     if self.traits.energy <= 0:
        #         self.alive = False
        #         # Optional Debug: print(f"Agent {id(self)} died from lack of passive energy at tick {world.state.tick_count}.")
        #         return


    ### 1.3 Method: eat Implementation ###
    def eat(self, food):
        """
        Allows the agent to consume a food source.
        Increases energy. Called by SimulationWorld.
        """
        # Ensure food still exists and has energy before consuming
        if food and food.energy_value > 0:
            self.traits.energy += food.energy_value
            food.energy_value = 0 # Food is consumed/depleted (will be removed by world logic)

            # Optional: Cap energy at a maximum if max_energy trait exists
            # if hasattr(self.traits, 'max_energy') and self.traits.max_energy is not None: # Example check
            #    self.traits.energy = min(self.traits.energy, self.traits.max_energy)

            # Optional: If the eaten food was the agent's target, clear the target
            # This helps the agent stop trying to move towards eaten food immediately
            if self.target == food:
               self.target = None
               # Optional Debug: print(f"Agent {id(self)} ate food at ({food.x},{food.y}) and cleared target.")


    ### 1.4 Method: draw Implementation ###
    def draw(self, surface, is_selected=False):
        """
        Draws the agent on the given pygame surface.
        Calls the separate rendering function.
        """
        # Call the rendering function from agent.render, passing this agent instance and selection status
        draw_agent(self, surface, is_selected)


# --- END CODE IMPLEMENTATION ---