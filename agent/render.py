# agent/render.py
#
# Description:
# This module is solely responsible for the visual representation of an Agent
# on the Pygame surface. It takes an Agent object and drawing parameters (like
# the surface and selection status) and uses Pygame drawing functions to
# render the agent's shape, color, and any visual indicators (like a selection ring).
#
# Key responsibilities of this file:
# - Define a function to draw a single agent.
# - Calculate agent pixel position and size based on grid coordinates and CELL_SIZE.
# - Visually represent agent state (alive/dead) and selection status.
#
# Design Philosophy/Notes:
# - Purely a drawing module; contains no simulation logic, state, or behavior.
# - Relies on data provided by the Agent instance and constants from `config.py`.
# - The drawing logic is separated from the Agent class itself to keep the Agent
#   class focused on its simulation state and behavior.

# Imports Description:
# This section lists the modules imported by agent/render.py and their purpose.
# - pygame: The core library, needed for drawing circles (`pygame.draw.circle`)
#   and defining shapes.
# - config: Imports constants (`CELL_SIZE`, `COLOR_AGENT_ALIVE`, `COLOR_AGENT_DEAD`,
#   `COLOR_SELECTED_RING`) necessary for determining size, position scaling, and colors.

# Code Block Descriptions:
# This section provides detailed blueprints for the code blocks (functions)
# implemented below.

# 1. Function: draw_agent
# Description:
# Draws a single agent onto the specified Pygame surface. The agent is
# rendered as a circle with a color indicating its alive/dead status.
# An additional ring is drawn around the agent if it is currently selected.
# Inputs:
#   - agent: The Agent instance to be drawn. Type: agent.Agent.
#            Origin: Passed from `Agent.draw()`.
#            Restrictions: Must be a valid Agent object with `x`, `y`, and `alive` attributes.
#   - surface: The pygame surface object to draw on. Type: pygame.Surface.
#              Origin: Passed from `Agent.draw()`.
#              Restrictions: Must be a valid pygame Surface.
#   - is_selected (optional): A boolean flag indicating if the agent should be drawn with a selection indicator. Type: bool.
#                           Origin: Passed from `Agent.draw()`.
#                           Restrictions: Must be True or False. Default: False.
# Where Inputs Typically Come From: Called by `Agent.draw()`.
# Restrictions on Inputs: None.
# Other Relevant Info: Uses `CELL_SIZE`, `COLOR_AGENT_ALIVE`, `COLOR_AGENT_DEAD`, and `COLOR_SELECTED_RING` from `config.py`.
#
# Description of Algorithm/Process:
# 1. Calculate the pixel center coordinates (`center_x`, `center_y`) of the grid cell where the agent is located, using `agent.x`, `agent.y`, and `CELL_SIZE`.
# 2. Determine the radius for the agent's body circle based on `CELL_SIZE` (slightly smaller than half a cell).
# 3. Check the value of the `is_selected` boolean flag.
# 4. If `is_selected` is `True`:
#    a. Define the `selection_color` (e.g., yellow from config).
#    b. Draw a circle on the `surface` using the `selection_color`, centered at (`center_x`, `center_y`), with a radius slightly larger than the body radius (to form a ring).
# 5. Determine the agent's body color based on its `agent.alive` status. Use `COLOR_AGENT_ALIVE` if True, `COLOR_AGENT_DEAD` if False (from config).
# 6. Draw the agent's main body circle on the `surface` using the determined `body_color`, centered at (`center_x`, `center_y`), with the calculated `radius`.
# 7. (Optional) Placeholder comment for adding future visual indicators (direction, energy).
#
# Description of Output:
# None. Side effect is drawing the agent's visual representation onto the provided `surface`.


# --- START CODE IMPLEMENTATION ---

# Imports:
# Standard library imports first
import pygame

# Local package imports
# Import constants needed for size, position, and colors
from config import CELL_SIZE, COLOR_AGENT_ALIVE, COLOR_AGENT_DEAD, COLOR_SELECTED_RING


### 1. Function: draw_agent Implementation ###
def draw_agent(agent, surface, is_selected=False):
    """
    Draws the agent onto the given surface.
    Position is based on agent.x, agent.y grid coordinates.
    Visuals change based on agent state (alive/dead) and selection status.
    """
    # Calculate pixel coordinates from grid coordinates
    center_x = agent.x * CELL_SIZE + CELL_SIZE // 2
    center_y = agent.y * CELL_SIZE + CELL_SIZE // 2
    radius = CELL_SIZE // 2 - 2 # Draw slightly smaller than the cell

    # Draw a selection ring if the agent is selected
    if is_selected:
        # Selection ring color (bright yellow from config)
        selection_color = COLOR_SELECTED_RING
        # Draw the ring slightly larger than the main body circle
        pygame.draw.circle(surface, selection_color, (center_x, center_y), radius + 3)

    # Determine the agent's body color based on its state
    if agent.alive:
        # Alive color (e.g., green from config)
        body_color = COLOR_AGENT_ALIVE
    else:
        # Dead color (e.g., gray from config)
        body_color = COLOR_AGENT_DEAD

    # Draw the agent's body circle
    pygame.draw.circle(surface, body_color, (center_x, center_y), radius)

    # Optional: Add visual indicators for direction or energy here in the future
    # e.g., draw a small shape pointing the direction, or change body color intensity based on energy


# --- END CODE IMPLEMENTATION ---