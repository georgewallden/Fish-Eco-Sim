import pygame
import random
from config import *

DIRECTIONS = ["N", "S", "E", "W"]

class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = random.choice(DIRECTIONS)
        self.color = (0, 255, 0)

        # Tick-based movement interval
        self.move_interval_ticks = 3  # move every 3 ticks
        self.tick_counter = 0

    def move(self):
        self.tick_counter += 1
        if self.tick_counter < self.move_interval_ticks:
            return

        self.tick_counter = 0  # reset

        dx, dy = self.get_direction_delta()

        # Wrap horizontally
        self.x = (self.x + dx) % GRID_COLS

        # Clamp vertically
        new_y = self.y + dy
        if 0 <= new_y < GRID_ROWS:
            self.y = new_y

        # Random direction change
        if random.random() < 0.1:
            self.direction = random.choice(DIRECTIONS)

    def get_direction_delta(self):
        return {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "W": (-1, 0),
        }[self.direction]

    def draw(self, surface, is_selected=False):
        center_x = self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.y * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 2

        if is_selected:
            pygame.draw.circle(surface, (255, 255, 0), (center_x, center_y), radius + 3)

        pygame.draw.circle(surface, self.color, (center_x, center_y), radius)
