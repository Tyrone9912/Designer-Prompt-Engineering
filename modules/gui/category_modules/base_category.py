from typing import Dict, List, Optional
import json
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                            QLabel, QCheckBox, QLineEdit, QSlider, QGroupBox,
                            QScrollArea, QPushButton, QTextEdit)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

from ...core.prompt_generator import CategorySelection


class BaseCategoryModule(QWidget):
    """Abstract base class for all category modules"""
    
    selection_changed = pyqtSignal(str, object)  # category_name, CategorySelection
    
    def __init__(self, category_name: str, parent=None):
        super().__init__(parent)
        self.category_name = category_name
        self.current_mode = "SFW"
        self.selections = {}
        self.custom_text = ""
        self.weight = 1.0
        self.selected_modifiers = []
        
        self.options = self.load_options()
        
        self.create_ui()
        
    def load_options(self) -> Dict:
        """Load category-specific options from data files"""
        data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "categories", f"{self.category_name}.json")
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            print(f"Error loading options for {self.category_name}: {e}")
            return {"sfw_options": [], "nsfw_options": [], "common_modifiers": []}
    
    def create_ui(self):
        """Create the UI components for this category"""
        layout = QVBoxLayout(self)
        
        header = self.create_header()
        layout.addWidget(header)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        options_group = self.create_options_group()
        content_layout.addWidget(options_group)
        
        custom_group = self.create_custom_input_group()
        content_layout.addWidget(custom_group)
        
        modifiers_group = self.create_modifiers_group()
        content_layout.addWidget(modifiers_group)
        
        weight_group = self.create_weight_group()
        content_layout.addWidget(weight_group)
        
        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)
        
    def create_header(self) -> QWidget:
        """Create category header with name and description"""
        header_widget = QWidget()
        layout = QVBoxLayout(header_widget)
        
        title = QLabel(self.category_name.title())
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        description = QLabel(self.get_category_description())
        description.setWordWrap(True)
        description.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(description)
        
        return header_widget
    
    def create_options_group(self) -> QGroupBox:
        """Create the options selection group"""
        group = QGroupBox("Options")
        layout = QGridLayout(group)
        
        options = self.get_current_options()
        
        row = 0
        col = 0
        max_cols = 3
        
        for option in options:
            checkbox = QCheckBox(option["label"])
            checkbox.setObjectName(f"option_{option['id']}")
            checkbox.toggled.connect(lambda checked, opt_id=option['id']: self.on_option_toggled(opt_id, checked))
            
            layout.addWidget(checkbox, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        return group
    
    def create_custom_input_group(self) -> QGroupBox:
        """Create custom text input group"""
        group = QGroupBox("Custom Text")
        layout = QVBoxLayout(group)
        
        self.custom_input = QTextEdit()
        self.custom_input.setMaximumHeight(80)
        self.custom_input.setPlaceholderText(f"Add custom {self.category_name} text...")
        self.custom_input.textChanged.connect(self.on_custom_text_changed)
        
        layout.addWidget(self.custom_input)
        
        return group
    
    def create_modifiers_group(self) -> QGroupBox:
        """Create common modifiers group"""
        group = QGroupBox("Common Modifiers")
        layout = QGridLayout(group)
        
        modifiers = self.options.get("common_modifiers", [])
        
        row = 0
        col = 0
        max_cols = 2
        
        for modifier in modifiers:
            checkbox = QCheckBox(modifier)
            checkbox.setObjectName(f"modifier_{modifier}")
            checkbox.toggled.connect(lambda checked, mod=modifier: self.on_modifier_toggled(mod, checked))
            
            layout.addWidget(checkbox, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        return group
    
    def create_weight_group(self) -> QGroupBox:
        """Create weight adjustment group"""
        group = QGroupBox("Importance Weight")
        layout = QHBoxLayout(group)
        
        layout.addWidget(QLabel("Low"))
        
        self.weight_slider = QSlider(Qt.Orientation.Horizontal)
        self.weight_slider.setMinimum(1)
        self.weight_slider.setMaximum(20)
        self.weight_slider.setValue(10)  # Default weight of 1.0
        self.weight_slider.valueChanged.connect(self.on_weight_changed)
        layout.addWidget(self.weight_slider)
        
        layout.addWidget(QLabel("High"))
        
        self.weight_label = QLabel("1.0")
        layout.addWidget(self.weight_label)
        
        return group
    
    def get_current_options(self) -> List[Dict]:
        """Get options for current mode (SFW/NSFW)"""
        if self.current_mode == "NSFW":
            return self.options.get("sfw_options", []) + self.options.get("nsfw_options", [])
        else:
            return self.options.get("sfw_options", [])
    
    def get_category_description(self) -> str:
        """Get description for this category"""
        descriptions = {
            "subjects": "Choose the main subject or focus of your image",
            "styles": "Select the artistic style and technique",
            "compositions": "Define the framing and layout of your image",
            "environments": "Set the background and setting",
            "lighting": "Choose the lighting mood and atmosphere",
            "technical": "Specify camera and technical quality settings"
        }
        return descriptions.get(self.category_name, f"Configure {self.category_name} options")
    
    def on_option_toggled(self, option_id: str, checked: bool):
        """Handle option checkbox toggle"""
        if checked:
            self.selections[option_id] = True
        else:
            self.selections.pop(option_id, None)
        
        self.emit_selection_changed()
    
    def on_custom_text_changed(self):
        """Handle custom text change"""
        self.custom_text = self.custom_input.toPlainText()
        self.emit_selection_changed()
    
    def on_modifier_toggled(self, modifier: str, checked: bool):
        """Handle modifier checkbox toggle"""
        if checked:
            if modifier not in self.selected_modifiers:
                self.selected_modifiers.append(modifier)
        else:
            if modifier in self.selected_modifiers:
                self.selected_modifiers.remove(modifier)
        
        self.emit_selection_changed()
    
    def on_weight_changed(self, value: int):
        """Handle weight slider change"""
        self.weight = value / 10.0  # Convert to 0.1 - 2.0 range
        self.weight_label.setText(f"{self.weight:.1f}")
        self.emit_selection_changed()
    
    def emit_selection_changed(self):
        """Emit selection changed signal"""
        selection_text_parts = []
        
        options = self.get_current_options()
        for option in options:
            if option["id"] in self.selections:
                selection_text_parts.append(option["label"])
        
        if self.custom_text.strip():
            selection_text_parts.append(self.custom_text.strip())
        
        selection = CategorySelection(
            category=self.category_name,
            selection_id=",".join(self.selections.keys()) if self.selections else "",
            custom_text=self.custom_text,
            weight=self.weight,
            modifiers=self.selected_modifiers.copy()
        )
        
        self.selection_changed.emit(self.category_name, selection)
    
    def set_mode(self, mode: str):
        """Set SFW/NSFW mode"""
        if mode != self.current_mode:
            self.current_mode = mode
            self.refresh_options()
    
    def refresh_options(self):
        """Refresh the options display for current mode"""
        options_group = self.findChild(QGroupBox, "Options")
        if options_group:
            layout = options_group.layout()
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            
            options = self.get_current_options()
            row = 0
            col = 0
            max_cols = 3
            
            for option in options:
                checkbox = QCheckBox(option["label"])
                checkbox.setObjectName(f"option_{option['id']}")
                checkbox.toggled.connect(lambda checked, opt_id=option['id']: self.on_option_toggled(opt_id, checked))
                
                if option['id'] in self.selections:
                    checkbox.setChecked(True)
                
                layout.addWidget(checkbox, row, col)
                
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
    
    def get_selections(self) -> CategorySelection:
        """Return current user selections as CategorySelection object"""
        return CategorySelection(
            category=self.category_name,
            selection_id=",".join(self.selections.keys()) if self.selections else "",
            custom_text=self.custom_text,
            weight=self.weight,
            modifiers=self.selected_modifiers.copy()
        )
    
    def clear_selections(self):
        """Clear all selections"""
        self.selections.clear()
        self.selected_modifiers.clear()
        self.custom_text = ""
        self.weight = 1.0
        
        if hasattr(self, 'custom_input'):
            self.custom_input.clear()
        if hasattr(self, 'weight_slider'):
            self.weight_slider.setValue(10)
            self.weight_label.setText("1.0")
        
        for checkbox in self.findChildren(QCheckBox):
            checkbox.setChecked(False)
