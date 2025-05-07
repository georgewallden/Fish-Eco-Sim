# agent/base.py
#
# Description:
# This file defines the core `Agent` class, which represents an individual
# fish-like entity in the simulation. It encapsulates the agent's fundamental
# state (position, direction, traits, alive status, target, behavior state,
# **neural network**). It orchestrates its actions during a simulation tick
# by calling the appropriate behavior logic (which uses the network for decisions),
# movement mechanics, and rendering.
#
# Key responsibilities of this file:
# - Define the `Agent` class structure.
# - Hold the state of an individual agent, including its neural network instance.
# - Manage the agent's lifecycle within a simulation tick (aging, death).
# - Delegate behavior logic, including state transitions and state execution
#   (driven by the neural network), to the `behavior` module.
# - Delegate position updates to the `movement` module (called by behavior execution).
# - Delegate visual representation to the `render` module.
# - Handle consumption of food.
#
# Design Philosophy/Notes:
# - Acts as the primary representation of an individual entity.
# - Follows a compositional pattern, using instances of `AgentTraits` and `NeuralNetwork`,
#   and calling functions from `agent.movement`, `agent.render`, and `agent.behavior`.
# - The `update` method is the central method for the agent's actions each tick.
# - Includes a `target` attribute to support goal-directed movement *within* certain behaviors.
# - Includes a `current_behavior_state` attribute for the State Machine pattern.
# - Each agent instance holds its *own* neural network, allowing for individual learning/evolution later.
# - Accepts the `SimulationWorld` instance in its `update` method to enable
#   sensing the environment via dedicated world methods (called by behavior).

# Imports Description:
# This section lists the modules imported by agent/base.py and their purpose.
# - random: Standard library, used for initial random direction generation.
# - .traits.AgentTraits: Imports the class that holds the agent's characteristics and stats.
# - .movement.move_agent: Imports the function that applies movement based on direction and handles boundaries.
# - .movement.get_random_direction: Imports the helper function for getting initial/random directions.
# - .render.draw_agent: Imports the function for drawing the agent's visual representation.
# - . import behavior: Imports the `agent.behavior` module as a whole to access its state transition and execution functions.
# - behavior.AgentState: Imports the constants defining the possible behavior states, used for initializing `current_behavior_state`.
# - .neural_net.NeuralNetwork: **NEW** Imports the class defining the agent's neural network brain.
# - config: (Implicitly used by imported modules). Might be needed directly if passing network dimensions from config.

# Code Block Descriptions:
# This section provides detailed blueprints for the code blocks (class and methods)
# implemented below.

# 1. Class: Agent
# Description:
# Represents a single active entity in the simulation. An agent exists at a specific
# grid location, has a direction, a set of traits, manages its lifecycle, tracks
# a target, operates within a specific behavioral state, and uses a neural network
# to inform its decisions.
#
# Attributes:
# - x (int): The agent's current grid column index.
# - y (int): The agent's current grid row index.
# - direction (str): The agent's current cardinal direction ("N", "S", "E", "W").
# - traits (AgentTraits): An instance of the AgentTraits class holding the agent's stats and properties.
# - tick_counter (int): Counter used for movement timing.
# - alive (bool): True if the agent is currently alive, False if dead.
# - target (object or None): A reference to an object the agent is currently moving towards.
# - current_behavior_state (str): The current state of the agent's behavior state machine.
# - network (NeuralNetwork): **NEW** An instance of the NeuralNetwork class, this agent's brain.
#
# Primary Role: Represent an individual simulation participant, hold its state including its neural network, and drive its actions via behavior logic.

# 1.1 Method: __init__
# Description:
# Constructor for the Agent class. Initializes a new agent instance with default
# position, direction, traits, state flags, target, behavior state, and creates
# its individual neural network instance.
# Inputs:
#   - self: The instance being initialized.
#   - x: The initial grid column index. Type: int.
#   - y: The initial grid row index. Type: int.
# Where Inputs Typically Come From: Called by `SimulationWorld` during spawning.
# Restrictions on Inputs: Caller should ensure valid grid coordinates.
# Other Relevant Info: Creates and assigns `AgentTraits` and `NeuralNetwork` instances. Sets the default behavior state.
#
# Description of Algorithm/Process:
# 1. Store `x` and `y` position.
# 2. Set initial random `direction`.
# 3. Create and assign `AgentTraits` instance to `self.traits`.
# 4. Initialize `self.tick_counter` to 0.
# 5. Set `self.alive` to `True`.
# 6. Initialize `self.target` to `None`.
# 7. Set `self.current_behavior_state` to the default wandering state constant (`behavior.AgentState.WANDERING`).
# 8. **NEW:** Create and assign a `NeuralNetwork` instance to `self.network`. The network dimensions (input, hidden, output size) must be specified based on the defined observation and action spaces.
#    - Input size: Based on `get_observation` output (e.g., 2 for `[normalized_energy, sees_food_flag]`).
#    - Output size: Based on the network output interpretation (e.g., 1 for a binary choice between states).
#    - Hidden size: A design choice (e.g., 4).
#
# Description of Output:
# None. Side effect is initializing the state attributes of the `self` object, including its network.

