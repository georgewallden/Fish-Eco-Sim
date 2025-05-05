# agent/render.py
# Handles the visual representation of an agent

import pygame
from config import * # Assumes config.py defines CELL_SIZE

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
        # Selection ring color (bright yellow)
        selection_color = (255, 255, 0)
        # Draw the ring slightly larger than the main body
        pygame.draw.circle(surface, selection_color, (center_x, center_y), radius + 3)

    # Determine the agent's body color based on its state
    if agent.alive:
        # Alive color (e.g., green, could be trait-driven later)
        body_color = (0, 255, 0)
    else:
        # Dead color (e.g., gray)
        body_color = (100, 100, 100)

    # Draw the agent's body
    pygame.draw.circle(surface, body_color, (center_x, center_y), radius)

    # Optional: Add visual indicators for direction or energy
    # e.g., a small triangle pointing the direction, or color intensity based on energy