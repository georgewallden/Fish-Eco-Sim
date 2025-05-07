# agent/base.py
#
# Description:
# This file defines the core `Agent` class, which represents an individual
# fish-like entity in the simulation. It encapsulates the agent's fundamental
# state (position, direction, traits, alive status, target, **behavior state**)
# and orchestrates its actions during a simulation tick. It delegates specific
# functionalities like movement mechanics, rendering, and complex decision-making
# (behavior, including state management) to other modules within the 'agent' package.
#
# Key responsibilities of this file:
# - Define the `Agent` class structure.
# - Hold the state of an individual agent.
# - Manage the agent's lifecycle within a simulation tick (aging, energy drain, death).
# - Trigger movement based on an internal timer.
# - Delegate behavior logic, **including state transitions and state execution**, to the `behavior` module.
# - Delegate position updates to the `movement` module.
# - Delegate visual representation to the `render` module.
# - Handle consumption of food.
#
# Design Philosophy/Notes:
# - Acts as the primary representation of an individual entity.
# - Follows a compositional pattern, using instances of `AgentTraits` and calling
#   functions from `agent.movement`, `agent.render`, and `agent.behavior`.
# - The `update` method is the central method for the agent's actions each tick.
# - Includes a `target` attribute to support goal-directed movement *within* certain behaviors.
# - Includes a `current_behavior_state` attribute to integrate the State Machine pattern.
# - Accepts the `SimulationWorld` instance in its `update` method to enable
#   sensing the environment via dedicated world methods (reducing direct coupling to world internals).

# Imports Description:
# This section lists the modules imported by agent/base.py and their purpose.
# - random: Standard library, used for initial random direction generation.
# - .traits.AgentTraits: Imports the class that holds the agent's characteristics and stats.
# - .movement.move_agent: Imports the function that applies movement based on direction and handles boundaries.
# - .movement.get_random_direction: Imports the helper function for getting initial/random directions.
# - .render.draw_agent: Imports the function for drawing the agent's visual representation.
# - . import behavior: Imports the `agent.behavior` module as a whole to access its state transition and execution functions.
# - behavior.AgentState: (Planned import from behavior) Imports the constants defining the possible behavior states.

# Code Block Descriptions:
# This section provides detailed blueprints for the code blocks (class and methods)
# implemented below.

# 1. Class: Agent
# Description:
# Represents a single active entity in the simulation. An agent exists at a specific
# grid location, has a direction, a set of traits defining its abilities and state,
# manages its lifecycle, tracks a target, and operates within a specific behavioral state.
#
# Attributes:
# - x (int): The agent's current grid column index.
# - y (int): The agent's current grid row index.
# - direction (str): The agent's current cardinal direction ("N", "S", "E", "W").
# - traits (AgentTraits): An instance of the AgentTraits class holding the agent's stats and properties.
# - tick_counter (int): Counter used to track ticks for determining when the agent should move based on its speed trait.
# - alive (bool): True if the agent is currently alive, False if dead.
# - target (object or None): A reference to an object the agent is currently moving towards.
# - current_behavior_state (str): The current state of the agent's behavior state machine (e.g., 'WANDERING', 'SEEKING_FOOD'). Initialized to a default state. (New attribute for State Machine).
#
# Primary Role: Represent an individual simulation participant and manage its per-tick actions based on state, traits, environment, and current behavior state.

# 1.1 Method: __init__
# Description:
# Constructor for the Agent class. Initializes a new agent instance at a given
# grid position with default traits and state. Sets an initial random direction,
# initializes internal counters/flags, sets the initial target to None, and
# sets the initial behavior state to the default wandering state.
# Inputs:
#   - self: The instance being initialized.
#   - x: The initial grid column index. Type: int.
#   - y: The initial grid row index. Type: int.
# Where Inputs Typically Come From: Called by `SimulationWorld` during spawning.
# Restrictions on Inputs: Caller should ensure valid grid coordinates.
# Other Relevant Info: Creates and assigns an `AgentTraits` instance. Sets the default behavior state.
#
# Description of Algorithm/Process:
# 1. Store `x` and `y` position.
# 2. Set initial random `direction`.
# 3. Create and assign `AgentTraits` instance to `self.traits`.
# 4. Initialize `self.tick_counter` to 0.
# 5. Set `self.alive` to `True`.
# 6. Initialize `self.target` to `None`.
# 7. Set `self.current_behavior_state` to the default wandering state constant (e.g., `behavior.AgentState.WANDERING`). Needs import from behavior.
#
# Description of Output:
# None. Side effect is initializing the state attributes of the `self` object.

