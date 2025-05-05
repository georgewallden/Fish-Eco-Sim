# agent/traits.py
# Defines the characteristics/stats of an agent

class AgentTraits:
    def __init__(self):
        self.energy = 50                  # current energy, determines lifespan/reproduction potential
        self.move_interval_ticks = 3     # ticks between moves (lower = faster movement, more energy drain per tick)
        self.age = 0                      # agent's age in ticks
        self.max_age = 500                # maximum age before dying of old age

        # You can add more later, like:
        # self.vision_range = 5           # how far the agent can 'see'
        # self.size = 1.0                   # body size, could influence predation, energy needs
        # self.speed = 1.0                  # multiplier for movement distance (if move_interval_ticks becomes more complex)
        # self.bite_strength = 1.0        # damage dealt in combat/predation
        # self.defense = 1.0              # damage resistance
        # self.color = (R, G, B)          # visual trait, potentially linked to genetics