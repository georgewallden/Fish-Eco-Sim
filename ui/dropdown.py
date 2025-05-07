# ui/dropdown.py
#
# Description:
# This module manages the tick jump dropdown menu that appears when the
# "Run N Ticks" button is right-clicked. It handles drawing the dropdown
# options and processing mouse clicks on those options to update the
# selected tick jump value. It also includes shared functionality for
# UI font initialization and access.
#
# Key responsibilities of this file:
# - Initialize and provide access to the main UI font.
# - Store the list of rectangles corresponding to the drawable dropdown options.
# - Draw the dropdown menu if it is currently visible.
# - Process mouse clicks to determine if a dropdown option was selected
#   or if the dropdown should be hidden.
# - Update the shared `selected_tick_jump` state upon selection.
#
# Design Philosophy/Notes:
# - Centralizes font management for the UI.
# - Works closely with `ui/__init__.py` to manage `dropdown_visible`
#   and `selected_tick_jump` shared state.
# - Uses the button definitions from `ui/buttons.py` to position the dropdown.
# - Temporarily stores dropdown option rectangles during drawing to allow
#   efficient collision detection during event handling.

# Imports Description:
# This section lists the modules imported by ui/dropdown.py and their purpose.
# - pygame: The core library, needed for font creation (`pygame.font.SysFont`),
#   text rendering (`font.render`), drawing (`pygame.draw`, `surface.blit`),
#   rectangle definition (`pygame.Rect`), and event processing (`event.pos`).
# - config: Imports `TICK_JUMP_VALUES` to define the options available in the dropdown.
# - . import dropdown_visible, selected_tick_jump: Imports shared state variables
#   from the parent `ui` package's `__init__.py`, which are read (`dropdown_visible`)
#   and modified (`selected_tick_jump`, `dropdown_visible`).
# - .buttons import BUTTONS: Imports the dictionary `BUTTONS` from `ui/buttons.py`,
#   needed to determine the position and width of the dropdown relative to the
#   "tick_jump" button.

# Code Block Descriptions:
# This section provides detailed blueprints for the code blocks implemented below.

# 1. Module-Level State Variables and Constants
# Description:
# Private module-level variables and constants used to maintain state
# within this module (like the font instance) and temporarily store
# data needed between drawing and event handling phases (like dropdown rects).
# Attributes defined in this block:
# - _font (pygame.font.Font or None): A private variable to hold the initialized Pygame font object. Initialized to None.
# - dropdown_rects (list[tuple[pygame.Rect, int]]): A list populated each frame the dropdown is drawn, storing tuples of (rectangle, value) for each dropdown option. Used for click detection.
# Process:
# `_font` is initialized by `init_ui_fonts()`. `dropdown_rects` is reset
# and populated by `draw_dropdown()`, and read by `handle_dropdown_click()`.
# Output:
# None. Defines module-level state.

# 2. Function: init_ui_fonts
# Description:
# Initializes the Pygame font instance used across the UI. This function should
# be called once after `pygame.init()`. It prevents recreating the font object
# multiple times.
# Inputs: None.
# Where Inputs Typically Come From: Called by `ui.__init__.py::init_ui`.
# Restrictions on Inputs: Must be called after `pygame.init()`.
# Other Relevant Info: Modifies the module-level `_font` variable.
#
# Description of Algorithm/Process:
# 1. Declare `_font` as `global` to modify the module-level variable.
# 2. Check if `_font` is currently `None` (meaning it hasn't been initialized yet).
# 3. If `_font` is `None`, create a new Pygame font instance using `pygame.font.SysFont(None, 24)` and assign it to `_font`.
# 4. Optional: Add initialization for other UI fonts if needed.
#
# Description of Output:
# None. Side effect is initializing the `_font` module variable.

# 3. Function: get_ui_font
# Description:
# Provides a standardized way to access the initialized UI font instance from
# other UI modules (like `ui.panel`). It includes a defensive check to ensure
# the font is initialized, although `init_ui()` in `ui/__init__.py` should
# ensure this.
# Inputs: None.
# Where Inputs Typically Come From: Called by UI drawing functions (e.g., `ui.panel::draw_panel`, `ui.dropdown::draw_dropdown`).
# Restrictions on Inputs: None.
# Other Relevant Info: Accesses the module-level `_font` variable.
#
# Description of Algorithm/Process:
# 1. Check if the module-level `_font` variable is `None`.
# 2. If it is `None`, print a warning and call `init_ui_fonts()` to initialize it (handles cases where initialization might have been missed, though less likely with the `ui.__init__.py` structure).
# 3. Return the `_font` instance.
#
# Description of Output:
# The initialized Pygame font object used for UI text. Type: pygame.font.Font.
# Output Range: A valid Pygame font object after initialization.

