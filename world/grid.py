# world/grid.py
#
# Description:
# This module handles the visual representation of the simulation grid background.
# It is responsible for calculating and drawing the color gradient based on depth
# (rows) and drawing the individual grid cells onto the display surface.
#
# Key responsibilities of this file:
# - Define a function to calculate the color for a given row based on a depth gradient.
# - Define a function to draw the entire grid background onto a surface.
#
# Design Philosophy/Notes:
# - Purely a drawing module; contains no simulation logic or state.
# - Relies on constants from `config.py` for grid dimensions and colors.
# - The depth gradient provides a visual cue for the environment, potentially
#   linked to simulation mechanics in the future.

# Imports Description:
# This section lists the modules imported by world/grid.py and their purpose.
# - pygame: The core library, needed for drawing rectangles (`pygame.draw.rect`)
#   and defining them (`pygame.Rect`), and for accessing constants if using grid lines.
# - config: Imports constants (`SCREEN_WIDTH`, `SCREEN_HEIGHT`, `GRID_COLS`, `GRID_ROWS`,
#   `CELL_SIZE`, `COLOR_OCEAN_SHALLOW`, `COLOR_OCEAN_DEEP`) required for determining
#   grid size, cell size, and the gradient colors.

# Code Block Descriptions:
# This section provides detailed blueprints for the code blocks (functions)
# implemented below.

# 1. Function: get_depth_color
# Description:
# Calculates and returns an RGB color tuple representing the ocean depth
# for a given grid row. It linearly interpolates between a shallow color
# (top row) and a deep color (bottom row).
# Inputs:
#   - row: The grid row index for which to calculate the color. Type: int.
#          Origin: Passed by `draw_grid` during its row iteration.
#          Restrictions: 0 <= row < GRID_ROWS.
# Where Inputs Typically Come From: Called by `draw_grid`.
# Restrictions on Inputs: The input `row` should be a valid row index within the grid.
# Other Relevant Info: Uses `COLOR_OCEAN_SHALLOW`, `COLOR_OCEAN_DEEP`, and `GRID_ROWS` from `config.py`.
#
# Description of Algorithm/Process:
# 1. Calculate the `depth_ratio` based on the input `row` and the total number of grid rows (`GRID_ROWS`).
#    - The ratio is `row / (GRID_ROWS - 1)` to make the top row (row 0) have a ratio of ~0.0 and the bottom row (row `GRID_ROWS - 1`) have a ratio of 1.0.
#    - Includes a safe guard for `GRID_ROWS <= 1`.
# 2. Linearly interpolate the R, G, and B components of the color:
#    - For each component (R, G, B), the interpolated value is `shallow_component + (deep_component - shallow_component) * depth_ratio`.
#    - Convert the result to an integer.
# 3. Clamp each color component value to the valid 0-255 range to ensure valid RGB values.
# 4. Return the calculated color as an `(r, g, b)` tuple.
#
# Description of Output:
# An RGB color tuple representing the interpolated depth color for the input row. Type: tuple(int, int, int).
# Output Range: (0-255, 0-255, 0-255).

# 2. Function: draw_grid
# Description:
# Draws the entire grid background onto the provided surface. It iterates
# through all cells in the grid, determines the color for each cell's row
# using `get_depth_color`, and draws a colored rectangle for that cell.
# Inputs:
#   - surface: The pygame surface object to draw the grid onto. Type: pygame.Surface.
#              Origin: Passed from `SimulationWorld.draw()`.
#              Restrictions: Must be a valid pygame Surface.
# Where Inputs Typically Come From: Called by `SimulationWorld.draw()`.
# Restrictions on Inputs: None.
# Other Relevant Info: Uses `GRID_COLS`, `GRID_ROWS`, `CELL_SIZE` from `config.py`. Calls `get_depth_color`. Draws rectangles using `pygame.draw.rect`.
#
# Description of Algorithm/Process:
# 1. Iterate through each `row` from 0 up to `GRID_ROWS - 1`.
# 2. For the current `row`, call `get_depth_color(row)` to get the color for this row.
# 3. Iterate through each `col` from 0 up to `GRID_COLS - 1` within the current row loop.
# 4. For the current cell (`row`, `col`):
#    a. Calculate the pixel coordinates for the top-left corner of the cell: `x = col * CELL_SIZE`, `y = row * CELL_SIZE`.
#    b. Create a `pygame.Rect` object for the cell using its top-left coordinates and `CELL_SIZE` for width and height.
#    c. Draw a filled rectangle on the `surface` using the color obtained in step 2 and the calculated cell rectangle.
# 5. (Optional) Code is included but commented out to draw grid lines if needed.
#
# Description of Output:
# None. Side effect is drawing the grid background onto the provided `surface`.


# --- START CODE IMPLEMENTATION ---

# Imports:
# Standard library imports first
import pygame

# Local package imports
# Import necessary constants from config
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_COLS, GRID_ROWS, CELL_SIZE
# Import the colors needed for the depth gradient
from config import COLOR_OCEAN_SHALLOW, COLOR_OCEAN_DEEP


### 1. Function: get_depth_color Implementation ###
def get_depth_color(row):
    """
    Calculates a color based on the row (depth) to create a gradient.
    Interpolates between COLOR_OCEAN_SHALLOW (top) and COLOR_OCEAN_DEEP (bottom).
    """
    # Calculate the depth ratio (0.0 at top, 1.0 at bottom)
    # Ensure we don't divide by zero if GRID_ROWS is 1 (unlikely but safe)
    # Use float conversion for accurate division
    depth_ratio = float(row) / (GRID_ROWS - 1) if GRID_ROWS > 1 else 0.0

    # Linearly interpolate between the shallow and deep colors
    r = int(COLOR_OCEAN_SHALLOW[0] + (COLOR_OCEAN_DEEP[0] - COLOR_OCEAN_SHALLOW[0]) * depth_ratio)
    g = int(COLOR_OCEAN_SHALLOW[1] + (COLOR_OCEAN_DEEP[1] - COLOR_OCEAN_SHALLOW[1]) * depth_ratio)
    b = int(COLOR_OCEAN_SHALLOW[2] + (COLOR_OCEAN_DEEP[2] - COLOR_OCEAN_SHALLOW[2]) * depth_ratio)

    # Ensure colors are within the valid 0-255 range (though interpolation should handle this)
    # Redundant clamping, but safe
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))

    return (r, g, b)


### 2. Function: draw_grid Implementation ###
def draw_grid(surface):
    """
    Draws the grid background with a depth-based color gradient.
    """
    # Draw the background cells row by row
    for row in range(GRID_ROWS):
        # Get the color for this row based on its depth
        row_color = get_depth_color(row)

        # Draw each cell in the current row
        for col in range(GRID_COLS):
            # Calculate the rectangle for the current grid cell in pixels
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            # Draw the cell with the calculated depth color
            pygame.draw.rect(surface, row_color, rect)

    # Optional: Draw grid lines if you want them visible for debugging/visual aid
    # for x in range(0, SCREEN_WIDTH, CELL_SIZE):
    #     pygame.draw.line(surface, (50, 50, 50), (x, 0), (x, SCREEN_HEIGHT))
    # for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
    #     pygame.draw.line(surface, (50, 50, 50), (0, y), (SCREEN_WIDTH, y))


# --- END CODE IMPLEMENTATION ---