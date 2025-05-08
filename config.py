# config.py
#
# Description:
# This file centralizes all key configuration parameters for the simulation.
# It includes display settings, grid dimensions, colors, simulation timings,
# and base traits for agents and food. By keeping these values in one place,
# it makes the simulation easier to tune, modify, and understand without
# digging through the core logic files. It acts as a single source of truth
# for simulation parameters.
#
# Key responsibilities of this file:
# - Define window size and frame rate.
# - Define grid dimensions and cell size.
# - Define color schemes.
# - Set initial counts and properties for agents and food.
# - Define base traits for agents (which can be inherited or mutated).
# - Define UI-related parameters (like panel width).
#
# Design Philosophy/Notes:
# - All simulation-wide constants are defined here to minimize hardcoded values
#   spread throughout the codebase.
# - Derived values (like total screen width, cell size) are calculated based
#   on primary settings to maintain consistency.
# - Uses standard Python constants naming convention (uppercase).

# Imports Description:
# This file does not typically import other modules from the project or standard
# libraries, as it only defines static data/constants.

# Code Block Descriptions:
# This section provides detailed blueprints for the code blocks implemented below.
# As this file primarily defines constants, there is one main block for all the
# configuration values, broken down by category mirroring the implementation.

# 1. Simulation Configuration Constants
# Description:
# A collection of constants defining various parameters for the simulation.
# These constants are used by other modules (world, agent, ui) to configure
# their behavior and appearance. The constants are logically grouped by category.
#
# Defined Constants (by Category):
# --- Display Settings ---
# - SCREEN_WIDTH (int): Width of the simulation grid area in pixels.
# - SCREEN_HEIGHT (int): Height of the simulation grid area in pixels.
# - PANEL_WIDTH (int): Width of the UI panel on the right side in pixels.
# - TOTAL_SCREEN_WIDTH (int): Derived total window width (SCREEN_WIDTH + PANEL_WIDTH). Used for pygame display setup.
# - FPS (int): Frames per second, controls the visual update rate of the pygame window.
#
# --- Grid Settings ---
# - GRID_COLS (int): Number of columns in the grid.
# - GRID_ROWS (int): Number of rows in the grid.
# - CELL_SIZE (int): Derived size of each grid cell in pixels (SCREEN_WIDTH // GRID_COLS). Assumes SCREEN_WIDTH is divisible by GRID_COLS and SCREEN_HEIGHT by GRID_ROWS for square cells.
#
# --- Colors ---
# - COLOR_* (tuple(int, int, int)): RGB tuples defining various colors used in drawing simulation elements and UI.
#
# --- Simulation Settings ---
# - INITIAL_AGENT_COUNT (int): Number of agents created at the start of the simulation.
# - INITIAL_FOOD_COUNT (int): Number of food pellets created at the start.
# - FOOD_LIFESPAN_TICKS (int): How many simulation ticks a food pellet exists if not eaten.
# - FOOD_SPAWN_INTERVAL_TICKS (int): How often (in ticks) the world attempts to spawn new food.
# - FOOD_SPAWN_AMOUNT (int): How many food pellets are spawned during a single spawn event.
# - FOOD_ENERGY_VALUE (int): The amount of energy an agent gains from eating one food pellet.
# - TICK_JUMP_VALUES (list[int]): List of tick counts available in the UI dropdown menu for stepping the simulation multiple steps at once.
#
# --- Agent Settings (Initial/Default) ---
# - BASE_MOVE_INTERVAL_TICKS (int): Default number of ticks an agent waits between movements. Lower value means faster movement.
# - BASE_ENERGY_DRAIN_PER_MOVE (float): Energy cost incurred by an agent each time it successfully moves to a new cell.
# - BASE_ENERGY_DRAIN_PER_TICK (float): Optional: Energy cost incurred by an agent each simulation tick just for existing (use one or both drain types).
# - BASE_MAX_AGE_TICKS (int): Default maximum age (in ticks) an agent can reach before dying naturally of old age.
# - BASE_VISION_RANGE (int): Default number of grid cells an agent can 'see' outwards when searching for targets like food.
# - BASE_MAX_ENERGY (float): **NEW** Default maximum energy an agent can store. Used for initial energy and for normalizing energy levels for network input.
#
# Process:
# Simply defines and assigns static values to global constants upon file import. No runtime logic is performed.
# Output:
# None. The output is the availability of these constants for other modules to import and use.


# --- START CODE IMPLEMENTATION ---

### 1. Simulation Configuration Constants Implementation ###

# --- Display Settings ---
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
PANEL_WIDTH = 200
TOTAL_SCREEN_WIDTH = SCREEN_WIDTH + PANEL_WIDTH
FPS = 60

# --- Grid Settings ---
GRID_COLS = 192
GRID_ROWS = 108
CELL_SIZE = SCREEN_WIDTH // GRID_COLS
# Optional: Add assertions to check if SCREEN_WIDTH/HEIGHT are divisible by GRID_COLS/ROWS
# assert SCREEN_WIDTH % GRID_COLS == 0, "SCREEN_WIDTH must be divisible by GRID_COLS"
# assert SCREEN_HEIGHT % GRID_ROWS == 0, "SCREEN_HEIGHT must be divisible by GRID_ROWS"


# --- Colors ---
COLOR_OCEAN_DEEP = (10, 20, 80)
COLOR_OCEAN_SHALLOW = (50, 150, 250)
COLOR_FOOD = (255, 0, 0)
COLOR_AGENT_ALIVE = (0, 255, 0)
COLOR_AGENT_DEAD = (100, 100, 100)
COLOR_SELECTED_RING = (255, 255, 0)
COLOR_PANEL_BG = (220, 220, 240)
COLOR_BUTTON_IDLE = (180, 180, 180)
COLOR_BUTTON_ACTIVE = (150, 255, 150)
COLOR_BORDER = (0, 0, 0)
COLOR_TEXT = (0, 0, 0)

# --- Simulation Settings ---
INITIAL_AGENT_COUNT = 5
INITIAL_FOOD_COUNT = 4000
FOOD_LIFESPAN_TICKS = 2000000
FOOD_SPAWN_INTERVAL_TICKS = 50
FOOD_SPAWN_AMOUNT = 5
FOOD_ENERGY_VALUE = 20

TICK_JUMP_VALUES = [10, 50, 100, 500, 1000]

# --- Agent Settings (Initial/Default) ---
# These might eventually be per-agent traits or base values for evolution
BASE_MOVE_INTERVAL_TICKS = 3
BASE_ENERGY_DRAIN_PER_MOVE = 1 # Energy cost each time an agent moves
BASE_ENERGY_DRAIN_PER_TICK = 0.05 # Optional: energy drain just for existing each tick
BASE_MAX_AGE_TICKS = 1000 # Example maximum age before an agent dies naturally
BASE_VISION_RANGE = 5 # Default number of grid cells an agent can 'see'

BASE_MAX_ENERGY = 1000.0 # NEW: Default maximum energy an agent can have


# --- END CODE IMPLEMENTATION ---