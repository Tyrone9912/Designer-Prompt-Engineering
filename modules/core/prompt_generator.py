from typing import Dict, List, Optional
import json
from dataclasses import dataclass, field


@dataclass
class CategorySelection:
    """Represents a selection from a category module"""
    category: str
    selection_id: str
    custom_text: str = ""
    weight: float = 1.0
    modifiers: List[str] = field(default_factory=list)


class PromptGenerator:
    """Main engine for combining category selections into coherent prompts"""
    
    def __init__(self):
        self.categories = {}
        self.current_selections: Dict[str, CategorySelection] = {}
        self.mode = "SFW"  # or "NSFW"
        self.separator = ", "
        
    def add_category_selection(self, category: str, selection: CategorySelection):
        """Add selection from a category module"""
        self.current_selections[category] = selection
        
    def remove_category_selection(self, category: str):
        """Remove selection from a category"""
        if category in self.current_selections:
            del self.current_selections[category]
            
    def set_mode(self, mode: str):
        """Toggle between SFW and NSFW modes"""
        if mode in ["SFW", "NSFW"]:
            self.mode = mode
            
    def generate_prompt(self) -> str:
        """Generate final prompt from current selections"""
        if not self.current_selections:
            return ""
            
        prompt_parts = []
        
        category_order = ["subject", "style", "composition", "environment", "lighting", "technical"]
        
        for category in category_order:
            if category in self.current_selections:
                selection = self.current_selections[category]
                part = self._format_selection(selection)
                if part:
                    prompt_parts.append(part)
        
        for category, selection in self.current_selections.items():
            if category not in category_order:
                part = self._format_selection(selection)
                if part:
                    prompt_parts.append(part)
        
        return self.separator.join(prompt_parts)
    
    def _format_selection(self, selection: CategorySelection) -> str:
        """Format a single category selection into prompt text"""
        parts = []
        
        if selection.custom_text.strip():
            parts.append(selection.custom_text.strip())
        
        if selection.modifiers:
            parts.extend(selection.modifiers)
            
        if selection.weight != 1.0 and parts:
            if selection.weight > 1.0:
                formatted_parts = [f"({part})" for part in parts]
            elif selection.weight < 1.0:
                formatted_parts = [f"[{part}]" for part in parts]
            else:
                formatted_parts = parts
        else:
            formatted_parts = parts
            
        return self.separator.join(formatted_parts)
    
    def get_prompt_stats(self) -> Dict:
        """Get statistics about the current prompt"""
        prompt = self.generate_prompt()
        return {
            "length": len(prompt),
            "word_count": len(prompt.split()),
            "categories_used": len(self.current_selections),
            "mode": self.mode
        }
    
    def clear_selections(self):
        """Clear all current selections"""
        self.current_selections.clear()
