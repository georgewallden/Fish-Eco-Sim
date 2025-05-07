# world/__init__.py
#
# Description:
# This file serves as the initialization file for the 'world' Python package
# and defines the central `SimulationWorld` class. The `SimulationWorld`
# class is the primary manager of the simulation state, overseeing the grid
# environment, the population of agents, and the distribution of food. It
# contains the core logic for updating the simulation from one tick to the
# next, handling interactions, spawning entities, and drawing the world state.
#
# Key responsibilities of this file:
# - Make the 'world' directory a valid Python package.
# - Define the `SimulationWorld` class to encapsulate all world state.
# - Initialize the simulation with starting agents and food.
# - Orchestrate the per-tick update cycle (update agents, update food, handle interactions, spawn).
# - Manage the simulation's pause/play/step state via a `SimulationState` instance.
# - Handle drawing the world elements (grid, food, agents).
# - Manage the selection of an agent for UI display.
#
# Design Philosophy/Notes:
# - Acts as the central model for the simulation, holding all simulation objects.
# - Delegates specific logic (drawing grid, managing sim state, food properties, agent behavior/properties)
#   to other modules within the 'world' package or the 'agent' package.
# - The `update` method is the heart of the simulation's progression.

# Imports Description:
# This section lists the modules imported by world/__init__.py and their purpose.
# - .grid.draw_grid: Imports the function to draw the grid background.
# - .sim.SimulationState: Imports the class that manages the simulation's control state (paused, ticks).
# - .food.FoodPellet: Imports the class representing food items.
# - agent.Agent: Imports the main Agent class from the 'agent' package. This requires 'agent' to be a valid package and `agent.__init__.py` to expose the Agent class.
# - random: Standard library, used for generating random numbers/positions for spawning entities.
# - config: Imports various constants needed for initialization and simulation logic (grid dimensions, initial counts, food properties).

# Code Block Descriptions:
# This section provides detailed blueprints for the code blocks implemented below.

# 1. Class: SimulationWorld
# Description:
# The main class that holds and manages the entire state of the simulation
# world, including the grid dimensions, the list of living agents, the
# list of active food pellets, the simulation control state, and the
# currently selected agent. It orchestrates the simulation tick update
# and drawing process.
#
# Attributes:
# - cols (int): Number of grid columns, copied from config.
# - rows (int): Number of grid rows, copied from config.
# - cell_size (int): Size of each grid cell in pixels, copied from config.
# - GRID_WIDTH_PX (int): Total width of the grid area in pixels.
# - GRID_HEIGHT_PX (int): Total height of the grid area in pixels.
# - state (SimulationState): An instance of the SimulationState class managing ticks, pause/play.
# - agents (list[Agent]): A list containing all currently alive Agent objects.
# - food (list[FoodPellet]): A list containing all currently active FoodPellet objects.
# - selected_agent (Agent or None): The Agent object currently selected by the user in the UI, or None if none is selected.
# - _food_spawn_timer (int): Internal counter to track time until the next food spawning event.
#
# Primary Role: Encapsulate, manage, and update the entire simulation state.

# 1.1 Method: __init__
# Description:
# Constructor for the SimulationWorld. Initializes the world state, including
# grid dimensions, lists for agents and food, the simulation state manager,
# and populates the world with initial agents and food pellets. Sets up
# internal timers.
# Inputs:
#   - self: The instance being initialized.
# Where Inputs Typically Come From: Called once by `main.py` at the start of the application.
# Restrictions on Inputs: None.
# Other Relevant Info: Uses constants from `config.py` for initial setup. Calls helper methods to perform initial spawning.
#
# Description of Algorithm/Process:
# 1. Assign grid dimension and cell size attributes from `config.py` constants.
# 2. Calculate and store pixel dimensions of the grid area.
# 3. Create a new instance of `SimulationState` and assign it to `self.state`.
# 4. Initialize empty lists for `self.agents` and `self.food`.
# 5. Initialize `self.selected_agent` to `None`.
# 6. Call `_spawn_initial_agents()` using the initial agent count from `config.py`.
# 7. Call `_spawn_initial_food()` using the initial food count from `config.py`.
# 8. Initialize `self._food_spawn_timer` to 0.
#
# Description of Output:
# None. Side effect is initializing the `self` object and populating it with initial entities.

