# agent/__init__.py
# This file makes the 'agent' package importable
# It also specifies which names are publicly available when doing 'from agent import ...'

# Import the main Agent class from the base module
from .base import Agent

# You might also want to make other classes/functions directly available
# under the 'agent' namespace, e.g., agent.AgentTraits
from .traits import AgentTraits

# Typically, internal functions like move_agent or draw_agent are not imported
# here unless they are intended to be called directly from outside the package.
# The Agent class itself calls them, so they don't need to be here.
# from .movement import move_agent # No need to import these here usually
# from .render import draw_agent   # No need to import these here usually

# The __all__ list can explicitly define what 'from agent import *' imports
# __all__ = ['Agent', 'AgentTraits']