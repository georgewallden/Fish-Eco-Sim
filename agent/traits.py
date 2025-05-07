# agent/traits.py
#
# Description:
# This module defines the `AgentTraits` class, which serves as a container
# for all the characteristics and numerical statistics (traits) that define
# an individual agent's capabilities, needs, and current state (beyond position
# and basic lifecycle). Traits can influence movement speed, energy levels,
# lifespan, sensing abilities, and potentially future interactions like size,
# attack strength, and defense.
#
# Key responsibilities of this file:
# - Define the `AgentTraits` class to hold agent attributes.
# - Initialize agent traits with base values from `config.py`.
# - Provide a structure for adding more complex, potentially genetic, traits in the future.
#
# Design Philosophy/Notes:
# - Decouples agent properties from the main `Agent` class logic.
# - Centralizes trait definitions for easier management and modification
#   (e.g., for evolution/mutation mechanisms later).
# - Traits are stored as instance attributes, allowing each agent to have unique values.

# Imports Description:
# This section lists the modules imported by agent/traits.py and their purpose.
# - config: Imports various `BASE_*` constants needed to initialize the default values of the agent's traits.

# Code Block Descriptions:
# This section provides detailed blueprints for the code blocks (class and methods)
# implemented below.

# 1. Class: AgentTraits
# Description:
# A container class holding various attributes that define an agent's physical
# and behavioral characteristics, as well as some dynamic state related to these
# characteristics (like current energy or age).
#
# Attributes:
# - energy (float): The agent's current energy level. Depletes over time/actions, replenishes by eating. Determines survival. Initialized from a base value. Using float allows for gradual drain.
# - move_interval_ticks (int): The number of simulation ticks the agent waits between executing a move action. Lower value means the agent moves more frequently (faster). Initialized from a base value.
# - age (int): The number of simulation ticks the agent has existed. Starts at 0 and increments each tick.
# - max_age (int): The maximum number of ticks the agent can live before dying naturally of old age. Initialized from a base value.
# - vision_range (int): The distance (in grid cells) the agent can "see" outwards when searching for targets like food. Initialized from a base value. (New trait).
# - energy_drain_per_move (float): The amount of energy the agent loses each time it successfully moves to a new cell. Copied from the base value in config. (Trait value, initialized from BASE_ENERGY_DRAIN_PER_MOVE).
# - energy_drain_per_tick (float): The amount of energy the agent loses every simulation tick just for existing, regardless of movement. Copied from the base value in config. (Trait value, initialized from BASE_ENERGY_DRAIN_PER_TICK, optional based on design).
#
# Primary Role: Bundle the characteristics and stats of an agent.

# 1.1 Method: __init__
# Description:
# Constructor for the AgentTraits class. Initializes all the trait attributes
# for a new agent instance using default base values imported from `config.py`.
# Inputs:
#   - self: The instance being initialized.
# Where Inputs Typically Come From: Called by `Agent.__init__` when a new agent is created.
# Restrictions on Inputs: None.
# Other Relevant Info: This method sets up the initial trait values; these values might be
#                      modified later due to mutation (on reproduction) or interactions.
#
# Description of Algorithm/Process:
# 1. Import necessary base trait constants from `config.py` *within* the method or globally in the implementation section. Importing globally is standard for constants used throughout the module.
# 2. Assign the initial `energy` value (e.g., 50.0) to `self.energy`. Using a float is good practice for energy.
# 3. Assign the `BASE_MOVE_INTERVAL_TICKS` constant from `config.py` to `self.move_interval_ticks`.
# 4. Initialize `self.age` to 0.
# 5. Assign the `BASE_MAX_AGE_TICKS` constant from `config.py` to `self.max_age`.
# 6. Assign the `BASE_VISION_RANGE` constant from `config.py` to `self.vision_range`.
# 7. Assign the `BASE_ENERGY_DRAIN_PER_MOVE` constant from `config.py` to `self.energy_drain_per_move`. (Storing this as a trait value makes sense for future evolution).
# 8. Assign the `BASE_ENERGY_DRAIN_PER_TICK` constant from `config.py` to `self.energy_drain_per_tick`. (Store this as a trait value if that drain type is used).
# 9. (Placeholder) Initialize any future traits (size, strength, color) to their base values.
#
# Description of Output:
# None. Side effect is initializing the state attributes of the `self` object.


# --- START CODE IMPLEMENTATION ---

# Imports:
# Standard library imports first
# (No standard libraries needed in traits.py)

# Local package imports
# Import necessary base constants from config
from config import (BASE_MOVE_INTERVAL_TICKS, BASE_ENERGY_DRAIN_PER_TICK,
                    BASE_MAX_AGE_TICKS, BASE_VISION_RANGE, BASE_ENERGY_DRAIN_PER_MOVE)


### 1. Class: AgentTraits Implementation ###
class AgentTraits:
    ### 1.1 Method: __init__ Implementation ###
    def __init__(self):
        """
        Initializes agent traits with base values from config.
        """
        # Dynamic State Trait
        self.energy = 50.0 # current energy, using float for precision

        # Core Behavioral/Physical Traits (initialized from config)
        self.move_interval_ticks = BASE_MOVE_INTERVAL_TICKS # ticks between moves (lower = faster)
        self.max_age = BASE_MAX_AGE_TICKS                # maximum age in ticks
        self.vision_range = BASE_VISION_RANGE           # how far the agent can 'see'

        # Energy Cost Traits (initialized from config)
        self.energy_drain_per_move = BASE_ENERGY_DRAIN_PER_MOVE # energy cost each time agent moves
        self.energy_drain_per_tick = BASE_ENERGY_DRAIN_PER_TICK # energy cost just for existing each tick

        # Age Trait (starts at 0, dynamic state)
        self.age = 0 # agent's age in ticks

        # Future Traits Placeholder:
        # self.size = 1.0
        # self.bite_strength = 1.0
        # self.defense = 1.0
        # self.color = None # Could set a default color or None


# --- END CODE IMPLEMENTATION ---