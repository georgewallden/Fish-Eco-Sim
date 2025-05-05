# ui/panel.py
# Handles drawing the main UI panel and its contents (buttons, info)

import pygame
# Import constants from config needed for drawing the panel
from config import SCREEN_WIDTH, SCREEN_HEIGHT, PANEL_WIDTH # Assuming PANEL_WIDTH is defined for the sidebar width

# Import shared UI state variables and button definitions
from . import selected_tick_jump # Import the shared state
from .buttons import BUTTONS # Need BUTTONS rects for drawing
# dropdown_visible and draw_dropdown are handled in ui/__init__.py's draw_ui
# We don't need to import them here if __init__.py manages the drawing order.
# from .dropdown import dropdown_visible, draw_dropdown # Removed direct import here

# Import the font getter function
from .dropdown import get_ui_font # Import the font getter


# --- Font is now handled by get_ui_font() ---
# Removed local font setup: font = pygame.font.SysFont(None, 24)


def draw_button(surface, rect, text, active=True):
    """Helper function to draw a standard button."""
    # Get the font for rendering button text
    current_font = get_ui_font() # Use the getter function

    # Choose button color based on active state
    color = (180, 180, 180) if active else (100, 100, 100) # Gray if active, darker gray if inactive
    pygame.draw.rect(surface, color, rect) # Draw button background
    pygame.draw.rect(surface, (0, 0, 0), rect, 2) # Draw button border (2px thick)

    # Render and draw the text label for the button
    label = current_font.render(text, True, (0, 0, 0)) # Use the font object, Black text
    # Center the text label within the button rectangle
    label_rect = label.get_rect(center=rect.center)
    surface.blit(label, label_rect)


def draw_panel(surface, world):
    """Draws the entire UI panel on the right side of the screen."""
    # Define the rectangle for the panel area
    # Use SCREEN_WIDTH as the starting X for the panel
    panel_rect = pygame.Rect(SCREEN_WIDTH, 0, PANEL_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(surface, (220, 220, 240), panel_rect) # Draw light blue panel background

    # Get the font for general panel text (tick count, agent info)
    current_font = get_ui_font() # Use the getter function

    # --- Draw Buttons ---
    # Use the BUTTONS dict and the draw_button helper function
    draw_button(surface, BUTTONS["start"], "Start", world.state.paused)
    draw_button(surface, BUTTONS["pause"], "Pause", not world.state.paused)
    draw_button(surface, BUTTONS["reset"], "Reset")
    draw_button(surface, BUTTONS["tick_once"], "Tick Once")
    # Use the shared selected_tick_jump state for the button text
    draw_button(surface, BUTTONS["tick_jump"], f"Run {selected_tick_jump} Ticks")

    # --- Draw Simulation Tick Count ---
    # Render and draw the tick count text
    tick_text = current_font.render(f"Tick: {world.state.tick_count}", True, (0, 0, 0)) # Use the font object
    surface.blit(tick_text, (SCREEN_WIDTH + 10, 250)) # Position below buttons

    # --- Draw Selected Agent Info ---
    # Check if an agent is currently selected
    if world.selected_agent:
        a = world.selected_agent # Shorthand for the selected agent object
        # Render and draw agent info lines
        surface.blit(current_font.render("Selected Agent:", True, (0, 0, 0)), (SCREEN_WIDTH + 10, 300)) # Header
        surface.blit(current_font.render(f"Pos: ({a.x}, {a.y})", True, (0, 0, 0)), (SCREEN_WIDTH + 10, 325)) # Position
        surface.blit(current_font.render(f"Dir: {a.direction}", True, (0, 0, 0)), (SCREEN_WIDTH + 10, 350)) # Direction
        # Format energy to one decimal place for cleaner display
        surface.blit(current_font.render(f"Energy: {a.traits.energy:.1f}", True, (0, 0, 0)), (SCREEN_WIDTH + 10, 375)) # Energy
        surface.blit(current_font.render(f"Speed: {a.traits.move_interval_ticks} ticks", True, (0, 0, 0)), (SCREEN_WIDTH + 10, 400)) # Speed (move interval)
        surface.blit(current_font.render(f"Age: {a.traits.age}", True, (0, 0, 0)), (SCREEN_WIDTH + 10, 425)) # Age


    # NOTE: The dropdown drawing is called in ui/__init__.py's draw_ui
    # after draw_panel, ensuring it is drawn on top of the panel.
    # No need to call draw_dropdown here directly.