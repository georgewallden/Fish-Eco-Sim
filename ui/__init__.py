# ui/__init__.py
#
# Description:
# This file serves as the initialization file for the 'ui' Python package.
# It defines the public interface of the UI module, manages shared UI state,
# and orchestrates the drawing and event handling by importing and calling
# functions from its sub-modules (buttons, panel, dropdown). It provides the
# main entry points (`init_ui`, `draw_ui`, `handle_ui_event`) that the
# `main.py` script interacts with.
#
# Key responsibilities of this file:
# - Make the 'ui' directory a valid Python package.
# - Define and manage shared state variables used across UI components (e.g., dropdown visibility).
# - Import and expose necessary functions from UI sub-modules.
# - Provide a single initialization function for the UI.
# - Provide a single function to draw all UI elements in the correct order.
# - Provide a single function to handle all UI-related events, prioritizing them correctly.
#
# Design Philosophy/Notes:
# - Acts as the central coordinator for the UI package.
# - Shared state is managed here to avoid circular dependencies between sub-modules
#   that need to access/modify the same state (like dropdown_visible).
# - Delegates specific tasks (drawing panel, drawing dropdown, handling button clicks,
#   handling dropdown clicks) to dedicated sub-modules.
# - Prioritizes event handling logically (dropdown > buttons > grid click).

# Imports Description:
# This section lists the modules imported by ui/__init__.py and their purpose.
# - pygame: Needed for pygame event types (like MOUSEBUTTONDOWN) in the event handling loop.
# - config: Imports constants like CELL_SIZE and SCREEN_WIDTH needed for event handling logic (specifically determining if a click is within the grid area).
# - .dropdown.init_ui_fonts: Imports the function responsible for initializing UI fonts, necessary setup after pygame.init(). This import requires the shared state variables below to be defined first to avoid circular import errors with ui.dropdown.
# - .panel.draw_panel: Imports the function to draw the main UI panel.
# - .dropdown.draw_dropdown: Imports the function to draw the tick jump dropdown menu if visible.
# - .buttons.handle_button_click: Imports the function that checks and processes clicks on UI buttons.
# - .dropdown.handle_dropdown_click: Imports the function that checks and processes clicks on the dropdown menu options.

# Code Block Descriptions:
# This section provides detailed blueprints for the code blocks implemented below.
# These blocks define the shared state and the main functions that interface
# with the rest of the application.

# 1. Shared UI State Variables
# Description:
# Global variables within the 'ui' package used to manage shared state
# that multiple UI components might need to access or modify. Defined at
# the module level.
# Attributes defined in this block:
# - dropdown_visible (bool): Flag indicating whether the tick jump dropdown menu is currently displayed.
# - selected_tick_jump (int): The number of ticks currently selected for the "Run N Ticks" button/dropdown.
# Process:
# These variables are initialized with default values when the `ui` package is imported.
# They are modified by event handling functions (like `handle_button_click`, `handle_dropdown_click`).
# They are read by drawing functions (like `draw_dropdown`, `draw_panel`) and event handling functions.
# Output:
# None. Defines shared global state within the module.

# 2. Function: init_ui
# Description:
# Initializes necessary components for the UI that require Pygame to be
# initialized first. Currently, this involves initializing fonts used by the UI.
# Inputs: None.
# Where Inputs Typically Come From: Called once by `main.py` after `pygame.init()`.
# Restrictions on Inputs: Must be called after `pygame.init()`.
# Other Relevant Info: Essential setup step before drawing or interacting with UI elements.
#
# Description of Algorithm/Process:
# 1. Call the `init_ui_fonts()` function imported from the `dropdown` module.
#    (This function itself handles the Pygame font initialization).
#
# Description of Output:
# None. Side effect is the initialization of UI font resources.

# 3. Function: draw_ui
# Description:
# Orchestrates the drawing of all UI elements onto the given surface. It calls
# the drawing functions from sub-modules in the correct order to ensure elements
# like dropdowns overlay others.
# Inputs:
#   - surface: The pygame surface to draw on. Type: pygame.Surface. Origin: Passed from `main.py`'s drawing loop. Restrictions: Must be a valid pygame Surface.
#   - world: The SimulationWorld instance. Type: world.SimulationWorld. Origin: Passed from `main.py`'s drawing loop. Restrictions: Must be a valid SimulationWorld object (needed by `draw_panel` to display world state).
# Where Inputs Typically Come From: Called once per frame by `main.py`'s main loop during the drawing phase.
# Restrictions on Inputs: None.
# Other Relevant Info: The order of drawing calls determines which elements appear on top.
#
# Description of Algorithm/Process:
# 1. Call `draw_panel(surface, world)` to draw the main sidebar panel and its contents (buttons, text, agent info).
# 2. Check the value of the shared `dropdown_visible` state variable.
# 3. If `dropdown_visible` is `True`, call `draw_dropdown(surface)` to draw the tick jump options on top of the panel.
#
# Description of Output:
# None. Side effect is drawing UI elements onto the provided `surface`.