# 1.2 Method: _spawn_initial_agents
# Description:
# Helper method to spawn a specified number of agents at random valid grid locations.
# Inputs:
#   - self: The SimulationWorld instance.
#   - count: The number of agents to spawn. Type: int. Origin: Called by `__init__` with a value from `config.py`. Restrictions: Must be a non-negative integer.
# Where Inputs Typically Come From: Called internally by `__init__`.
# Restrictions on Inputs: `count` should be >= 0.
# Other Relevant Info: Uses `random.randint` and the world's grid dimensions. Appends new `Agent` instances to `self.agents`.
#
# Description of Algorithm/Process:
# 1. Loop `count` times.
# 2. In each iteration, generate a random integer `x` between 0 and `self.cols - 1`.
# 3. Generate a random integer `y` between 0 and `self.rows - 1`.
# 4. Create a new `Agent` instance at position (`x`, `y`).
# 5. Append the newly created agent instance to the `self.agents` list.
#
# Description of Output:
# None. Side effect is populating the `self.agents` list.

# 1.3 Method: _spawn_initial_food
# Description:
# Helper method to spawn a specified number of food pellets at random valid grid locations.
# Inputs:
#   - self: The SimulationWorld instance.
#   - count: The number of food pellets to spawn. Type: int. Origin: Called by `__init__` with a value from `config.py`. Restrictions: Must be a non-negative integer.
# Where Inputs Typically Come From: Called internally by `__init__`.
# Restrictions on Inputs: `count` should be >= 0.
# Other Relevant Info: Uses `random.randint` and the world's grid dimensions. Appends new `FoodPellet` instances to `self.food` with properties from `config.py`.
#
# Description of Algorithm/Process:
# 1. Loop `count` times.
# 2. In each iteration, generate a random integer `x` between 0 and `self.cols - 1`.
# 3. Generate a random integer `y` between 0 and `self.rows - 1`.
# 4. Create a new `FoodPellet` instance at position (`x`, `y`), using `FOOD_LIFESPAN_TICKS` and `FOOD_ENERGY_VALUE` from `config.py`.
# 5. Append the newly created food pellet instance to the `self.food` list.
#
# Description of Output:
# None. Side effect is populating the `self.food` list.

# 1.4 Method: _spawn_food_over_time
# Description:
# Handles the periodic spawning of new food pellets during the simulation based
# on an internal timer and configuration settings. Only spawns food if the
# simulation is not paused.
# Inputs:
#   - self: The SimulationWorld instance.
# Where Inputs Typically Come From: Called internally by `update` during each tick.
# Restrictions on Inputs: None.
# Other Relevant Info: Uses `_food_spawn_timer`, `FOOD_SPAWN_INTERVAL_TICKS`, `FOOD_SPAWN_AMOUNT`, `FOOD_LIFESPAN_TICKS`, `FOOD_ENERGY_VALUE` from `config.py`. Accesses `self.state.paused`.
#
# Description of Algorithm/Process:
# 1. Check if `self.state.paused` is `False`. If the simulation is paused, exit the method.
# 2. Increment `self._food_spawn_timer`.
# 3. Check if `self._food_spawn_timer` has reached or exceeded `FOOD_SPAWN_INTERVAL_TICKS`.
# 4. If the timer threshold is met:
#    a. Reset `self._food_spawn_timer` to 0.
#    b. Loop `FOOD_SPAWN_AMOUNT` times.
#    c. In each loop iteration, generate a random valid grid position (`x`, `y`).
#    d. Create a new `FoodPellet` instance at (`x`, `y`) with properties from `config.py`.
#    e. Append the new food pellet to `self.food`.
#
# Description of Output:
# None. Side effect is potentially adding new food pellets to `self.food`.

