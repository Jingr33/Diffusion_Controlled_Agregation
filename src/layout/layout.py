from enum import Enum

class Layout(Enum):
    """
    Types of initial layout for the simulation.
    """
    CUBE = "cube"
    SPHERE = "sphere"
    RANDOM = "random"
