import sys
from typing import Dict, Optional
from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, 
                            QWidget, QTextEdit, QLabel, QPushButton, QMenuBar, 
                            QMenu, QMessageBox, QFileDialog, QCheckBox, QSplitter,
                            QGroupBox, QListWidget, QListWidgetItem)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QAction, QFont, QKeySequence

from ..core.prompt_generator import PromptGenerator, CategorySelection
from ..core.template_manager import TemplateManager
from ..core.config_manager import ConfigManager
from .category_modules.subject_module import SubjectModule
from .category_modules.style_module import StyleModule
from .category_modules.composition_module import CompositionModule
from .category_modules.environment_module import EnvironmentModule
from .category_modules.lighting_module import LightingModule
from .category_modules.technical_module import TechnicalModule


class MainWindow(QMainWindow):
    """Main application window with tabbed interface"""
    
    def __init__(self):
        super().__init__()
        
        self.prompt_generator = PromptGenerator()
        self.template_manager = TemplateManager()
        self.config_manager = ConfigManager()
        
        self.category_modules = {}
        
        self.setup_ui()
        self.setup_menu()
        self.setup_connections()
        self.restore_window_state()
        
    def setup_ui(self):
        """Initialize main UI layout"""
        self.setWindowTitle("AI Art Prompt Builder")
        self.setMinimumSize(1024, 768)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        left_widget = self.create_category_tabs()
        splitter.addWidget(left_widget)
        
        right_widget = self.create_right_panel()
        splitter.addWidget(right_widget)
        
        splitter.setSizes([700, 300])
        
        self.statusBar().showMessage("Ready")
        
    def create_category_tabs(self) -> QWidget:
        """Create the tabbed interface for categories"""
        tab_widget = QTabWidget()
        
        self.category_modules["subjects"] = SubjectModule()
        self.category_modules["styles"] = StyleModule()
        self.category_modules["compositions"] = CompositionModule()
        self.category_modules["environments"] = EnvironmentModule()
        self.category_modules["lighting"] = LightingModule()
        self.category_modules["technical"] = TechnicalModule()
        
        tab_widget.addTab(self.category_modules["subjects"], "Subject")
        tab_widget.addTab(self.category_modules["styles"], "Style")
        tab_widget.addTab(self.category_modules["compositions"], "Composition")
        tab_widget.addTab(self.category_modules["environments"], "Environment")
        tab_widget.addTab(self.category_modules["lighting"], "Lighting")
        tab_widget.addTab(self.category_modules["technical"], "Technical")
        
        return tab_widget
    
    def create_right_panel(self) -> QWidget:
        """Create the right panel with prompt preview and templates"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        mode_group = self.create_mode_toggle()
        layout.addWidget(mode_group)
        
        preview_group = self.create_prompt_preview()
        layout.addWidget(preview_group)
        
        template_group = self.create_template_panel()
        layout.addWidget(template_group)
        
        return widget
    
    def create_mode_toggle(self) -> QGroupBox:
        """Create SFW/NSFW mode toggle"""
        group = QGroupBox("Content Mode")
        layout = QHBoxLayout(group)
        
        self.sfw_checkbox = QCheckBox("SFW Mode")
        self.sfw_checkbox.setChecked(True)
        self.sfw_checkbox.toggled.connect(self.on_mode_toggled)
        layout.addWidget(self.sfw_checkbox)
        
        mode_label = QLabel("(Safe for Work content only)")
        mode_label.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(mode_label)
        
        layout.addStretch()
        
        return group
    
    def create_prompt_preview(self) -> QGroupBox:
        """Create prompt preview area"""
        group = QGroupBox("Generated Prompt Preview")
        layout = QVBoxLayout(group)
        
        self.prompt_preview = QTextEdit()
        self.prompt_preview.setMaximumHeight(150)
        self.prompt_preview.setPlaceholderText("Your generated prompt will appear here...")
        self.prompt_preview.setReadOnly(True)
        layout.addWidget(self.prompt_preview)
        
        button_layout = QHBoxLayout()
        
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_prompt)
        button_layout.addWidget(self.copy_button)
        
        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self.clear_all_selections)
        button_layout.addWidget(self.clear_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.stats_label = QLabel("Length: 0 | Words: 0 | Categories: 0")
        self.stats_label.setStyleSheet("color: #666; font-size: 10px;")
        layout.addWidget(self.stats_label)
        
        return group
    
    def create_template_panel(self) -> QGroupBox:
        """Create template management panel"""
        group = QGroupBox("Templates")
        layout = QVBoxLayout(group)
        
        self.template_list = QListWidget()
        self.template_list.itemDoubleClicked.connect(self.load_selected_template)
        layout.addWidget(self.template_list)
        
        button_layout = QHBoxLayout()
        
        self.save_template_button = QPushButton("Save Template")
        self.save_template_button.clicked.connect(self.save_current_template)
        button_layout.addWidget(self.save_template_button)
        
        self.load_template_button = QPushButton("Load Template")
        self.load_template_button.clicked.connect(self.load_selected_template)
        button_layout.addWidget(self.load_template_button)
        
        layout.addLayout(button_layout)
        
        self.refresh_template_list()
        
        return group
    
    def setup_menu(self):
        """Setup application menu"""
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.clear_all_selections)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        save_action = QAction("Save Template", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_current_template)
        file_menu.addAction(save_action)
        
        load_action = QAction("Load Template", self)
        load_action.setShortcut(QKeySequence.StandardKey.Open)
        load_action.triggered.connect(self.show_load_template_dialog)
        file_menu.addAction(load_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("Export Prompt", self)
        export_action.triggered.connect(self.export_prompt)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("Quit", self)
        quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        edit_menu = menubar.addMenu("Edit")
        
        copy_action = QAction("Copy Prompt", self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(self.copy_prompt)
        edit_menu.addAction(copy_action)
        
        clear_action = QAction("Clear All", self)
        clear_action.triggered.connect(self.clear_all_selections)
        edit_menu.addAction(clear_action)
        
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_connections(self):
        """Setup signal connections"""
        for module in self.category_modules.values():
            module.selection_changed.connect(self.on_category_selection_changed)
    
    def on_category_selection_changed(self, category: str, selection: CategorySelection):
        """Handle category selection change"""
        self.prompt_generator.add_category_selection(category, selection)
        self.update_prompt_preview()
    
    def on_mode_toggled(self, checked: bool):
        """Handle SFW/NSFW mode toggle"""
        mode = "SFW" if checked else "NSFW"
        self.prompt_generator.set_mode(mode)
        
        for module in self.category_modules.values():
            module.set_mode(mode)
        
        self.update_prompt_preview()
    
    def update_prompt_preview(self):
        """Update the prompt preview display"""
        prompt = self.prompt_generator.generate_prompt()
        self.prompt_preview.setPlainText(prompt)
        
        stats = self.prompt_generator.get_prompt_stats()
        self.stats_label.setText(
            f"Length: {stats['length']} | Words: {stats['word_count']} | Categories: {stats['categories_used']}"
        )
        
        self.statusBar().showMessage(f"Prompt updated - {stats['mode']} mode")
    
    def copy_prompt(self):
        """Copy prompt to clipboard"""
        prompt = self.prompt_preview.toPlainText()
        if prompt:
            clipboard = self.app.clipboard() if hasattr(self, 'app') else None
            if clipboard:
                clipboard.setText(prompt)
            self.statusBar().showMessage("Prompt copied to clipboard")
        else:
            self.statusBar().showMessage("No prompt to copy")
    
    def clear_all_selections(self):
        """Clear all category selections"""
        self.prompt_generator.clear_selections()
        
        for module in self.category_modules.values():
            module.clear_selections()
        
        self.update_prompt_preview()
        self.statusBar().showMessage("All selections cleared")
    
    def save_current_template(self):
        """Save current selections as a template"""
        prompt = self.prompt_generator.generate_prompt()
        if not prompt.strip():
            QMessageBox.warning(self, "Warning", "No prompt to save. Please make some selections first.")
            return
        
        from PyQt6.QtWidgets import QInputDialog
        name, ok = QInputDialog.getText(self, "Save Template", "Template name:")
        
        if ok and name.strip():
            try:
                template_id = self.template_manager.save_template(
                    name=name.strip(),
                    description="",
                    categories=self.prompt_generator.current_selections,
                    generated_prompt=prompt,
                    mode=self.prompt_generator.mode
                )
                self.refresh_template_list()
                self.statusBar().showMessage(f"Template '{name}' saved successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save template: {str(e)}")
    
    def load_selected_template(self):
        """Load the selected template"""
        current_item = self.template_list.currentItem()
        if not current_item:
            return
        
        template_id = current_item.data(Qt.ItemDataRole.UserRole)
        template = self.template_manager.load_template(template_id)
        
        if template:
            self.clear_all_selections()
            
            mode = template.mode
            self.sfw_checkbox.setChecked(mode == "SFW")
            self.prompt_generator.set_mode(mode)
            
            self.prompt_preview.setPlainText(template.generated_prompt)
            self.statusBar().showMessage(f"Template '{template.name}' loaded")
    
    def show_load_template_dialog(self):
        """Show template loading dialog"""
        if self.template_list.count() == 0:
            QMessageBox.information(self, "Info", "No templates available to load.")
            return
        
        self.load_selected_template()
    
    def refresh_template_list(self):
        """Refresh the template list"""
        self.template_list.clear()
        
        templates = self.template_manager.list_templates()
        for template in templates:
            item = QListWidgetItem(f"{template.name} ({template.mode})")
            item.setData(Qt.ItemDataRole.UserRole, template.template_id)
            self.template_list.addItem(item)
    
    def export_prompt(self):
        """Export prompt to file"""
        prompt = self.prompt_preview.toPlainText()
        if not prompt.strip():
            QMessageBox.warning(self, "Warning", "No prompt to export.")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Prompt", "prompt.txt", "Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(prompt)
                self.statusBar().showMessage(f"Prompt exported to {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export prompt: {str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self, "About AI Art Prompt Builder",
            "AI Art Prompt Builder v1.0\n\n"
            "A desktop application for generating sophisticated AI art prompts "
            "through an intuitive, modular interface.\n\n"
            "Built with PyQt6"
        )
    
    def restore_window_state(self):
        """Restore window state from config"""
        geometry = self.config_manager.get_window_geometry()
        self.resize(*geometry["size"])
        self.move(*geometry["position"])
    
    def closeEvent(self, event):
        """Handle window close event"""
        geometry = self.geometry()
        self.config_manager.set_window_geometry(
            geometry.width(), geometry.height(),
            geometry.x(), geometry.y()
        )
        
        event.accept()