# 1.5 Method: _handle_agent_food_interaction
# Description:
# Processes interactions between agents and food pellets. It checks if any
# alive agent is on the same grid cell as an edible food pellet and, if so,
# triggers the agent's eating behavior and marks the food for removal.
# Inputs:
#   - self: The SimulationWorld instance.
# Where Inputs Typically Come From: Called internally by `update` during each tick.
# Restrictions on Inputs: None.
# Other Relevant Info: Iterates through `self.agents` and `self.food`. Calls `agent.eat()`. Modifies `self.food`.
#
# Description of Algorithm/Process:
# 1. Create an empty set `eaten_food_indices` to track the indices of food pellets that are eaten.
# 2. Iterate through each `agent` in the `self.agents` list.
# 3. If the agent is not `agent.alive`, skip to the next agent.
# 4. Create a list `food_at_location_indices` containing the indices of food pellets in `self.food` that are at the same grid position (`x`, `y`) as the current agent AND have `energy_value > 0`.
# 5. If `food_at_location_indices` is not empty (food was found at the agent's location):
#    a. Get the index of the first food pellet found (`food_index_to_eat = food_at_location_indices[0]`).
#    b. Call the current agent's `eat()` method, passing the `FoodPellet` object `self.food[food_index_to_eat]`.
#    c. Add `food_index_to_eat` to the `eaten_food_indices` set.
# 6. After iterating through all agents, get a sorted list of unique indices from `eaten_food_indices` in reverse order.
# 7. Iterate through this sorted list of indices.
# 8. For each `index`:
#    a. Add a safety check `0 <= index < len(self.food)` before attempting removal.
#    b. Remove the food pellet from `self.food` at the specified `index` using `self.food.pop(index)`.
#
# Description of Output:
# None. Side effects include increasing agent energy and removing eaten food pellets from `self.food`.

# 1.6 Method: update
# Description:
# Advances the simulation state by one tick. This is the core simulation logic
# loop per tick. It updates all dynamic elements (agents, food), handles
# interactions, and manages spawning. It only runs if the simulation state
# (`self.state`) indicates it should (not paused or has pending steps).
# Inputs:
#   - self: The SimulationWorld instance.
# Where Inputs Typically Come From: Called once per frame by `main.py`'s main loop.
# Restrictions on Inputs: None.
# Other Relevant Info: Checks `self.state.is_running()`. Calls update methods on agents and food, interaction handlers, and spawning logic. Modifies `self.agents` and `self.food` lists by removing dead/expired entities. Calls `agent.update()`, which requires the `world` instance to be passed for sensing.
#
# Description of Algorithm/Process:
# 1. Check if `self.state.is_running()` is `False`. If the simulation should not run this tick (paused with no steps), return immediately.
# 2. Increment the simulation tick count using `self.state.increment_tick()`.
# 3. --- Update Agents ---
#    a. Iterate through each `agent` in the `self.agents` list.
#    b. Call `agent.update(self)` to update the agent's internal state, trigger movement timing, handle aging/energy drain, and potentially call agent behavior/sensing logic (needs the world instance passed).
# 4. --- Update Food ---
#    a. Iterate through each `pellet` in the `self.food` list.
#    b. Call `pellet.update()` to increment its age.
#    c. After updating all food, create a new `self.food` list using a list comprehension, keeping only pellets where `pellet.is_expired(self.state.tick_count)` returns `False`.
# 5. --- Handle Interactions ---
#    a. Call `_handle_agent_food_interaction()` to process agents eating food.
#    b. (Placeholder) Call `_handle_agent_agent_interaction()` for future interactions (predation, reproduction).
# 6. --- Spawn New Entities ---
#    a. Call `_spawn_food_over_time()` to handle periodic food spawning.
# 7. --- Remove Dead Entities ---
#    a. Check if the currently `self.selected_agent` is no longer `alive`. If so, set `self.selected_agent` to `None`.
#    b. Create a new `self.agents` list using a list comprehension, keeping only agents where `agent.alive` is `True`.
# 8. (Optional) Call `self.state.finish_step()` if specific signaling is needed for stepping.
#
# Description of Output:
# None. Side effects include advancing the simulation tick count, modifying
# the state of all agents and food pellets, adding new food, and removing
# dead/expired entities from the world lists.

