# world/food.py
#
# Description:
# This module defines the `FoodPellet` class, which represents a consumable
# food source in the simulation grid. Each food pellet has a position,
# an energy value it provides when eaten, a lifespan, and tracks its age.
# It includes methods for updating its state (aging) and drawing itself.
#
# Key responsibilities of this file:
# - Define the `FoodPellet` class.
# - Hold the state (position, energy, lifespan, age) of individual food pellets.
# - Provide a method for aging the food pellet.
# - Provide a method to check if the food pellet has expired.
# - Provide a method to draw the food pellet visually.
#
# Design Philosophy/Notes:
# - Encapsulates the data and simple behaviors of a single food item.
# - Keeps its `update` method simple, primarily incrementing age.
# - The core simulation logic (`SimulationWorld`) is responsible for creating,
#   managing lists of, interacting with, and removing food pellets.
# - Drawing logic is self-contained within the class's `draw` method.

# Imports Description:
# This section lists the modules imported by world/food.py and their purpose.
# - pygame: Needed for drawing the food pellet shape (`pygame.draw.polygon`)
#   and calculating position/size based on `CELL_SIZE`.
# - random: (Not strictly used in the current methods but included in the original). It might be used in future extensions (e.g., randomized energy value).
# - config: Imports constants (`GRID_COLS`, `GRID_ROWS`, `CELL_SIZE`,
#   `COLOR_FOOD`, `FOOD_ENERGY_VALUE`, `FOOD_LIFESPAN_TICKS`) used during
#   initialization (`__init__`) and drawing.

# Code Block Descriptions:
# This section provides detailed blueprints for the code blocks implemented below.

# 1. Class: FoodPellet
# Description:
# Represents a single food item positioned on the grid. It has properties
# related to its location, nutritional value, and how long it lasts.
#
# Attributes:
# - x (int): The grid column index where the food pellet is located.
# - y (int): The grid row index where the food pellet is located.
# - lifespan (int): The maximum number of ticks the food pellet will exist before expiring.
# - age (int): The current number of ticks the food pellet has existed since spawning.
# - energy_value (int): The amount of energy this food pellet provides to an agent that consumes it.
#
# Primary Role: Represent a static, consumable resource in the world.

# 1.1 Method: __init__
# Description:
# Constructor for the FoodPellet class. Initializes a new food pellet at a
# specific grid location with a defined lifespan and energy value.
# Inputs:
#   - self: The instance being initialized.
#   - x: The initial grid column index for the food pellet. Type: int.
#        Origin: Passed by `SimulationWorld` during spawning.
#        Restrictions: 0 <= x < GRID_COLS (caller's responsibility).
#   - y: The initial grid row index for the food pellet. Type: int.
#        Origin: Passed by `SimulationWorld` during spawning.
#        Restrictions: 0 <= y < GRID_ROWS (caller's responsibility).
#   - lifespan: The maximum age (in ticks) for this pellet. Type: int.
#               Origin: Passed by `SimulationWorld` (usually from `config.py`).
#               Restrictions: Should be a non-negative integer.
#   - energy_value: The energy amount provided upon consumption. Type: int.
#                   Origin: Passed by `SimulationWorld` (usually from `config.py`).
#                   Restrictions: Should be a non-negative integer.
# Where Inputs Typically Come From: Called by `SimulationWorld`'s spawning methods (`_spawn_initial_food`, `_spawn_food_over_time`).
# Restrictions on Inputs: Caller should ensure valid grid coordinates.
# Other Relevant Info: Sets the initial state of the food pellet.
#
# Description of Algorithm/Process:
# 1. Assign the input `x` and `y` to `self.x` and `self.y`.
# 2. Assign the input `lifespan` to `self.lifespan`.
# 3. Initialize `self.age` to 0.
# 4. Assign the input `energy_value` to `self.energy_value`.
#
# Description of Output:
# None. Side effect is initializing the state attributes of the `self` object.

# 1.2 Method: update
# Description:
# Advances the food pellet's internal age counter by one tick.
# Inputs:
#   - self: The FoodPellet instance being updated.
# Where Inputs Typically Come From: Called by `SimulationWorld.update()` for each active food pellet.
# Restrictions on Inputs: None.
# Other Relevant Info: This is a simple update; the check for expiration and removal is done externally.
#
# Description of Algorithm/Process:
# 1. Increment `self.age` by 1.
#
# Description of Output:
# None. Side effect is incrementing the `self.age` attribute.

