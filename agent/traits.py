# agent/traits.py
#
# Description:
# This module defines the `AgentTraits` class, which serves as a container
# for all the characteristics and numerical statistics (traits) that define
# an individual agent's capabilities, needs, and current state (beyond position
# and basic lifecycle). Traits influence attributes like movement speed,
# energy levels (including maximum capacity and drain rates), lifespan,
# sensing abilities (vision range), and potentially future interactions
# like size, attack strength, and defense. These traits also provide
# the input data for the agent's neural network.
#
# Key responsibilities of this file:
# - Define the `AgentTraits` class to hold agent attributes.
# - Initialize agent traits with base values from `config.py`.
# - Provide a structured way to access an agent's properties.
# - (Future) Provide methods for trait mutation and inheritance during reproduction.
#
# Design Philosophy/Notes:
# - Decouples agent properties from the main `Agent` class logic.
# - Centralizes trait definitions for easier management and modification
#   (e.g., for evolution/mutation mechanisms later).
# - Traits are stored as instance attributes, allowing each agent to have unique values.
# - Includes attributes like `max_energy` and drain rates that are important
#   for energy management and normalization as input for the neural network.

# Imports Description:
# This section lists the modules imported by agent/traits.py and their purpose.
# - config: Imports various `BASE_*` constants needed to initialize the default values of the agent's traits, including the newly added `BASE_MAX_ENERGY`.

# Code Block Descriptions:
# This section provides detailed blueprints for the code blocks (class and methods)
# implemented below.

# 1. Class: AgentTraits
# Description:
# A container class holding various attributes that define an agent's physical
# and behavioral characteristics, as well as some dynamic state related to these
# characteristics (like current energy or age). Includes properties essential
# for energy management and as input features for the neural network.
#
# Attributes:
# - energy (float): The agent's current energy level. Depletes over time/actions, replenishes by eating. Determines survival. Initialized from a base value (often less than max). Using float allows for gradual drain.
# - max_energy (float): **NEW** The maximum amount of energy the agent can hold. Initialized from `BASE_MAX_ENERGY` in `config.py`. Used for capping energy gain and for normalizing energy as a neural network input feature.
# - move_interval_ticks (int): The number of simulation ticks the agent waits between executing a move action. Lower value means the agent moves more frequently (faster). Initialized from a base value.
# - age (int): The number of simulation ticks the agent has existed. Starts at 0 and increments each tick.
# - max_age (int): The maximum number of ticks the agent can live before dying naturally of old age. Initialized from a base value.
# - vision_range (int): The distance (in grid cells) the agent can "see" outwards when searching for targets like food. Initialized from a base value.
# - energy_drain_per_move (float): The amount of energy the agent loses each time it successfully moves to a new cell. Copied from the base value in config. (Trait value).
# - energy_drain_per_tick (float): The amount of energy the agent loses every simulation tick just for existing, regardless of movement. Copied from the base value in config. (Trait value, optional based on design).
#
# Primary Role: Bundle the characteristics and stats of an agent, serving as configuration and state features.

# 1.1 Method: __init__
# Description:
# Constructor for the AgentTraits class. Initializes all the trait attributes
# for a new agent instance using default base values imported from `config.py`.
# This includes setting the initial current energy and the maximum energy capacity.
# Inputs:
#   - self: The instance being initialized.
# Where Inputs Typically Come From: Called by `Agent.__init__` when a new agent is created.
# Restrictions on Inputs: None.
# Other Relevant Info: This method sets up the initial trait values; these values might be
#                      modified later due to mutation (on reproduction) or interactions.
#                      Initial energy is set to a fixed value (50.0), and max energy
#                      is set from the config constant.
#
# Description of Algorithm/Process:
# 1. Import necessary base trait constants from `config.py`.
# 2. Assign the `BASE_MAX_ENERGY` constant from `config.py` to `self.max_energy`.
# 3. Assign the initial `energy` value (e.g., 50.0) to `self.energy`. This is typically less than or equal to `self.max_energy`.
# 4. Assign the `BASE_MOVE_INTERVAL_TICKS` constant to `self.move_interval_ticks`.
# 5. Initialize `self.age` to 0.
# 6. Assign the `BASE_MAX_AGE_TICKS` constant to `self.max_age`.
# 7. Assign the `BASE_VISION_RANGE` constant to `self.vision_range`.
# 8. Assign the `BASE_ENERGY_DRAIN_PER_MOVE` constant to `self.energy_drain_per_move`.
# 9. Assign the `BASE_ENERGY_DRAIN_PER_TICK` constant to `self.energy_drain_per_tick`.
# 10. (Placeholder) Initialize any future traits (size, strength, color) to their base values.
#
# Description of Output:
# None. Side effect is initializing the state attributes of the `self` object.


# --- START CODE IMPLEMENTATION ---

# Imports:
# Standard library imports first
# (No standard libraries needed in traits.py for initialization)

# Local package imports
# Import necessary base constants from config
from config import (BASE_MOVE_INTERVAL_TICKS, BASE_ENERGY_DRAIN_PER_TICK,
                    BASE_MAX_AGE_TICKS, BASE_VISION_RANGE, BASE_ENERGY_DRAIN_PER_MOVE,
                    BASE_MAX_ENERGY) # Import the new max energy constant


### 1. Class: AgentTraits Implementation ###
class AgentTraits:
    ### 1.1 Method: __init__ Implementation ###
    def __init__(self):
        """
        Initializes agent traits with base values from config.
        Includes initial and maximum energy.
        """
        # Energy Traits
        self.max_energy = BASE_MAX_ENERGY # NEW: Maximum energy capacity
        self.energy = self.max_energy / 2.0 # Start with half energy, or 50.0 as in original code
                                           # Let's use 50.0 to match original behavior unless specified
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