# 1.7 Method: draw
# Description:
# Draws the current visual state of the simulation world onto the provided
# Pygame surface. It draws the background, then food, then agents, ensuring
# correct layering. It also tells agents whether they are selected so they
# can draw a selection indicator.
# Inputs:
#   - self: The SimulationWorld instance.
#   - surface: The pygame surface to draw the world onto. Type: pygame.Surface. Origin: Passed from `main.py`'s drawing loop. Restrictions: Must be a valid pygame Surface.
# Where Inputs Typically Come From: Called once per frame by `main.py`'s main loop during the drawing phase.
# Restrictions on Inputs: None.
# Other Relevant Info: Calls drawing functions/methods from other modules (`draw_grid`, `FoodPellet.draw`, `Agent.draw`).
#
# Description of Algorithm/Process:
# 1. Call `draw_grid(surface)` from `world.grid` to draw the background with the depth gradient.
# 2. Iterate through each `pellet` in the `self.food` list.
# 3. Call `pellet.draw(surface)` for each food pellet (drawn under agents).
# 4. Iterate through each `agent` in the `self.agents` list.
# 5. For each agent, check if it is the same object as `self.selected_agent`.
# 6. Call `agent.draw(surface, is_selected)` for each agent, passing the surface and the selection status (drawn on top of food).
#
# Description of Output:
# None. Side effect is rendering the world state onto the `surface`.

# 1.8 Method: select_agent_at
# Description:
# Attempts to select an agent at the given grid coordinates when the user clicks
# within the simulation grid area. If an alive agent is found at the coordinates,
# it is set as the `self.selected_agent`. If multiple agents are present, it
# selects the one drawn last (by iterating the list in reverse).
# Inputs:
#   - self: The SimulationWorld instance.
#   - col: The grid column index of the click location. Type: int. Origin: Calculated in `ui.__init__.py::handle_ui_event` from pixel coordinates. Restrictions: Assumed to be within valid grid column bounds based on checks in the caller.
#   - row: The grid row index of the click location. Type: int. Origin: Calculated in `ui.__init__.py::handle_ui_event` from pixel coordinates. Restrictions: Assumed to be within valid grid row bounds based on checks in the caller.
# Where Inputs Typically Come From: Called by `ui.__init__.py::handle_ui_event` when a click occurs within the grid bounds.
# Restrictions on Inputs: Assumes `col` and `row` are valid grid coordinates (checked by caller).
# Other Relevant Info: Modifies the `self.selected_agent` attribute.
#
# Description of Algorithm/Process:
# 1. Initialize a variable `clicked_agent` to `None`.
# 2. Iterate through the `self.agents` list in reverse order (so agents drawn later, potentially on top, are checked first).
# 3. For each `agent`:
#    a. Check if the agent is `agent.alive`.
#    b. Check if the agent's position (`agent.x`, `agent.y`) matches the input `col` and `row`.
#    c. If both conditions are true (agent is alive and at the clicked location):
#       i. Assign this `agent` to `clicked_agent`.
#       ii. Break out of the loop (select only the first one found in reverse order).
# 4. Set `self.selected_agent` to the `clicked_agent` found (which will be `None` if no agent was found at the location).
#
# Description of Output:
# None. Side effect is updating the `self.selected_agent` attribute.


