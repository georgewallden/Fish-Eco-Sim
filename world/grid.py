# world/grid.py
# Handles drawing the grid background and depth gradient

import pygame
# Import necessary constants from config
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_COLS, GRID_ROWS, CELL_SIZE
# Import the colors needed for the depth gradient
from config import COLOR_OCEAN_SHALLOW, COLOR_OCEAN_DEEP


def get_depth_color(row):
    """
    Calculates a color based on the row (depth) to create a gradient.
    Interpolates between COLOR_OCEAN_SHALLOW (top) and COLOR_OCEAN_DEEP (bottom).
    """
    # Calculate the depth ratio (0.0 at top, 1.0 at bottom)
    # Ensure we don't divide by zero if GRID_ROWS is 1 (unlikely but safe)
    depth_ratio = row / (GRID_ROWS - 1) if GRID_ROWS > 1 else 0.0

    # Linearly interpolate between the shallow and deep colors
    r = int(COLOR_OCEAN_SHALLOW[0] + (COLOR_OCEAN_DEEP[0] - COLOR_OCEAN_SHALLOW[0]) * depth_ratio)
    g = int(COLOR_OCEAN_SHALLOW[1] + (COLOR_OCEAN_DEEP[1] - COLOR_OCEAN_SHALLOW[1]) * depth_ratio)
    b = int(COLOR_OCEAN_SHALLOW[2] + (COLOR_OCEAN_DEEP[2] - COLOR_OCEAN_SHALLOW[2]) * depth_ratio)

    # Ensure colors are within the valid 0-255 range (though interpolation should handle this)
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))

    return (r, g, b)


def draw_grid(surface):
    """
    Draws the grid background with a depth-based color gradient.
    """
    # Draw the background cells
    for row in range(GRID_ROWS):
        # Get the color for this row based on its depth
        row_color = get_depth_color(row)

        for col in range(GRID_COLS):
            # Calculate the rectangle for the current grid cell
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            # Draw the cell with the calculated depth color
            pygame.draw.rect(surface, row_color, rect)

    # Optional: Draw grid lines if you want them visible
    # for x in range(0, SCREEN_WIDTH, CELL_SIZE):
    #     pygame.draw.line(surface, (50, 50, 50), (x, 0), (x, SCREEN_HEIGHT))
    # for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
    #     pygame.draw.line(surface, (50, 50, 50), (0, y), (SCREEN_WIDTH, y))