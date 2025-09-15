from enum import Enum

class DSPType(Enum):
    """Enumeration for different DSP AP types. 
    Currently only uses ITEM and TECH."""
    ITEM = 1
    TECH = 2
    RECIPE = 3