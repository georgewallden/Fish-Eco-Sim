# agent/movement.py
# Handles movement logic for agents

import random
from config import * # Assumes config.py defines GRID_COLS, GRID_ROWS, etc.

DIRECTIONS = ["N", "S", "E", "W"]

def get_random_direction():
    """Returns a random cardinal direction."""
    return random.choice(DIRECTIONS)

def get_direction_delta(direction):
    """Returns the (dx, dy) tuple for a given direction."""
    return {
        "N": (0, -1), # Up
        "S": (0, 1),  # Down
        "E": (1, 0),  # Right
        "W": (-1, 0), # Left
    }.get(direction, (0, 0)) # Default to no movement for invalid direction


def move_agent(agent):
    """
    Calculates the agent's new position based on its direction.
    Applies border wrapping horizontally and clamping vertically.
    Also includes a chance for the agent to change direction.
    """
    dx, dy = get_direction_delta(agent.direction)

    # Calculate potential new position
    new_x = agent.x + dx
    new_y = agent.y + dy

    # Apply border rules
    # Horizontal wrap-around (left/right edges connect)
    agent.x = new_x % GRID_COLS

    # Vertical clamping (cannot move past top/bottom edges)
    if 0 <= new_y < GRID_ROWS:
        agent.y = new_y
    # Else: agent stays at the current y position

    # Optional: Chance to change direction after moving
    # This adds a bit of randomness to the movement pattern
    if random.random() < 0.1: # 10% chance
        agent.direction = get_random_direction()