from .base_category import BaseCategoryModule


class StyleModule(BaseCategoryModule):
    """Style category module for selecting artistic styles"""
    
    def __init__(self, parent=None):
        super().__init__("styles", parent)
