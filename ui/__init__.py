# ui/__init__.py
# This file makes the 'ui' directory a Python package
# It also specifies which names are publicly available and manages shared UI state

import pygame # Need pygame for event types like MOUSEBUTTONDOWN
from config import CELL_SIZE, SCREEN_WIDTH # Need constants from config

# --- Shared UI State ---
# Manage state like dropdown visibility and selected jump value centrally here
dropdown_visible = False
selected_tick_jump = 10 # Default value


# --- Import Initialization Functions ---
# Import font initialization from dropdown (or a dedicated ui_utils)
from .dropdown import init_ui_fonts # Assuming dropdown handles font init for UI


# --- Import Other UI Components ---
# Import drawing functions
from .panel import draw_panel
from .dropdown import draw_dropdown # Still need to draw the dropdown

# Import event handling functions
from .buttons import handle_button_click
from .dropdown import handle_dropdown_click


# --- UI Initialization Function ---
def init_ui():
    """Initializes all UI components that require pygame to be initialized."""
    init_ui_fonts() # Initialize fonts


# --- Main UI Drawing Function (called by main.py) ---
def draw_ui(surface, world):
    """Draws all UI elements onto the screen surface."""
    # Drawing order matters: Draw panel first, then overlay dropdown
    draw_panel(surface, world)

    # Draw dropdown if visible
    global dropdown_visible # Declare global to access the module-level variable
    if dropdown_visible:
        draw_dropdown(surface)

# --- Main UI Event Handling Function (called by main.py) ---
def handle_ui_event(event, world):
    """Handles pygame events related to the UI. Returns True if event was handled."""
    global dropdown_visible # Declare global to modify the module-level variable
    global selected_tick_jump # Declare global here too if modifying it

    handled = False # Flag to indicate if the event was consumed by the UI

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
                 col = mx // CELL_SIZE # Use CELL_SIZE from config
                 row = my // CELL_SIZE # Use CELL_SIZE from config

                 # --- FIX IS HERE ---
                 # Check if calculated coordinates are within the actual grid bounds
                 # Use world.cols and world.rows which exist, instead of world.grid.cols/rows
                 if 0 <= col < world.cols and 0 <= row < world.rows:
                     # If within bounds, attempt to select an agent at these coordinates
                     world.select_agent_at(col, row)
                     handled = True # Event handled by attempting agent selection

    # Return True if the UI handled the event, False otherwise
    return handled