# 1.3 Method: is_expired
# Description:
# Checks if the food pellet has reached or exceeded its maximum lifespan.
# Inputs:
#   - self: The FoodPellet instance.
#   - current_tick: The current simulation tick count. Type: int.
#                   Origin: Passed by `SimulationWorld.update()`.
#                   Restrictions: Should be a non-negative integer.
# Where Inputs Typically Come From: Called by `SimulationWorld.update()` to filter the food list.
# Restrictions on Inputs: None.
# Other Relevant Info: Uses the pellet's internal `age` to determine expiration. The `current_tick` parameter is not strictly necessary with the current implementation but is included in the original code's signature; the logic relies on `self.age`.
#
# Description of Algorithm/Process:
# 1. Compare `self.age` with `self.lifespan`.
# 2. Return `True` if `self.age` is greater than or equal to `self.lifespan`, `False` otherwise.
#
# Description of Output:
# A boolean value indicating whether the food pellet has expired. Type: bool.
# Output Range: `True` or `False`.

# 1.4 Method: draw
# Description:
# Draws the food pellet onto the given Pygame surface as a diamond shape
# at its grid location.
# Inputs:
#   - self: The FoodPellet instance to be drawn.
#   - surface: The pygame surface object to draw on. Type: pygame.Surface.
#              Origin: Passed from `SimulationWorld.draw()`.
#              Restrictions: Must be a valid pygame Surface.
# Where Inputs Typically Come From: Called by `SimulationWorld.draw()`.
# Restrictions on Inputs: None.
# Other Relevant Info: Uses `self.x`, `self.y`, `CELL_SIZE`, and `COLOR_FOOD` from `config.py` for positioning, sizing, and coloring.
#
# Description of Algorithm/Process:
# 1. Calculate the pixel center coordinates (`cx`, `cy`) of the grid cell where the food is located, using `self.x`, `self.y`, and `CELL_SIZE`.
# 2. Determine an offset value based on `CELL_SIZE` to define the size of the diamond.
# 3. Define a list of pixel coordinates for the vertices of the diamond shape relative to the calculated center (`cx`, `cy`).
# 4. Draw a filled polygon (the diamond) on the `surface` using the `COLOR_FOOD` from `config.py` and the list of vertices.
#
# Description of Output:
# None. Side effect is drawing the food pellet onto the provided `surface`.


# --- START CODE IMPLEMENTATION ---

# Imports:
# Standard library imports first
import pygame
# import random # Not used in current methods

# Local package imports
# Import specific constants from config
from config import CELL_SIZE, COLOR_FOOD, FOOD_ENERGY_VALUE, FOOD_LIFESPAN_TICKS


### 1. Class: FoodPellet Implementation ###
class FoodPellet:
    ### 1.1 Method: __init__ Implementation ###
    def __init__(self, x, y, lifespan, energy_value):
        self.x = x
        self.y = y
        self.lifespan = lifespan # Max age before despawning
        self.age = 0 # Current age in ticks
        self.energy_value = energy_value # Energy provided when eaten

    ### 1.2 Method: update Implementation ###
    def update(self):
        """Updates the food pellet's state (increments age)."""
        self.age += 1

    ### 1.3 Method: is_expired Implementation ###
    # Original signature included current_tick, keeping it for now
    def is_expired(self, current_tick=None):
        """Checks if the food pellet has reached the end of its lifespan."""
        # Using the pellet's age for lifespan check
        return self.age >= self.lifespan
        # Alternative: if you stored the spawn tick, check current_tick - spawn_tick >= lifespan


    ### 1.4 Method: draw Implementation ###
    def draw(self, surface):
        """Draws the food pellet onto the given surface."""
        # Calculate pixel coordinates from grid coordinates
        cx = self.x * CELL_SIZE + CELL_SIZE // 2
        cy = self.y * CELL_SIZE + CELL_SIZE // 2
        offset = CELL_SIZE // 3 # Size of the diamond shape

        # Define the vertices of the diamond shape
        diamond = [
            (cx, cy - offset),  # top
            (cx + offset, cy),  # right
            (cx, cy + offset),  # bottom
            (cx - offset, cy),  # left
        ]

        # Draw the diamond using the configured food color
        pygame.draw.polygon(surface, COLOR_FOOD, diamond)


# --- END CODE IMPLEMENTATION ---