# ui/buttons.py
#
# Description:
# This module defines the rectangles for all UI buttons in the panel and
# handles the logic for what happens when a button is clicked. It interacts
# with the simulation state (`world.state`) to trigger actions like pausing,
# starting, resetting, or stepping the simulation. It also manages the
# visibility state of the tick jump dropdown menu.
#
# Key responsibilities of this file:
# - Define the position and size of each interactive button using Pygame Rects.
# - Provide a single function to check if a given mouse click event falls
#   within any button's area.
# - Execute the appropriate simulation action based on which button was clicked.
# - Manage the `dropdown_visible` shared state for the tick jump button.
#
# Design Philosophy/Notes:
# - Separates button definition (position/size) from drawing (handled in `panel.py`)
#   and core UI orchestration (handled in `ui/__init__.py`).
# - Uses a dictionary (`BUTTONS`) for easy access to button geometries.
# - Relies on shared state (`dropdown_visible`, `selected_tick_jump`) managed
#   in the parent package's `__init__.py`.

# Imports Description:
# This section lists the modules imported by ui/buttons.py and their purpose.
# - pygame: Needed for `pygame.Rect` to define button areas and `event.pos`/`event.button` to process clicks.
# - config: Imports constants (`SCREEN_WIDTH`) needed to position buttons relative to the simulation grid boundary.
# - . import dropdown_visible, selected_tick_jump: Imports shared state variables from the parent `ui` package's `__init__.py`, which are modified by `handle_button_click`.

# Code Block Descriptions:
# This section provides detailed blueprints for the code blocks implemented below.

# 1. Constant: BUTTONS
# Description:
# A dictionary containing `pygame.Rect` objects that define the screen coordinates
# and dimensions for each interactive button in the UI panel. The keys are
# descriptive names for the buttons (e.g., "start", "pause").
# Attributes defined in this block:
# - BUTTONS (dict[str, pygame.Rect]): Dictionary mapping button names to their Pygame Rects.
# Process:
# Defined as a global constant when the module is imported. The Rect positions
# are calculated based on the `SCREEN_WIDTH` constant to place them correctly
# within the UI panel area.
# Output:
# None. Defines a global constant available for import by other modules (like `ui.panel`).

# 2. Function: handle_button_click
# Description:
# Checks if a mouse click event occurred within the bounds of any defined button.
# If a button is clicked, it executes the corresponding simulation action by
# interacting with the `world` object and potentially modifies the shared UI state.
# Inputs:
#   - event: The Pygame event object, specifically expecting a MOUSEBUTTONDOWN event with `event.pos` (click coordinates) and potentially `event.button` (for left/right click). Type: pygame.event.Event. Origin: Passed from `ui/__init__.py::handle_ui_event`. Restrictions: Should be a mouse button down event for click detection.
#   - world: The SimulationWorld instance, needed to interact with its state (e.g., `world.state.paused`, `world.__init__`, `world.state.step_once`, `world.state.step_many`). Type: world.SimulationWorld. Origin: Passed from `ui/__init__.py::handle_ui_event`. Restrictions: Must be a valid SimulationWorld object with a `state` attribute.
# Where Inputs Typically Come From: Called by `ui/__init__.py::handle_ui_event` if the click wasn't handled by the dropdown.
# Restrictions on Inputs: None.
# Other Relevant Info: Uses the `BUTTONS` constant defined in this module. Modifies the shared `dropdown_visible` and `selected_tick_jump` state variables.
#
# Description of Algorithm/Process:
# 1. Declare the shared state variables `dropdown_visible` and `selected_tick_jump` as `global` to allow modification.
# 2. Check if the event's position (`event.pos`) collides with the `pygame.Rect` of the "start" button using `.collidepoint()`.
# 3. If "start" is clicked:
#    - Set `world.state.paused` to `False`.
#    - Set `dropdown_visible` to `False` to hide the dropdown.
#    - Return `True` to indicate the event was handled.
# 4. Else, check for collision with the "pause" button.
# 5. If "pause" is clicked:
#    - Set `world.state.paused` to `True`.
#    - Set `dropdown_visible` to `False`.
#    - Return `True`.
# 6. Else, check for collision with the "reset" button.
# 7. If "reset" is clicked:
#    - Call `world.__init__()` to reset the simulation state (Note: This is a simple reset, calling a dedicated `world.reset()` method would be better practice).
#    - Set `dropdown_visible` to `False`.
#    - Return `True`.
# 8. Else, check for collision with the "tick_once" button.
# 9. If "tick_once" is clicked:
#    - Call `world.state.step_once()` to queue a single simulation step.
#    - Set `dropdown_visible` to `False`.
#    - Return `True`.
# 10. Else, check for collision with the "tick_jump" button.
# 11. If "tick_jump" is clicked:
#     a. Check the mouse button: if it's button 1 (left click):
#        - Call `world.state.step_many()`, passing the value of the shared `selected_tick_jump`.
#        - Set `dropdown_visible` to `False` to hide the dropdown after executing the jump.
#     b. If it's button 3 (right click):
#        - Toggle the boolean value of `dropdown_visible`.
#     c. Return `True` to indicate the event was handled by this button.
# 12. If the click did not collide with any defined button after checking all of them, return `False`.
#
# Description of Output:
# A boolean value. Type: bool.
# Output Range: `True` if a button was clicked and handled, `False` otherwise.
# Side Effects: Modifies `world.state` (`paused`, `pending_ticks`), potentially re-initializes `world`, and modifies the shared `dropdown_visible` state.


