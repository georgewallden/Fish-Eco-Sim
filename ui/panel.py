# ui/panel.py
#
# Description:
# This module is responsible for drawing the main UI panel on the right side
# of the simulation window. It draws the panel background, static elements
# like the simulation tick count, and dynamic elements like the selected
# agent's information. It also calls helper functions to draw the buttons.
#
# Key responsibilities of this file:
# - Draw the background rectangle for the UI panel.
# - Draw the simulation tick counter.
# - Draw information about the currently selected agent.
# - Call helper functions to draw individual buttons.
#
# Design Philosophy/Notes:
# - Focuses solely on the visual representation of the main panel area.
# - Relies on shared UI state (like `selected_tick_jump` and the selected
#   agent held in `world`) and constants (`config`, `BUTTONS` from `buttons.py`).
# - Delegates button drawing to a helper function within this file for
#   consistency and reuse.

# Imports Description:
# This section lists the modules imported by ui/panel.py and their purpose.
# - pygame: The core library, needed for drawing functions (`pygame.draw`, `surface.blit`) and rectangle definition (`pygame.Rect`).
# - config: Imports constants (`SCREEN_WIDTH`, `SCREEN_HEIGHT`, `PANEL_WIDTH`) necessary to determine the panel's size and position.
# - . import selected_tick_jump: Imports the shared state variable `selected_tick_jump` from the parent `ui` package's `__init__.py` file, needed to display the text on the tick jump button.
# - .buttons import BUTTONS: Imports the dictionary `BUTTONS` from `ui/buttons.py`, which contains the `pygame.Rect` objects defining the position and size of each button, used for drawing them correctly.
# - .dropdown import get_ui_font: Imports the function `get_ui_font` which provides access to the initialized Pygame font used for all UI text rendering.

# Code Block Descriptions:
# This section provides detailed blueprints for the code blocks (functions)
# implemented below.

# 1. Function: draw_button
# Description:
# A helper function used internally by `draw_panel` to render a single button
# with a background, border, and centered text label. It can optionally draw
# the button in an 'active' visual state.
# Inputs:
#   - surface: The pygame surface to draw the button onto. Type: pygame.Surface. Origin: Passed from `draw_panel`. Restrictions: Must be a valid pygame Surface.
#   - rect: The pygame.Rect defining the position and dimensions of the button. Type: pygame.Rect. Origin: Passed from the `BUTTONS` dictionary imported from `ui/buttons.py`. Restrictions: Must be a valid pygame Rect.
#   - text: The text label to display on the button. Type: str. Origin: Hardcoded string values for button labels. Restrictions: Can be any string.
#   - active (optional): A boolean flag determining the button's background color (visually indicating state like paused/running). Type: bool. Origin: Passed based on the current simulation state (`world.state.paused`). Restrictions: Must be True or False. Default: True.
# Where Inputs Typically Come From: Called multiple times by `draw_panel` for each button.
# Restrictions on Inputs: `rect` should define a drawable area within the surface.
# Other Relevant Info: Uses the `get_ui_font()` helper to ensure consistent font usage.
#
# Description of Algorithm/Process:
# 1. Get the current UI font using `get_ui_font()`.
# 2. Determine the button's background color based on the `active` parameter.
# 3. Draw a filled rectangle for the button background using the determined color and the input `rect`.
# 4. Draw a black border around the button rectangle.
# 5. Render the input `text` using the UI font and black color.
# 6. Get the bounding rectangle for the rendered text label.
# 7. Center the text label's rectangle within the button's `rect`.
# 8. Draw the rendered text label onto the `surface` at its centered position.
#
# Description of Output:
# None. Side effect is drawing a button onto the provided `surface`.