# 1.2 Method: update
# Description:
# Advances the agent's state for a single simulation tick. This is the main
# method called by the `SimulationWorld`. It handles aging, checks for death,
# determines the agent's behavior state transition, executes the logic for
# the current behavior state (which includes movement timing and execution),
# and applies energy costs. **Accepts the `world` instance for sensing.**
# Inputs:
#   - self: The Agent instance being updated.
#   - world: The SimulationWorld instance (for sensing and interaction). Type: world.SimulationWorld.
# Where Inputs Typically Come From: Called by `SimulationWorld.update()` per agent.
# Restrictions on Inputs: None.
# Other Relevant Info: Orchestrates state transitions and state execution via the `behavior` module.
#
# Description of Algorithm/Process:
# 1. Check if `self.alive` is `False`. If dead, return immediately.
# 2. Increment `self.traits.age`.
# 3. Check for old age death (`self.traits.age >= self.traits.max_age`). If dead, set `self.alive = False` and return.
# 4. --- State Transition ---
#    a. Determine the *next* potential behavior state by calling a behavior function, passing the agent and world: `next_state = behavior.get_next_state(self, world)`. This function will decide based on current state, traits, and sensed environment.
#    b. If the `next_state` is different from the `self.current_behavior_state`:
#       i. (Optional) Call an `on_exit_state` function/method for the current state.
#       ii. Update the agent's state: `self.current_behavior_state = next_state`.
#       iii. (Optional) Call an `on_enter_state` function/method for the new state.
# 5. --- State Execution ---
#    a. Execute the logic for the agent's *current* behavior state by calling a behavior function, passing agent and world: `behavior.execute_state(self, world)`. This function will handle movement timing, calling `move_agent`, managing the `target`, applying energy cost, etc., *based on the specific state logic*.
#
# Description of Output:
# None. Side effects include modifying the agent's state (`age`, `alive`, `energy`, `x`, `y`, `direction`, `tick_counter`, `target`, **current_behavior_state**).

# 1.3 Method: eat
# Description:
# Allows the agent to consume a food source, increasing its energy level. Called
# by the `SimulationWorld` when an agent interacts with food.
# Inputs:
#   - self: The Agent instance.
#   - food: The FoodPellet instance being eaten. Type: world.food.FoodPellet.
# Where Inputs Typically Come From: Called by `SimulationWorld::_handle_agent_food_interaction`.
# Restrictions on Inputs: Food must have `energy_value`.
# Other Relevant Info: Increases energy, sets food energy to 0. Might clear target.
#
# Description of Algorithm/Process:
# 1. Check if food is valid and edible (`food and food.energy_value > 0`).
# 2. Add `food.energy_value` to `self.traits.energy`.
# 3. Set `food.energy_value` to 0.
# 4. (Optional) If `self.target == food`, set `self.target = None`.
#
# Description of Output:
# None. Side effects: updates agent energy, depletes food energy, potentially clears target.

# 1.4 Method: draw
# Description:
# Instructs the rendering module to draw the agent.
# Inputs:
#   - self: The Agent instance.
#   - surface: The pygame surface. Type: pygame.Surface.
#   - is_selected (optional): bool.
# Where Inputs Typically Come From: Called by `SimulationWorld.draw()`.
# Restrictions on Inputs: Valid surface.
# Other Relevant Info: Delegates to `agent.render::draw_agent`.
#
# Description of Algorithm/Process:
# 1. Call `draw_agent(self, surface, is_selected)`.
#
# Description of Output:
# None. Side effect: agent rendered on surface.


