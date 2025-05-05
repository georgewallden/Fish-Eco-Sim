# ui/buttons.py
# Handles button definitions and click logic

import pygame
from config import TICK_JUMP_VALUES, SCREEN_WIDTH # Need SCREEN_WIDTH for button positioning

# Import shared UI state variables from the ui package's __init__.py
from . import dropdown_visible, selected_tick_jump # Import the shared state variables
# No need to import tick_jump_values from here, it's used in dropdown.py
# and could potentially be moved to config or ui/__init__.py if needed elsewhere.
# For now, it's fine to keep using TICK_JUMP_VALUES from config directly where needed.


# Button rect definitions - Use SCREEN_WIDTH from config
# Assuming SCREEN_WIDTH is the width of the simulation grid area
BUTTONS = {
    "start": pygame.Rect(SCREEN_WIDTH + 20, 20, 160, 35),
    "pause": pygame.Rect(SCREEN_WIDTH + 20, 65, 160, 35),
    "reset": pygame.Rect(SCREEN_WIDTH + 20, 110, 160, 35),
    "tick_once": pygame.Rect(SCREEN_WIDTH + 20, 155, 160, 35),
    "tick_jump": pygame.Rect(SCREEN_WIDTH + 20, 200, 160, 35),
}

# Removed local state definitions (dropdown_visible, selected_tick_jump)
# They are now managed in ui/__init__.py

def handle_button_click(event, world):
    """
    Checks if a button was clicked and performs the corresponding action.
    Modifies the shared dropdown_visible state.
    Returns True if a button was clicked, False otherwise.
    """
    global dropdown_visible, selected_tick_jump # Declare global to modify the shared state

    # Check if the event position collides with any button rect
    if BUTTONS["start"].collidepoint(event.pos):
        world.state.paused = False
        dropdown_visible = False # Hide dropdown if clicking a button
        return True
    elif BUTTONS["pause"].collidepoint(event.pos):
        world.state.paused = True
        dropdown_visible = False # Hide dropdown if clicking a button
        return True
    elif BUTTONS["reset"].collidepoint(event.pos):
        # NOTE: world.__init__() is a crude reset. A dedicated reset method in SimulationWorld is better.
        world.__init__()
        dropdown_visible = False # Hide dropdown
        return True
    elif BUTTONS["tick_once"].collidepoint(event.pos):
        world.state.step_once()
        dropdown_visible = False # Hide dropdown
        return True
    elif BUTTONS["tick_jump"].collidepoint(event.pos):
        # Handle clicks specifically on the tick_jump button
        if event.button == 1:  # Left click performs the jump
            # Use the selected_tick_jump value from the shared state
            world.state.step_many(selected_tick_jump)
            dropdown_visible = False # Hide dropdown after action
        elif event.button == 3:  # Right click toggles dropdown visibility
            dropdown_visible = not dropdown_visible # Toggle shared state
        return True # This button click was handled

    # If no button was clicked
    return False