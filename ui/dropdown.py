# ui/dropdown.py
# Handles the tick jump dropdown menu logic and drawing

import pygame
from config import TICK_JUMP_VALUES # Import the values from config
# Import shared UI state variables and BUTTONS from ui package
from . import dropdown_visible, selected_tick_jump # Import the shared state
from .buttons import BUTTONS # Need BUTTONS position/size

# --- Font Initialization (Moved Here) ---
_font = None # Private module variable to hold the font instance

def init_ui_fonts():
    """Initializes fonts required by the UI after pygame.init() is called."""
    global _font
    if _font is None:
        # Using None defaults to the system font
        _font = pygame.font.SysFont(None, 24)
    # You could initialize other UI-specific fonts here if needed

def get_ui_font():
    """Provides access to the initialized font."""
    # Simple check, though init_ui() in __init__ should ensure it's called
    if _font is None:
         print("Warning: UI font accessed before initialization. Call init_ui().")
         init_ui_fonts() # Initialize if somehow missed
    return _font


# --- Dropdown State & Drawing ---
# dropdown_visible and selected_tick_jump are now managed in ui/__init__.py

# List to store the rectangles for each dropdown option
# This list is populated when the dropdown is drawn.
dropdown_rects = []

def draw_dropdown(surface):
    """Draws the dropdown menu options."""
    global dropdown_rects # Declare global to modify the module-level list
    global dropdown_visible # Use the shared state

    # Ensure the font is initialized before drawing text
    current_font = get_ui_font() # Get the font object

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
        pygame.draw.rect(surface, (200, 200, 200), rect) # Light gray background
        pygame.draw.rect(surface, (0, 0, 0), rect, 1) # Black border

        # Render and draw the text label for the option
        label = current_font.render(f"Run {value} Ticks", True, (0, 0, 0)) # Use the font object
        surface.blit(label, (rect.x + 10, rect.y + 5)) # Position text inside the rect


def handle_dropdown_click(event, world):
    """
    Checks if a dropdown option was clicked and updates the selected value.
    Returns True if an option was clicked or if click was outside dropdown (hiding it).
    Returns False only if dropdown was not visible.
    """
    global selected_tick_jump, dropdown_visible # Declare global to modify shared state

    if not dropdown_visible:
        return False # Not visible, so cannot handle click

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