# --- START CODE IMPLEMENTATION ---

# Imports:
# Standard library imports first
import random

# Local package imports
from .traits import AgentTraits
from .movement import move_agent, get_random_direction
from .render import draw_agent
# Import the behavior module and its state constants
from . import behavior
from .behavior import AgentState # Import AgentState constants directly for clarity


### 1. Class: Agent Implementation ###
class Agent:
    ### 1.1 Method: __init__ Implementation ###
    def __init__(self, x, y):
        """
        Initializes a new agent at a given grid position and sets its initial state.
        """
        self.x = x
        self.y = y
        self.direction = get_random_direction() # Use helper for initial direction

        self.traits = AgentTraits() # Assign initial traits

        self.tick_counter = 0       # Counter to track ticks for move interval
        self.alive = True           # Agent's survival status

        self.target = None # Field to store the agent's current target

        # New: Attribute for the agent's current behavior state
        self.current_behavior_state = AgentState.WANDERING # Start in the default state


    ### 1.2 Method: update Implementation ###
    def update(self, world):
        """
        Updates the agent's state for a single simulation tick, managing
        its lifecycle and orchestrating behavior via the state machine.
        Requires the world instance for sensing/interaction.
        """
        if not self.alive:
            return # Dead agents don't update

        # --- Lifecycle: Aging and Age Death ---
        self.traits.age += 1
        if self.traits.age >= self.traits.max_age:
            self.alive = False
            # Optional Debug: print(f"Agent {id(self)} died of old age at tick {world.state.tick_count}.")
            return

        # --- Behavior: State Transition ---
        # Determine the next behavior state based on current state, traits, and world context
        next_state = behavior.get_next_state(self, world)

        # If the state is changing, perform transition actions (optional)
        if next_state != self.current_behavior_state:
             # Optional: Call on_exit for current state
             # Optional: Call on_enter for next state
             self.current_behavior_state = next_state
             # Optional Debug: print(f"Agent {id(self)} transition to state: {self.current_behavior_state} at tick {world.state.tick_count}.")


        # --- Behavior: State Execution ---
        # Execute the actions associated with the current behavior state
        # This function in behavior.py will handle movement timing, target logic, energy cost, etc.
        behavior.execute_current_state(self, world)

        # Note: Energy drain per move and death check based on energy are now
        # expected to be handled within the execute_current_state logic in behavior.py
        # when a move actually occurs. A passive per-tick drain could still be here
        # if it applies regardless of state/movement.

        # Optional: Passive Energy drain per tick (if implemented in AgentTraits and config)
        # if self.traits.energy_drain_per_tick > 0:
        #     self.traits.energy -= self.traits.energy_drain_per_tick
        #     if self.traits.energy <= 0:
        #         self.alive = False
        #         # Optional Debug: print(f"Agent {id(self)} died from lack of passive energy at tick {world.state.tick_count}.")
        #         return


    ### 1.3 Method: eat Implementation ###
    def eat(self, food):
        """
        Allows the agent to consume a food source. Increases energy.
        Called by SimulationWorld when agent and food are on the same cell.
        """
        if food and food.energy_value > 0:
            self.traits.energy += food.energy_value
            food.energy_value = 0 # Food is consumed/depleted (will be removed by world logic)

            # Optional: Cap energy at a maximum if max_energy trait exists
            # if hasattr(self.traits, 'max_energy') and self.traits.max_energy is not None:
            #    self.traits.energy = min(self.traits.energy, self.traits.max_energy)

            # If the eaten food was the agent's target, clear the target
            if self.target == food:
               self.target = None
               # Optional Debug: print(f"Agent {id(self)} ate food at ({food.x},{food.y}) and cleared target at tick {world.state.tick_count}.") # Needs world here for tick count


    ### 1.4 Method: draw Implementation ###
    def draw(self, surface, is_selected=False):
        """
        Draws the agent on the given pygame surface.
        Calls the separate rendering function.
        """
        draw_agent(self, surface, is_selected)


# --- END CODE IMPLEMENTATION ---