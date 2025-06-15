from .base_category import BaseCategoryModule


class EnvironmentModule(BaseCategoryModule):
    """Environment category module for selecting settings and backgrounds"""
    
    def __init__(self, parent=None):
        super().__init__("environments", parent)