# 4. Function: draw_dropdown
# Description:
# Draws the tick jump dropdown menu onto the provided surface if the
# `dropdown_visible` shared state is True. It calculates the position of
# each option based on the "tick_jump" button's location and stores the
# option rectangles for click detection.
# Inputs:
#   - surface: The pygame surface to draw the dropdown onto. Type: pygame.Surface. Origin: Passed from `ui/__init__.py::draw_ui`. Restrictions: Must be a valid pygame Surface.
# Where Inputs Typically Come From: Called by `ui/__init__.py::draw_ui` if the dropdown is visible.
# Restrictions on Inputs: None.
# Other Relevant Info: Accesses and modifies the module-level `dropdown_rects` list. Accesses the shared `dropdown_visible` state and the `BUTTONS` constant.
#
# Description of Algorithm/Process:
# 1. Declare `dropdown_rects` and `dropdown_visible` as `global`.
# 2. Get the current UI font using `get_ui_font()`.
# 3. Check if `dropdown_visible` is `False`. If so, clear `dropdown_rects` and return immediately (nothing to draw).
# 4. Calculate the starting position (`x`, `y`), width, and height for the dropdown options based on `BUTTONS["tick_jump"]` and a small offset.
# 5. Reset `dropdown_rects` to an empty list.
# 6. Iterate through the `TICK_JUMP_VALUES` list from `config.py`.
# 7. For each `value` and its index `i`:
#    a. Calculate the `pygame.Rect` for the option row (`rect = pygame.Rect(x, y + i * height, width, height)`).
#    b. Append a tuple `(rect, value)` to the `dropdown_rects` list.
#    c. Draw a light gray background rectangle for the option row.
#    d. Draw a black border around the option row rectangle.
#    e. Render the text label "Run {value} Ticks" using the UI font and black color.
#    f. Draw the rendered text onto the `surface` at a slight offset within the option `rect`.
#
# Description of Output:
# None. Side effects include drawing the dropdown options onto the provided `surface`
# and populating the module-level `dropdown_rects` list.

# 5. Function: handle_dropdown_click
# Description:
# Checks if a mouse click event occurred within the bounds of any currently
# drawn dropdown option rectangle. If an option is clicked, it updates the
# shared `selected_tick_jump` value and hides the dropdown. If the dropdown
# was visible but the click was elsewhere, it hides the dropdown.
# Inputs:
#   - event: The Pygame event object, expecting a MOUSEBUTTONDOWN event with `event.pos`. Type: pygame.event.Event. Origin: Passed from `ui/__init__.py::handle_ui_event`. Restrictions: Should be a mouse button down event.
#   - world: The SimulationWorld instance. Not directly used in the current implementation, but included in the signature as it's often passed through UI event handlers. Type: world.SimulationWorld. Origin: Passed from `ui/__init__.py::handle_ui_event`. Restrictions: Must be a valid SimulationWorld object.
# Where Inputs Typically Come From: Called by `ui/__init__.py::handle_ui_event` if the dropdown is visible.
# Restrictions on Inputs: None.
# Other Relevant Info: Accesses the module-level `dropdown_rects` list and modifies the shared `selected_tick_jump` and `dropdown_visible` state variables.
#
# Description of Algorithm/Process:
# 1. Declare `selected_tick_jump` and `dropdown_visible` as `global`.
# 2. Check if `dropdown_visible` is `False`. If so, return `False` immediately (nothing to handle).
# 3. Iterate through the `dropdown_rects` list, which contains `(rect, value)` tuples for each option.
# 4. For each `(rect, value)` tuple:
#    a. Check if the event's position (`event.pos`) collides with the `rect` using `.collidepoint()`.
#    b. If a collision is detected:
#       i. Set the shared `selected_tick_jump` to the `value` associated with the clicked rectangle.
#       ii. Set `dropdown_visible` to `False` to hide the dropdown.
#       iii. Return `True` to indicate the event was handled.
# 5. If the loop finishes without finding any collision (meaning the click was while the dropdown was visible, but not on an option):
#    a. Set `dropdown_visible` to `False` to hide the dropdown.
#    b. Return `True` to indicate that the event interacted with the visible dropdown area and caused it to close (considered handled in this context).
#
# Description of Output:
# A boolean value. Type: bool.
# Output Range: `True` if the dropdown was visible and the click caused a selection or closed it, `False` only if the dropdown was not visible when the function was called.
# Side Effects: May modify the shared `selected_tick_jump` and `dropdown_visible` state variables.