# 1.2 Method: update
# Description:
# Advances the agent's state for a single simulation tick. It manages
# lifecycle, checks for death, and delegates behavior logic (state transition
# and execution) to the `behavior` module. The behavior logic will now
# internally use the agent's neural network for decisions. **Accepts the `world`
# instance for sensing.**
# Inputs:
#   - self: The Agent instance being updated.
#   - world: The SimulationWorld instance (for sensing and interaction). Type: world.SimulationWorld.
# Where Inputs Typically Come From: Called by `SimulationWorld.update()` per agent.
# Restrictions on Inputs: None.
# Other Relevant Info: Orchestrates state transitions and state execution via the `behavior` module. The behavior module will access `self.network`.
#
# Description of Algorithm/Process:
# 1. Check if `self.alive` is `False`. If dead, return.
# 2. Increment `self.traits.age`.
# 3. Check for old age death. If dead, set `self.alive = False` and return.
# 4. --- Behavior: State Transition (driven by Network) ---
#    a. Determine the *next* potential behavior state by calling `behavior.get_next_state(self, world)`. This function in the behavior module will use `self.network`.
#    b. If the `next_state` is different from `self.current_behavior_state`:
#       i. Update the agent's state: `self.current_behavior_state = next_state`.
#       ii. (Optional) Call state entry/exit actions in behavior.
# 5. --- Behavior: State Execution ---
#    a. Execute the logic for the agent's *current* behavior state by calling `behavior.execute_current_state(self, world)`. This function in the behavior module handles movement timing, calling `move_agent`, managing `target`, applying energy cost, and checking for energy death *based on the state and network output* (if network output drives actions within states).
#
# Description of Output:
# None. Side effects include modifying the agent's state (`age`, `alive`, `energy`, `x`, `y`, `direction`, `tick_counter`, `target`, current_behavior_state).

# 1.3 Method: eat
# Description:
# Allows the agent to consume a food source, increasing its energy. Called
# by the `SimulationWorld`.
# Inputs:
#   - self: The Agent instance.
#   - food: The FoodPellet instance being eaten. Type: world.food.FoodPellet.
# Where Inputs Typically Come From: Called by `SimulationWorld::_handle_agent_food_interaction`.
# Restrictions on Inputs: Food must have `energy_value`.
# Other Relevant Info: Increases energy, sets food energy to 0. Might clear target.
#
# Description of Algorithm/Process:
# 1. Check if food is valid and edible.
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
# NEW: Import the NeuralNetwork class
from .neural_net import NeuralNetwork


### 1. Class: Agent Implementation ###
class Agent:
    ### 1.1 Method: __init__ Implementation ###
    def __init__(self, x, y):
        """
        Initializes a new agent at a given grid position, sets its state, traits, and neural network.
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

        self.target = None # Field to store the agent's current target for goal-directed movement

        # Attribute for the agent's current behavior state
        self.current_behavior_state = AgentState.WANDERING # Start in the default state

        # NEW: Create an instance of the neural network for this agent
        # Based on minimal observation [normalized_energy, sees_food_flag] (2 inputs)
        # and binary state choice output (1 output)
        # Hidden size is a design choice (e.g., 4)
        self.network = NeuralNetwork(input_size=2, hidden_size=4, output_size=1)


    ### 1.2 Method: update Implementation ###
    def update(self, world):
        """
        Updates the agent's state for a single simulation tick, managing
        its lifecycle and orchestrating behavior via the state machine
        driven by the neural network. Requires the world instance for sensing/interaction.
        """
        if not self.alive:
            return # Dead agents don't update

        # --- Lifecycle: Aging and Age Death ---
        self.traits.age += 1
        if self.traits.age >= self.traits.max_age:
            self.alive = False
            # Optional Debug: print(f"Agent {id(self)} died of old age at tick {world.state.tick_count}.")
            return

        # --- Behavior: State Transition (driven by Network) ---
        # Determine the next behavior state by consulting the behavior module, which uses the network
        # Pass the agent (which holds the network) and the world (for sensing)
        next_state = behavior.get_next_state(self, world)

        # If the state is changing, perform transition actions (optional)
        if next_state != self.current_behavior_state:
             # Optional: Call behavior.on_exit_state(self, world) for current state
             # Optional: Call behavior.on_enter_state(self, world) for next state
             self.current_behavior_state = next_state
             # Optional Debug: print(f"Agent {id(self)} transition to state: {self.current_behavior_state} at tick {world.state.tick_count}.")


        # --- Behavior: State Execution ---
        # Execute the actions associated with the current behavior state
        # This function in behavior.py uses the current state to perform logic
        behavior.execute_current_state(self, world)

        # Note: Energy drain per move and death check based on energy are now
        # handled within the execute_current_state logic in behavior.py
        # when a move actually occurs for states that involve movement.


    ### 1.3 Method: eat Implementation ###
    def eat(self, food):
        """
        Allows the agent to consume a food source. Increases energy.
        Called by SimulationWorld when agent and food are on the same cell.
        """
        if food and food.energy_value > 0:
            self.traits.energy += food.energy_value
            food.energy_value = 0 # Food is consumed/depleted (will be removed by world logic)

            # Optional: Cap energy at a maximum using the trait value
            if hasattr(self.traits, 'max_energy'): # Check if max_energy trait exists
               self.traits.energy = min(self.traits.energy, self.traits.max_energy)

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