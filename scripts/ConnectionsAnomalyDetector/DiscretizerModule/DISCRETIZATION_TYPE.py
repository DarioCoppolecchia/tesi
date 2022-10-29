from enum import Enum, auto

class DISCRETIZATION_TYPE(Enum):
    """
    Enumerate the types of discretization
        #. EQUAL_FREQUENCY
        #. EQUAL_WIDTH
    """    
    EQUAL_FREQUENCY = auto()
    EQUAL_WIDTH = auto()