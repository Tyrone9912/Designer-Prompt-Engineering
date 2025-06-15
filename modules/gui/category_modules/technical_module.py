from .base_category import BaseCategoryModule


class TechnicalModule(BaseCategoryModule):
    """Technical category module for camera and quality settings"""
    
    def __init__(self, parent=None):
        super().__init__("technical", parent)
