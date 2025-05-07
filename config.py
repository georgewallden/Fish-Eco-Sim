# config.py
# Global constants for the simulation

# --- Display Settings ---
SCREEN_WIDTH = 1920  # Width of the simulation grid area in pixels
SCREEN_HEIGHT = 1080 # Height of the simulation grid area in pixels
PANEL_WIDTH = 200   # Width of the UI panel on the right

# Derived total window width (used when setting up the pygame display)
TOTAL_SCREEN_WIDTH = SCREEN_WIDTH + PANEL_WIDTH

FPS = 30 # Frames per second

# --- Grid Settings ---
GRID_COLS = 192 # Number of columns in the grid
GRID_ROWS = 108 # Number of rows in the grid

# Derived cell size (ensure SCREEN_WIDTH/HEIGHT are divisible by GRID_COLS/ROWS)
CELL_SIZE = SCREEN_WIDTH // GRID_COLS
# You might want to add an assertion here to check if SCREEN_WIDTH % GRID_COLS == 0
# and SCREEN_HEIGHT % GRID_ROWS == 0 to ensure cells are perfect squares/integers
# assert SCREEN_WIDTH % GRID_COLS == 0, "SCREEN_WIDTH must be divisible by GRID_COLS"
# assert SCREEN_HEIGHT % GRID_ROWS == 0, "SCREEN_HEIGHT must be divisible by GRID_ROWS"


# --- Colors ---
# Define standard colors as RGB tuples (0-255)
COLOR_OCEAN_DEEP = (10, 20, 80)   # Dark blue for the bottom depth gradient
COLOR_OCEAN_SHALLOW = (50, 150, 250) # Light blue for the top depth gradient
COLOR_FOOD = (255, 0, 0) # Red for food pellets
COLOR_AGENT_ALIVE = (0, 255, 0) # Green for alive agents
COLOR_AGENT_DEAD = (100, 100, 100) # Gray for dead agents
COLOR_SELECTED_RING = (255, 255, 0) # Yellow for selection ring
COLOR_PANEL_BG = (220, 220, 240) # Light gray-blue for panel background
COLOR_BUTTON_IDLE = (180, 180, 180) # Medium gray for inactive buttons
COLOR_BUTTON_ACTIVE = (150, 255, 150) # Light green for active state (optional)
COLOR_BORDER = (0, 0, 0) # Black for borders (used for buttons, grid lines potentially)
COLOR_TEXT = (0, 0, 0) # Black for text

# --- Simulation Settings ---
INITIAL_AGENT_COUNT = 1 # Number of agents to start with
INITIAL_FOOD_COUNT = 2000  # Number of food pellets to start with
FOOD_LIFESPAN_TICKS = 2000000 # How long food lasts if not eaten (in simulation ticks)
FOOD_SPAWN_INTERVAL_TICKS = 50 # How often new food attempts to spawn
FOOD_SPAWN_AMOUNT = 5 # How many food pellets spawn at once when spawning
FOOD_ENERGY_VALUE = 20 # How much energy a food pellet provides when eaten

# Tick jump options for the UI dropdown menu
TICK_JUMP_VALUES = [10, 50, 100, 500, 1000]

# --- Agent Settings (Initial/Default) ---
# These might eventually be per-agent traits or base values for evolution
BASE_MOVE_INTERVAL_TICKS = 3 # Default ticks between agent movements
BASE_ENERGY_DRAIN_PER_MOVE = 1 # Energy cost each time an agent moves
BASE_ENERGY_DRAIN_PER_TICK = 0.05 # Optional: energy drain just for existing each tick
BASE_MAX_AGE_TICKS = 1000 # Example maximum age before an agent dies naturally