# --- START CODE IMPLEMENTATION ---

# Imports:
# Standard library imports first
import pygame

# Local package imports
from config import TICK_JUMP_VALUES # Import the values from config
# Import shared UI state variables and BUTTONS from ui package
from . import dropdown_visible, selected_tick_jump
from .buttons import BUTTONS # Need BUTTONS position/size


### 1. Module-Level State Variables and Constants Implementation ###
# Private module variable to hold the font instance
_font = None

# List to store the rectangles for each dropdown option (populated during drawing)
dropdown_rects = []


### 2. Function: init_ui_fonts Implementation ###
def init_ui_fonts():
    """Initializes fonts required by the UI after pygame.init() is called."""
    global _font
    if _font is None:
        # Using None defaults to the system font
        _font = pygame.font.SysFont(None, 24)
    # You could initialize other UI-specific fonts here if needed


### 3. Function: get_ui_font Implementation ###
def get_ui_font():
    """Provides access to the initialized font."""
    # Simple check, though init_ui() in __init__ should ensure it's called
    if _font is None:
         print("Warning: UI font accessed before initialization. Call init_ui().")
         # Defensive initialization if somehow missed
         init_ui_fonts()
    return _font


### 4. Function: draw_dropdown Implementation ###
def draw_dropdown(surface):
    """Draws the dropdown menu options."""
    # Declare global to modify the module-level list and access shared state
    global dropdown_rects
    global dropdown_visible

    # Ensure the font is initialized before drawing text
    current_font = get_ui_font()

    if not dropdown_visible:
        dropdown_rects = [] # Clear previous rects if dropdown is not visible
        return # Don't draw if not visible

    # Calculate dropdown position based on the tick_jump button
    x = BUTTONS["tick_jump"].x
    y = BUTTONS["tick_jump"].bottom + 2 # Position just below the button
    width = BUTTONS["tick_jump"].width
    height = 30 # Height of each option row

    dropdown_rects = [] # Reset rects for the current draw frame
    # Use TICK_JUMP_VALUES directly from config
    for i, value in enumerate(TICK_JUMP_VALUES):
        rect = pygame.Rect(x, y + i * height, width, height)
        dropdown_rects.append((rect, value)) # Store rect and its corresponding value

        # Draw background and border for the option
        # Using hardcoded colors here, constants could be used
        pygame.draw.rect(surface, (200, 200, 200), rect) # Light gray background
        pygame.draw.rect(surface, (0, 0, 0), rect, 1) # Black border

        # Render and draw the text label for the option
        label = current_font.render(f"Run {value} Ticks", True, (0, 0, 0)) # Black text
        # Position text inside the rect
        surface.blit(label, (rect.x + 10, rect.y + 5))


### 5. Function: handle_dropdown_click Implementation ###
def handle_dropdown_click(event, world):
    """
    Checks if a dropdown option was clicked and updates the selected value.
    Returns True if an option was clicked or if click was outside dropdown (hiding it).
    Returns False only if dropdown was not visible.
    """
    # Declare global to modify shared state variables
    global selected_tick_jump, dropdown_visible

    # If the dropdown isn't visible, this function can't handle a click
    if not dropdown_visible:
        return False

    # Check if event position collides with any of the drawn dropdown option rects
    for rect, value in dropdown_rects:
        if rect.collidepoint(event.pos):
            selected_tick_jump = value # Update the shared state
            dropdown_visible = False # Hide dropdown after selection
            return True # Click was handled by selecting an option

    # If the click happened while the dropdown was visible, but didn't hit an option,
    # we should probably close the dropdown.
    dropdown_visible = False # Hide dropdown
    return True # Consider the event handled, as it interacted with the dropdown area


# --- END CODE IMPLEMENTATION ---