from boolean_image.basemanipulator import BaseManipulator
from boolean_image.shave import Shave
from boolean_image.center import Center

class SimpleManipulator(Center, Shave):
    """
    Initialize BIA manipulators only requiring Base.__init__()
    """
    def __init__(self, *args, **kwargs):
        Shave.__init__(self, *args, **kwargs)
        Center.__init__(self, *args, **kwargs)
        return