# 4. Function: handle_ui_event
# Description:
# Processes a single Pygame event to determine if it corresponds to a UI interaction
# (like a button click, dropdown option click, or agent selection click in the grid).
# It delegates specific event handling to sub-modules and prioritizes which UI element
# gets to handle the event.
# Inputs:
#   - event: The Pygame event object to process. Type: pygame.event.Event. Origin: Pulled from `pygame.event.get()` in `main.py`. Restrictions: Must be a valid Pygame event object.
#   - world: The SimulationWorld instance. Type: world.SimulationWorld. Origin: Passed from `main.py`'s event handling loop. Restrictions: Must be a valid SimulationWorld object (needed for actions like `world.state.toggle_pause`, `world.select_agent_at`).
# Where Inputs Typically Come From: Called by `main.py` for each event in the event queue.
# Restrictions on Inputs: None.
# Other Relevant Info: Returns `True` if the event was handled by the UI, indicating that `main.py` should potentially stop processing this event.
#
# Description of Algorithm/Process:
# 1. Initialize a boolean flag `handled` to `False`.
# 2. Check if the event type is `pygame.MOUSEBUTTONDOWN`. UI interactions are typically mouse clicks.
# 3. If it is a mouse click:
#    a. Check if the shared `dropdown_visible` state is `True`.
#    b. If the dropdown is visible, call `handle_dropdown_click(event, world)`. This function will return `True` if the click interacted with the dropdown (either clicking an option or clicking outside to close it).
#    c. If `handle_dropdown_click` returns `True`, set `handled` to `True`.
#    d. If the event was *not* handled by the dropdown (either not visible or click was outside the dropdown area but not registered as a dropdown-area interaction that closes it):
#       i. Call `handle_button_click(event, world)`. This function returns `True` if the click was on a button.
#       ii. If `handle_button_click` returns `True`, set `handled` to `True`.
#    e. If the event was *not* handled by any button:
#       i. Check if the click occurred within the simulation grid area (pixel X coordinate < SCREEN_WIDTH).
#       ii. If within the grid area, calculate the grid column and row based on the pixel coordinates and `CELL_SIZE`.
#       iii. Check if the calculated grid coordinates are within the valid bounds of the world grid (`0 <= col < world.cols` and `0 <= row < world.rows`).
#       iv. If within valid grid bounds, call `world.select_agent_at(col, row)` to attempt to select an agent at that location.
#       v. If the click was within the grid bounds, set `handled` to `True`.
# 4. Return the final value of the `handled` flag.
#
# Description of Output:
# A boolean value. Type: bool.
# Output Range: `True` if the event was processed by the UI (dropdown click, button click, or grid click for selection), `False` otherwise.
# Side Effects: May modify shared UI state variables (`dropdown_visible`, `selected_tick_jump`) by calling sub-module handlers, and may modify the `world.selected_agent` state.


# --- START CODE IMPLEMENTATION ---

# Imports:
# Standard library imports first
import pygame # Need pygame for event types like MOUSEBUTTONDOWN

# Local package imports
from config import CELL_SIZE, SCREEN_WIDTH # Need constants from config

### 1. Shared UI State Variables Implementation ###
# DEFINE THESE FIRST to avoid circular import issues with sub-modules
# that import these variables.
dropdown_visible = False
selected_tick_jump = 10 # Default value

# NOW IMPORT FROM SUB-MODULES that might rely on the above variables
# Import initialization functions
from .dropdown import init_ui_fonts
# Import drawing functions
from .panel import draw_panel
from .dropdown import draw_dropdown
# Import event handling functions
from .buttons import handle_button_click
from .dropdown import handle_dropdown_click


### 2. Function: init_ui Implementation ###
def init_ui():
    """Initializes all UI components that require pygame to be initialized."""
    init_ui_fonts() # Initialize fonts


### 3. Function: draw_ui Implementation ###
def draw_ui(surface, world):
    """Draws all UI elements onto the screen surface."""
    # Drawing order matters: Draw panel first, then overlay dropdown
    draw_panel(surface, world)

    # Draw dropdown if visible
    # Note: Accessing module-level variable via global declaration
    global dropdown_visible
    if dropdown_visible:
        draw_dropdown(surface)


### 4. Function: handle_ui_event Implementation ###
def handle_ui_event(event, world):
    """Handles pygame events related to the UI. Returns True if event was handled."""
    # Note: Modifying module-level variables requires global declaration
    global dropdown_visible
    # selected_tick_jump is modified by handle_dropdown_click, not here,
    # but declaring global is good practice if you might modify it later.
    # global selected_tick_jump

    handled = False

    if event.type == pygame.MOUSEBUTTONDOWN:
        # Check for clicks in the dropdown first IF visible
        # This prevents clicks on visible dropdown options from triggering buttons/grid underneath
        if dropdown_visible:
            # handle_dropdown_click returns True if it processed the click (either option or outside)
            if handle_dropdown_click(event, world):
                handled = True
                # handle_dropdown_click updates dropdown_visible and selected_tick_jump internally

        # If the event wasn't handled by the dropdown (either not visible or click was outside options)
        # Check for button clicks
        if not handled:
             # handle_button_click returns True if it processed a button click
             if handle_button_click(event, world):
                 handled = True
                 # handle_button_click might also toggle dropdown_visible itself

        # If the event wasn't handled by any explicit UI element (button or dropdown)
        # Check for grid clicks to select an agent
        if not handled:
            mx, my = event.pos # Get mouse click position in pixels

            # Check if click is within the grid area (left side of the screen)
            # Assuming SCREEN_WIDTH from config is the boundary between grid and panel
            if mx < SCREEN_WIDTH:
                 # Calculate grid coordinates from pixel coordinates
                 col = mx // CELL_SIZE
                 row = my // CELL_SIZE

                 # Check if calculated coordinates are within the actual grid bounds
                 # Use world.cols and world.rows which exist on the SimulationWorld object
                 if 0 <= col < world.cols and 0 <= row < world.rows:
                     # If within bounds, attempt to select an agent at these coordinates
                     world.select_agent_at(col, row)
                     handled = True # Event handled by attempting agent selection

    # Return True if the UI handled the event, False otherwise
    return handled


# --- END CODE IMPLEMENTATION ---