# world/__init__.py
# This file makes the 'world' directory a Python package
# It also defines the main SimulationWorld class

# Import necessary components from other modules within the world package
from .grid import draw_grid         # Import the grid drawing function
from .sim import SimulationState    # Import the simulation state manager
from .food import FoodPellet        # Import the FoodPellet class

# Import the Agent class from the agent package
# Assuming agent/__init__.py correctly exposes the Agent class from agent/base.py
from agent import Agent # This import should now work correctly

import random # Needed for placing agents/food
# Import specific constants from config
from config import (GRID_COLS, GRID_ROWS, CELL_SIZE, INITIAL_AGENT_COUNT,
                    INITIAL_FOOD_COUNT, FOOD_LIFESPAN_TICKS, FOOD_SPAWN_INTERVAL_TICKS,
                    FOOD_SPAWN_AMOUNT, FOOD_ENERGY_VALUE)

# --- Removed the sys.path manipulation ---
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# import os # No longer need os if not manipulating path


class SimulationWorld:
    """
    Manages the entire simulation state: agents, food, grid, and simulation state.
    """
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


    def _spawn_initial_agents(self, count):
        """Spawns a specified number of agents at random locations."""
        for _ in range(count):
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)
            # Agents are created with default traits in their own __init__
            self.agents.append(Agent(x, y))


    def _spawn_initial_food(self, count):
        """Spawns a specified number of food pellets at random locations."""
        for _ in range(count):
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)
            # FoodPellets are created with explicit values now
            self.food.append(FoodPellet(x, y, lifespan=FOOD_LIFESPAN_TICKS, energy_value=FOOD_ENERGY_VALUE))


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
            if 0 <= index < len(self.food): # Add a safety check
                self.food.pop(index)


    def update(self):
        """Updates the state of the simulation for one tick."""
        # Only perform updates if the simulation state allows (not paused or pending steps)
        if not self.state.is_running():
            return

        self.state.increment_tick() # Advance the simulation tick

        # --- Simulation Logic for the Current Tick ---

        # 1. Update Agents
        # Agents update their internal state (age, energy drain per tick)
        # Their movement is handled within agent.update() based on move_interval_ticks
        for agent in self.agents:
            agent.update()

        # 2. Update Food (handle lifespan)
        # Increment food age
        for pellet in self.food:
            pellet.update() # Increments pellet.age

        # Remove expired food pellets
        # Use a list comprehension to keep only food pellets that have NOT expired
        # The is_expired method now takes the current tick count
        self.food = [
            pellet for pellet in self.food
            if not pellet.is_expired(self.state.tick_count)
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