from .base_category import BaseCategoryModule


class SubjectModule(BaseCategoryModule):
    """Subject category module for selecting main subjects"""
    
    def __init__(self, parent=None):
        super().__init__("subjects", parent)
