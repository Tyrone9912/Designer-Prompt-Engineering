from .base_category import BaseCategoryModule


class CompositionModule(BaseCategoryModule):
    """Composition category module for selecting framing and layout"""
    
    def __init__(self, parent=None):
        super().__init__("compositions", parent)
