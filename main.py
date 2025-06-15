#!/usr/bin/env python3
"""
AI Art Prompt Builder - Desktop Application
A PyQt6-based GUI application for generating AI art prompts
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.gui.main_window import MainWindow


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("AI Art Prompt Builder")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Designer Prompt Engineering")
    
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    window = MainWindow()
    window.app = app  # Store reference for clipboard access
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
