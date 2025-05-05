# agent/base.py
# Defines the core Agent class and its fundamental behaviors

import random # Needed for initial direction or random changes (if implemented here)
# Note: config is needed by movement.py, so the Agent class doesn't strictly
# need it unless it directly uses config constants itself.
# from config import *

from .traits import AgentTraits # Import the traits class
from .movement import move_agent, get_random_direction # Import movement logic
from .render import draw_agent   # Import rendering logic


class Agent:
    """
    Represents a single fish-like agent in the simulation.
    Has position, direction, traits, and basic behaviors (move, eat).
    """
    def __init__(self, x, y):
        """
        Initializes a new agent at a given grid position.
        """
        self.x = x
        self.y = y
        # Start with a random direction using the helper from movement.py
        self.direction = get_random_direction()

        self.traits = AgentTraits() # Assign initial traits

        self.tick_counter = 0       # Counter to track ticks for move interval
        self.alive = True           # Agent's survival status

        # --- Optional: Add fields for future features ---
        # self.food_target = None   # Could store a reference to a target food pellet
        # self.mate_target = None   # Could store a reference to a potential mate


    def update(self):
        """
        Updates the agent's state for a single simulation tick.
        Handles aging, movement timing, and energy drain.
        """
        if not self.alive:
            return # Dead agents don't update

        # Age the agent
        self.traits.age += 1
        # Check for old age death
        if self.traits.age >= self.traits.max_age:
            self.alive = False
            return # Agent dies of old age

        # Handle movement based on interval
        self.tick_counter += 1
        if self.tick_counter >= self.traits.move_interval_ticks:
            self.tick_counter = 0 # Reset counter
            # Call the movement logic function, passing this agent instance
            move_agent(self)

            # Energy drain happens *per move*, linked to the cost of movement
            # If energy should drain every tick regardless of movement,
            # subtract a small amount here *outside* this if block.
            self.traits.energy -= 1 # Energy cost per step

            # Check energy level after paying movement cost
            if self.traits.energy <= 0:
                self.alive = False
                return # Agent dies from lack of energy


        # --- Future Update Logic (Placeholder Comments) ---
        # Handle sensing environment (vision, smell)
        # Decide on next action (move towards food, flee predator, seek mate, random move)
        # Interact with environment/other agents (eat food, attempt to eat other agent, reproduce)


    def eat(self, food):
        """
        Allows the agent to consume a food source.
        Increases energy.
        """
        # Ensure food still exists and has energy
        if food and food.energy_value > 0:
            self.traits.energy += food.energy_value
            food.energy_value = 0 # Food is consumed/depleted

            # Optional: Cap energy at a maximum
            # self.traits.energy = min(self.traits.energy, self.traits.max_energy)


    def draw(self, surface, is_selected=False):
        """
        Draws the agent on the given pygame surface.
        Calls the separate rendering function.
        """
        # Call the rendering function, passing this agent instance
        draw_agent(self, surface, is_selected)