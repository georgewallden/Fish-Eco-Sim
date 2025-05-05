# world/food.py
# Defines the FoodPellet class

import pygame
import random
# Import specific constants from config
from config import GRID_COLS, GRID_ROWS, CELL_SIZE, COLOR_FOOD, FOOD_ENERGY_VALUE, FOOD_LIFESPAN_TICKS

class FoodPellet:
    """Represents a food source in the simulation grid."""
    # Removed random values from __init__ as spawning logic belongs in SimulationWorld
    # __init__ should take explicit position and potentially other properties
    def __init__(self, x, y, lifespan, energy_value):
        self.x = x
        self.y = y
        self.lifespan = lifespan # Max age before despawning
        self.age = 0 # Current age in ticks
        self.energy_value = energy_value # Energy provided when eaten

    def update(self):
        """Updates the food pellet's state (increments age)."""
        self.age += 1
        # Note: We no longer return a boolean here.
        # The lifespan check is done externally in SimulationWorld.

    def is_expired(self, current_tick):
        """Checks if the food pellet has reached the end of its lifespan."""
        # Using the pellet's age for lifespan check is fine
        return self.age >= self.lifespan
        # Alternative: if you stored the spawn tick, check current_tick - spawn_tick >= lifespan


    def draw(self, surface):
        """Draws the food pellet onto the given surface."""
        # Calculate pixel coordinates from grid coordinates
        cx = self.x * CELL_SIZE + CELL_SIZE // 2
        cy = self.y * CELL_SIZE + CELL_SIZE // 2
        offset = CELL_SIZE // 3 # Size of the diamond shape

        # Define the vertices of the diamond shape
        diamond = [
            (cx, cy - offset),  # top
            (cx + offset, cy),  # right
            (cx, cy + offset),  # bottom
            (cx - offset, cy),  # left
        ]

        # Draw the diamond using the configured food color
        pygame.draw.polygon(surface, COLOR_FOOD, diamond)