# --- START CODE IMPLEMENTATION ---

# Imports:
# Standard library imports first
import pygame

# Local package imports
from config import TICK_JUMP_VALUES, SCREEN_WIDTH # Need SCREEN_WIDTH for button positioning
# Import shared UI state variables from the ui package's __init__.py
from . import dropdown_visible, selected_tick_jump


### 1. Constant: BUTTONS Implementation ###
# Button rect definitions - Use SCREEN_WIDTH from config to position in panel
BUTTONS = {
    "start": pygame.Rect(SCREEN_WIDTH + 20, 20, 160, 35),
    "pause": pygame.Rect(SCREEN_WIDTH + 20, 65, 160, 35),
    "reset": pygame.Rect(SCREEN_WIDTH + 20, 110, 160, 35),
    "tick_once": pygame.Rect(SCREEN_WIDTH + 20, 155, 160, 35),
    "tick_jump": pygame.Rect(SCREEN_WIDTH + 20, 200, 160, 35),
}


### 2. Function: handle_button_click Implementation ###
def handle_button_click(event, world):
    """
    Checks if a button was clicked and performs the corresponding action.
    Modifies the shared dropdown_visible state.
    Returns True if a button was clicked, False otherwise.
    """
    # Declare global to modify the shared state variables from ui/__init__.py
    global dropdown_visible, selected_tick_jump

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
        world.__init__() # This re-runs the SimulationWorld constructor
        dropdown_visible = False # Hide dropdown
        return True
    elif BUTTONS["tick_once"].collidepoint(event.pos):
        world.state.step_once() # Queue a single step
        dropdown_visible = False # Hide dropdown
        return True
    elif BUTTONS["tick_jump"].collidepoint(event.pos):
        # Handle clicks specifically on the tick_jump button
        if event.button == 1:  # Left click performs the jump
            # Use the selected_tick_jump value from the shared state
            world.state.step_many(selected_tick_jump) # Queue multiple steps
            dropdown_visible = False # Hide dropdown after action
        elif event.button == 3:  # Right click toggles dropdown visibility
            dropdown_visible = not dropdown_visible # Toggle shared state
        return True # This button click was handled

    # If no button was clicked, return False
    return False


# --- END CODE IMPLEMENTATION ---