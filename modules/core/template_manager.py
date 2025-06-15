import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict, field
from .prompt_generator import CategorySelection


@dataclass
class Template:
    """Represents a saved prompt template"""
    template_id: str
    name: str
    description: str
    created_date: str
    mode: str
    categories: Dict[str, Dict]
    generated_prompt: str
    tags: List[str] = field(default_factory=list)


class TemplateManager:
    """Manages saving, loading, and organizing prompt templates"""
    
    def __init__(self, templates_dir: str = "modules/data/templates"):
        self.templates_dir = templates_dir
        self.ensure_templates_dir()
        
    def ensure_templates_dir(self):
        """Ensure templates directory exists"""
        os.makedirs(self.templates_dir, exist_ok=True)
        
    def save_template(self, name: str, description: str, categories: Dict[str, CategorySelection], 
                     generated_prompt: str, mode: str, tags: Optional[List[str]] = None) -> str:
        """Save a new template and return its ID"""
        template_id = str(uuid.uuid4())
        
        categories_dict = {}
        for category, selection in categories.items():
            categories_dict[category] = {
                "selection_id": selection.selection_id,
                "custom_text": selection.custom_text,
                "weight": selection.weight,
                "modifiers": selection.modifiers
            }
        
        template = Template(
            template_id=template_id,
            name=name,
            description=description,
            created_date=datetime.utcnow().isoformat() + "Z",
            mode=mode,
            categories=categories_dict,
            generated_prompt=generated_prompt,
            tags=tags or []
        )
        
        filename = f"{template_id}.json"
        filepath = os.path.join(self.templates_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(asdict(template), f, indent=2, ensure_ascii=False)
            
        return template_id
    
    def load_template(self, template_id: str) -> Optional[Template]:
        """Load a template by ID"""
        filename = f"{template_id}.json"
        filepath = os.path.join(self.templates_dir, filename)
        
        if not os.path.exists(filepath):
            return None
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return Template(**data)
        except (json.decoder.JSONDecodeError, TypeError) as e:
            print(f"Error loading template {template_id}: {e}")
            return None
    
    def list_templates(self, mode_filter: Optional[str] = None, 
                      tag_filter: Optional[str] = None) -> List[Template]:
        """List all templates with optional filtering"""
        templates = []
        
        if not os.path.exists(self.templates_dir):
            return templates
            
        for filename in os.listdir(self.templates_dir):
            if filename.endswith('.json'):
                template_id = filename[:-5]  # Remove .json extension
                template = self.load_template(template_id)
                
                if template:
                    if mode_filter and template.mode != mode_filter:
                        continue
                    if tag_filter and tag_filter not in template.tags:
                        continue
                        
                    templates.append(template)
        
        templates.sort(key=lambda t: t.created_date, reverse=True)
        return templates
    
    def delete_template(self, template_id: str) -> bool:
        """Delete a template by ID"""
        filename = f"{template_id}.json"
        filepath = os.path.join(self.templates_dir, filename)
        
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                return True
            except OSError as e:
                print(f"Error deleting template {template_id}: {e}")
                return False
        return False
    
    def update_template(self, template_id: str, **updates) -> bool:
        """Update an existing template"""
        template = self.load_template(template_id)
        if not template:
            return False
            
        for key, value in updates.items():
            if hasattr(template, key):
                setattr(template, key, value)
        
        filename = f"{template_id}.json"
        filepath = os.path.join(self.templates_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(asdict(template), f, indent=2, ensure_ascii=False)
            return True
        except (OSError, json.decoder.JSONDecodeError) as e:
            print(f"Error updating template {template_id}: {e}")
            return False
    
    def export_template(self, template_id: str, export_path: str) -> bool:
        """Export a template to a specific file path"""
        template = self.load_template(template_id)
        if not template:
            return False
            
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(template), f, indent=2, ensure_ascii=False)
            return True
        except (OSError, json.decoder.JSONDecodeError) as e:
            print(f"Error exporting template {template_id}: {e}")
            return False
    
    def import_template(self, import_path: str) -> Optional[str]:
        """Import a template from a file and return its new ID"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            old_id = data.get('template_id')
            new_id = str(uuid.uuid4())
            data['template_id'] = new_id
            
            filename = f"{new_id}.json"
            filepath = os.path.join(self.templates_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            return new_id
            
        except (OSError, json.decoder.JSONDecodeError, KeyError) as e:
            print(f"Error importing template: {e}")
            return None