# --- START CODE IMPLEMENTATION ---

# Imports:
# Standard library imports first
import random

# Local package imports
# Import necessary components from other modules within the world package
from .grid import draw_grid
from .sim import SimulationState
from .food import FoodPellet

# Import the Agent class from the agent package
# Assuming agent.__init__.py correctly exposes the Agent class from agent.base
from agent import Agent

# Import specific constants from config
from config import (GRID_COLS, GRID_ROWS, CELL_SIZE, INITIAL_AGENT_COUNT,
                    INITIAL_FOOD_COUNT, FOOD_LIFESPAN_TICKS, FOOD_SPAWN_INTERVAL_TICKS,
                    FOOD_SPAWN_AMOUNT, FOOD_ENERGY_VALUE)


### 1. Class: SimulationWorld Implementation ###
class SimulationWorld:
    ### 1.1 Method: __init__ Implementation ###
    def __init__(self):
        """Initializes the simulation world with initial agents and food."""
        # Grid dimensions and cell size
        self.cols = GRID_COLS
        self.rows = GRID_ROWS
        self.cell_size = CELL_SIZE

        # Define the pixel width/height of the grid area (used by UI for click detection)
        self.GRID_WIDTH_PX = self.cols * self.cell_size
        self.GRID_HEIGHT_PX = self.rows * self.cell_size # May not be strictly needed but good to have

        self.state = SimulationState() # Initialize the simulation state manager
        self.agents = [] # List to hold agent objects
        self.food = [] # List to hold food pellet objects
        self.selected_agent = None # Currently selected agent (for UI)

        # --- Setup Initial Simulation State ---
        self._spawn_initial_agents(INITIAL_AGENT_COUNT)
        self._spawn_initial_food(INITIAL_FOOD_COUNT)

        # --- Timers/Counters for Spawning ---
        self._food_spawn_timer = 0

    ### 1.2 Method: _spawn_initial_agents Implementation ###
    def _spawn_initial_agents(self, count):
        """Spawns a specified number of agents at random locations."""
        for _ in range(count):
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)
            # Agents are created with default traits in their own __init__
            self.agents.append(Agent(x, y))

    ### 1.3 Method: _spawn_initial_food Implementation ###
    def _spawn_initial_food(self, count):
        """Spawns a specified number of food pellets at random locations."""
        for _ in range(count):
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)
            # FoodPellets are created with explicit values now
            self.food.append(FoodPellet(x, y, lifespan=FOOD_LIFESPAN_TICKS, energy_value=FOOD_ENERGY_VALUE))

    ### 1.4 Method: _spawn_food_over_time Implementation ###
    def _spawn_food_over_time(self):
        """Handles spawning new food based on a timer and config settings."""
        # Only spawn food if the simulation is running (not just stepping)
        if not self.state.paused:
            self._food_spawn_timer += 1
            if self._food_spawn_timer >= FOOD_SPAWN_INTERVAL_TICKS:
                self._food_spawn_timer = 0 # Reset the timer
                # Spawn a set amount of food
                for _ in range(FOOD_SPAWN_AMOUNT):
                    x = random.randint(0, self.cols - 1)
                    y = random.randint(0, self.rows - 1)
                    self.food.append(FoodPellet(x, y, lifespan=FOOD_LIFESPAN_TICKS, energy_value=FOOD_ENERGY_VALUE))

    ### 1.5 Method: _handle_agent_food_interaction Implementation ###
    def _handle_agent_food_interaction(self):
        """Checks if agents are on the same cell as food and handles eating."""
        eaten_food_indices = set() # Keep track of food pellets that were eaten

        # Iterate through all alive agents
        for agent in self.agents:
            if not agent.alive:
                continue # Skip dead agents

            # Find food pellets at the agent's current location
            # It's important to iterate through food by index if we plan to modify the list
            # Or collect indices/references first. Collecting indices is safer.
            food_at_location_indices = [
                i for i, pellet in enumerate(self.food)
                if pellet.x == agent.x and pellet.y == agent.y and pellet.energy_value > 0 # Check position and if it's still edible
            ]

            # If there's food, the agent eats one pellet (simple behavior: eats the first one found)
            if food_at_location_indices:
                food_index_to_eat = food_at_location_indices[0]
                agent.eat(self.food[food_index_to_eat]) # Call the agent's eat method
                eaten_food_indices.add(food_index_to_eat) # Mark this food pellet to be removed

        # Remove eaten food pellets.
        # Iterate through marked indices in reverse order to avoid messing up indices
        # of items not yet processed.
        for index in sorted(list(eaten_food_indices), reverse=True):
            # Add a safety check just in case list size changed unexpectedly
            if 0 <= index < len(self.food):
                 self.food.pop(index)


    ### 1.6 Method: update Implementation ###
    # Needs 'world' to be passed to agent.update for sensing
    def update(self):
        """Updates the state of the simulation for one tick."""
        # Only perform updates if the simulation state allows (not paused or pending steps)
        if not self.state.is_running():
            return

        self.state.increment_tick() # Advance the simulation tick

        # --- Simulation Logic for the Current Tick ---

        # 1. Update Agents
        # Agents update their internal state (age, energy drain, behavior, movement timing)
        # agent.update now needs the world context for sensing
        for agent in self.agents:
            agent.update(self) # Pass 'self' (the SimulationWorld instance)

        # 2. Update Food (handle lifespan)
        # Increment food age
        for pellet in self.food:
            pellet.update() # Increments pellet.age

        # Remove expired food pellets
        # Use a list comprehension to keep only food pellets that have NOT expired
        # The is_expired method now takes the current tick count (or uses internal age)
        self.food = [
            pellet for pellet in self.food
            if not pellet.is_expired(self.state.tick_count) # Pass tick count if needed, or rely on pellet's age
        ]

        # 3. Handle Interactions
        self._handle_agent_food_interaction()
        # _handle_agent_agent_interaction() # Future: predation, reproduction, mating, etc.

        # 4. Spawn New Food (based on timer)
        self._spawn_food_over_time()

        # 5. Remove Dead Agents
        # Use a list comprehension to keep only agents that are still alive
        # Also clear selected_agent if the selected one died
        if self.selected_agent and not self.selected_agent.alive:
            self.selected_agent = None # Deselect dead agent

        self.agents = [agent for agent in self.agents if agent.alive]

        # --- End Simulation Logic ---

        # If the simulation is stepping once or many, signal completion of this step
        self.state.finish_step()

    ### 1.7 Method: draw Implementation ###
    def draw(self, surface):
        """Draws the current state of the simulation world onto the surface."""
        # 1. Draw the grid background with the depth gradient
        draw_grid(surface)

        # 2. Draw food pellets (draw under agents)
        for pellet in self.food:
             pellet.draw(surface)

        # 3. Draw agents (draw on top of food)
        for agent in self.agents:
            # Check if this agent is the selected one for UI highlight
            is_selected = (agent == self.selected_agent)
            agent.draw(surface, is_selected) # Call the agent's draw method

    ### 1.8 Method: select_agent_at Implementation ###
    def select_agent_at(self, col, row):
        """Selects an agent at the given grid coordinates for UI display."""
        clicked_agent = None
        # Find the first alive agent at the clicked coordinates
        # Iterate in reverse allows selecting agents drawn on top
        for agent in reversed(self.agents):
            if agent.alive and agent.x == col and agent.y == row:
                clicked_agent = agent
                break # Select the first one found at that spot (topmost if drawn last)

        self.selected_agent = clicked_agent # Set or clear the selected agent


# --- END CODE IMPLEMENTATION ---