# 2. Function: draw_panel
# Description:
# The main drawing function for the UI panel. It draws the panel's background,
# all static text (like "Tick:"), dynamic text (like the current tick count
# and selected agent info), and calls `draw_button` for each of the defined
# buttons.
# Inputs:
#   - surface: The pygame surface to draw the panel onto. Type: pygame.Surface. Origin: Passed from `ui/__init__.py`'s `draw_ui`. Restrictions: Must be a valid pygame Surface.
#   - world: The SimulationWorld instance containing the current simulation state (tick count) and the currently selected agent. Type: world.SimulationWorld. Origin: Passed from `ui/__init__.py`'s `draw_ui`. Restrictions: Must be a valid SimulationWorld object with `state` and `selected_agent` attributes.
# Where Inputs Typically Come From: Called once per frame by `ui/__init__.py::draw_ui`.
# Restrictions on Inputs: None.
# Other Relevant Info: Positions all elements relative to the `SCREEN_WIDTH` constant to place them in the panel area. Accesses the shared `selected_tick_jump` state.
#
# Description of Algorithm/Process:
# 1. Define the rectangle covering the entire panel area using `SCREEN_WIDTH`, `0`, `PANEL_WIDTH`, and `SCREEN_HEIGHT`.
# 2. Draw a filled rectangle for the panel background using the defined panel color and the panel rectangle.
# 3. Get the current UI font using `get_ui_font()` for general panel text.
# 4. Call `draw_button` for each button defined in the `BUTTONS` dictionary, passing the surface, the button's rectangle, its text label, and the appropriate active state (based on `world.state.paused` for Start/Pause). The text for the "Run Ticks" button includes the value of the shared `selected_tick_jump`.
# 5. Render the "Tick: {count}" text using the UI font and draw it onto the surface at a fixed position within the panel, using `world.state.tick_count`.
# 6. Check if `world.selected_agent` is not `None`.
# 7. If an agent is selected:
#    a. Render and draw the "Selected Agent:" header text using the UI font.
#    b. Render and draw lines of text displaying the selected agent's properties (`x`, `y`, `direction`, `traits.energy`, `traits.move_interval_ticks`, `traits.age`), retrieving the values from the `world.selected_agent` object and formatting them as needed (e.g., energy to 1 decimal place). Position these lines below the header at increasing Y offsets.
# 8. If no agent is selected, the agent info section remains empty.
#
# Description of Output:
# None. Side effect is drawing the UI panel and its contents onto the provided `surface`.


# --- START CODE IMPLEMENTATION ---

# Imports:
# Standard library imports first
import pygame

# Local package imports
from config import SCREEN_WIDTH, SCREEN_HEIGHT, PANEL_WIDTH # Import constants for panel dimensions
from . import selected_tick_jump # Import the shared state variable for the tick jump button text
from .buttons import BUTTONS # Import button rectangles for drawing
from .dropdown import get_ui_font # Import the font getter function


### 1. Function: draw_button Implementation ###
def draw_button(surface, rect, text, active=True):
    """Helper function to draw a standard button."""
    current_font = get_ui_font()

    # Choose button color based on active state
    # Using constants might be better than hardcoded tuples here, but matches original code
    color = (180, 180, 180) if active else (100, 100, 100)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, (0, 0, 0), rect, 2) # Black border

    # Render and draw the text label
    label = current_font.render(text, True, (0, 0, 0)) # Black text
    label_rect = label.get_rect(center=rect.center)
    surface.blit(label, label_rect)


### 2. Function: draw_panel Implementation ###
def draw_panel(surface, world):
    """Draws the entire UI panel on the right side of the screen."""
    # Define the rectangle for the panel area
    panel_rect = pygame.Rect(SCREEN_WIDTH, 0, PANEL_WIDTH, SCREEN_HEIGHT)
    # Using a hardcoded color tuple here, COLOR_PANEL_BG from config could be used instead
    pygame.draw.rect(surface, (220, 220, 240), panel_rect) # Panel background

    current_font = get_ui_font() # Get the font for text rendering

    # --- Draw Buttons ---
    draw_button(surface, BUTTONS["start"], "Start", world.state.paused)
    draw_button(surface, BUTTONS["pause"], "Pause", not world.state.paused)
    draw_button(surface, BUTTONS["reset"], "Reset")
    draw_button(surface, BUTTONS["tick_once"], "Tick Once")
    draw_button(surface, BUTTONS["tick_jump"], f"Run {selected_tick_jump} Ticks")

    # --- Draw Simulation Tick Count ---
    tick_text = current_font.render(f"Tick: {world.state.tick_count}", True, (0, 0, 0))
    surface.blit(tick_text, (SCREEN_WIDTH + 10, 250)) # Position below buttons

    # --- Draw Selected Agent Info ---
    if world.selected_agent:
        a = world.selected_agent
        surface.blit(current_font.render("Selected Agent:", True, (0, 0, 0)), (SCREEN_WIDTH + 10, 300))
        surface.blit(current_font.render(f"Pos: ({a.x}, {a.y})", True, (0, 0, 0)), (SCREEN_WIDTH + 10, 325))
        surface.blit(current_font.render(f"Dir: {a.direction}", True, (0, 0, 0)), (SCREEN_WIDTH + 10, 350))
        surface.blit(current_font.render(f"Energy: {a.traits.energy:.1f}", True, (0, 0, 0)), (SCREEN_WIDTH + 10, 375))
        surface.blit(current_font.render(f"Speed: {a.traits.move_interval_ticks} ticks", True, (0, 0, 0)), (SCREEN_WIDTH + 10, 400))
        surface.blit(current_font.render(f"Age: {a.traits.age}", True, (0, 0, 0)), (SCREEN_WIDTH + 10, 425))

    # NOTE: The dropdown drawing is called in ui/__init__.py's draw_ui
    # after draw_panel, ensuring it is drawn on top of the panel.
    # No need to call draw_dropdown here directly.


# --- END CODE IMPLEMENTATION ---