from .base_category import BaseCategoryModule


class LightingModule(BaseCategoryModule):
    """Lighting category module for selecting lighting and atmosphere"""
    
    def __init__(self, parent=None):
        super().__init__("lighting", parent)
