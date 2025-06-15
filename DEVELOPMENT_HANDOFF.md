# AI Art Prompt Builder - Development Handoff Document

## Project Overview

The AI Art Prompt Builder is a desktop GUI application designed to help users generate sophisticated AI art prompts through an intuitive, modular interface. The application provides structured categories for prompt elements, real-time preview generation, and template management capabilities.

### Core Vision
Create a professional-grade desktop tool that democratizes AI art prompt creation by providing structured guidance across key artistic elements while maintaining flexibility for creative expression.

## Technical Architecture

### Framework & Platform
- **GUI Framework**: PyQt6 (cross-platform desktop support)
- **Target Platforms**: macOS, Linux (Windows support possible)
- **Python Version**: 3.8+
- **Architecture Pattern**: Modular MVC with category-based components

### Project Structure
```
Designer-Prompt-Engineering/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── modules/                         # Core application modules
│   ├── __init__.py
│   ├── core/                       # Core business logic
│   │   ├── __init__.py
│   │   ├── prompt_generator.py     # Main prompt generation engine
│   │   ├── template_manager.py     # Template save/load functionality
│   │   └── config_manager.py       # Application configuration
│   ├── gui/                        # GUI components
│   │   ├── __init__.py
│   │   ├── main_window.py          # Main application window
│   │   ├── prompt_preview.py       # Real-time prompt preview widget
│   │   ├── template_panel.py       # Template management UI
│   │   └── category_modules/       # Individual category implementations
│   │       ├── __init__.py
│   │       ├── base_category.py    # Abstract base class for categories
│   │       ├── subject_module.py   # Subject/character selection
│   │       ├── style_module.py     # Art style and technique
│   │       ├── composition_module.py # Layout and framing
│   │       ├── environment_module.py # Setting and background
│   │       ├── lighting_module.py  # Lighting and atmosphere
│   │       └── technical_module.py # Camera and technical settings
│   └── data/                       # Data files and resources
│       ├── __init__.py
│       ├── categories/             # Category option definitions
│       │   ├── subjects.json
│       │   ├── styles.json
│       │   ├── compositions.json
│       │   ├── environments.json
│       │   ├── lighting.json
│       │   └── technical.json
│       └── templates/              # Saved user templates
├── tests/                          # Unit and integration tests
│   ├── __init__.py
│   ├── test_prompt_generator.py
│   ├── test_template_manager.py
│   └── test_gui_components.py
└── assets/                         # Static assets (icons, images)
    └── icons/
```

## Feature Specifications

### Phase 1: MVP (Weeks 1-4)
**Core Functionality**
- Desktop GUI application with tabbed interface
- 6 category modules with predefined options
- Real-time prompt generation and preview
- Basic template save/load functionality
- SFW/NSFW mode toggle

**Category Modules**
1. **Subject Module**: Character types, objects, creatures
2. **Style Module**: Art styles, techniques, artists
3. **Composition Module**: Framing, angles, layouts
4. **Environment Module**: Settings, backgrounds, locations
5. **Lighting Module**: Lighting types, moods, times of day
6. **Technical Module**: Camera settings, quality modifiers

### Phase 2: Enhanced Features (Weeks 5-7)
- Advanced template management with categories
- Export functionality (clipboard, text file, JSON)
- Custom option addition within categories
- Prompt history and favorites
- Basic prompt optimization suggestions

### Phase 3: Professional Features (Weeks 8-11)
- API integrations (Stable Diffusion, DALL-E, Midjourney)
- Plugin system for custom categories
- Batch prompt generation
- Advanced prompt analysis and scoring
- Cloud sync for templates and settings

## Technical Implementation Details

### Core Classes and Components

#### PromptGenerator (modules/core/prompt_generator.py)
```python
class PromptGenerator:
    """Main engine for combining category selections into coherent prompts"""
    
    def __init__(self):
        self.categories = {}
        self.current_selections = {}
        self.mode = "SFW"  # or "NSFW"
    
    def generate_prompt(self) -> str:
        """Generate final prompt from current selections"""
        pass
    
    def add_category_selection(self, category: str, selection: dict):
        """Add selection from a category module"""
        pass
    
    def set_mode(self, mode: str):
        """Toggle between SFW and NSFW modes"""
        pass
```

#### BaseCategoryModule (modules/gui/category_modules/base_category.py)
```python
from abc import ABC, abstractmethod
from PyQt6.QtWidgets import QWidget

class BaseCategoryModule(QWidget, ABC):
    """Abstract base class for all category modules"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selections = {}
        self.options = self.load_options()
    
    @abstractmethod
    def load_options(self) -> dict:
        """Load category-specific options from data files"""
        pass
    
    @abstractmethod
    def create_ui(self):
        """Create the UI components for this category"""
        pass
    
    def get_selections(self) -> dict:
        """Return current user selections"""
        return self.selections
    
    def selection_changed(self):
        """Emit signal when selections change"""
        pass
```

#### MainWindow (modules/gui/main_window.py)
```python
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal

class MainWindow(QMainWindow):
    """Main application window with tabbed interface"""
    
    prompt_updated = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_categories()
        self.setup_connections()
    
    def setup_ui(self):
        """Initialize main UI layout"""
        pass
    
    def setup_categories(self):
        """Initialize all category modules"""
        pass
    
    def update_prompt_preview(self):
        """Update real-time prompt preview"""
        pass
```

### Data Structure Specifications

#### Category Options Format (JSON)
```json
{
  "category_name": "subjects",
  "sfw_options": [
    {
      "id": "person_portrait",
      "label": "Portrait of a person",
      "tags": ["person", "portrait", "face"],
      "weight": 1.0,
      "modifiers": ["detailed", "realistic"]
    }
  ],
  "nsfw_options": [
    {
      "id": "adult_content",
      "label": "Adult content example",
      "tags": ["adult", "mature"],
      "weight": 1.0,
      "modifiers": ["artistic", "tasteful"]
    }
  ],
  "common_modifiers": ["high quality", "detailed", "professional"]
}
```

#### Template Format
```json
{
  "template_id": "uuid-string",
  "name": "User Template Name",
  "description": "Template description",
  "created_date": "2025-06-15T12:46:47Z",
  "mode": "SFW",
  "categories": {
    "subject": {"selection_id": "person_portrait", "custom_text": ""},
    "style": {"selection_id": "photorealistic", "custom_text": ""},
    "composition": {"selection_id": "close_up", "custom_text": ""},
    "environment": {"selection_id": "studio", "custom_text": ""},
    "lighting": {"selection_id": "soft_natural", "custom_text": ""},
    "technical": {"selection_id": "high_res", "custom_text": ""}
  },
  "generated_prompt": "Final generated prompt text",
  "tags": ["portrait", "realistic", "studio"]
}
```

## User Interface Specifications

### Main Window Layout
- **Menu Bar**: File, Edit, View, Tools, Help
- **Toolbar**: Quick actions (New, Save, Load, Export, Mode Toggle)
- **Category Tabs**: 6 tabs for different prompt categories
- **Prompt Preview Panel**: Real-time generated prompt display
- **Template Panel**: Template management sidebar
- **Status Bar**: Current mode, selection count, generation status

### Category Module UI Pattern
Each category module follows a consistent layout:
- **Header**: Category name and description
- **Options Grid**: Selectable options with preview images/icons
- **Custom Input**: Text field for custom additions
- **Modifiers**: Checkboxes for common modifiers
- **Weight Slider**: Importance weighting for this category

### Responsive Design Considerations
- Minimum window size: 1024x768
- Scalable UI elements for different screen sizes
- Keyboard shortcuts for power users
- Accessibility compliance (screen readers, high contrast)

## Development Guidelines

### Code Standards
- **PEP 8**: Python code style compliance
- **Type Hints**: Use throughout for better IDE support
- **Docstrings**: Google-style docstrings for all public methods
- **Error Handling**: Comprehensive exception handling
- **Logging**: Structured logging for debugging and monitoring

### Testing Strategy
- **Unit Tests**: Core logic components (pytest)
- **Integration Tests**: GUI component interactions
- **User Acceptance Tests**: End-to-end workflow testing
- **Performance Tests**: Prompt generation speed benchmarks

### Version Control
- **Branch Strategy**: Feature branches with descriptive names
- **Commit Messages**: Conventional commit format
- **Code Reviews**: Required for all changes
- **CI/CD**: Automated testing and linting

## Deployment and Distribution

### Development Environment
```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py

# Run tests
pytest tests/

# Lint code
python -m py_compile *.py
```

### Build and Package
- **PyInstaller**: Create standalone executables
- **Platform-specific**: Separate builds for macOS and Linux
- **Asset Bundling**: Include all data files and icons
- **Installer Creation**: Platform-appropriate installers

## Security and Privacy

### Data Handling
- **Local Storage**: All templates and settings stored locally
- **No Telemetry**: No data collection or transmission
- **NSFW Content**: Appropriate warnings and age verification
- **User Privacy**: No personal information required or stored

### Content Moderation
- **SFW Mode**: Default safe mode with family-friendly options
- **NSFW Mode**: Explicit content with appropriate warnings
- **Content Filtering**: Configurable content restrictions
- **Export Controls**: Warning for potentially sensitive content

## Performance Requirements

### Response Times
- **UI Interactions**: < 100ms response time
- **Prompt Generation**: < 500ms for complex prompts
- **Template Loading**: < 200ms for template operations
- **Application Startup**: < 3 seconds cold start

### Resource Usage
- **Memory**: < 200MB typical usage
- **Storage**: < 50MB application size
- **CPU**: Minimal background processing
- **Network**: No network requirements (offline capable)

## Future Roadmap

### Planned Enhancements
- **AI Integration**: Direct API connections to image generators
- **Community Features**: Template sharing and rating
- **Advanced Analytics**: Prompt effectiveness tracking
- **Mobile Companion**: Simplified mobile interface
- **Web Version**: Browser-based alternative

### Extensibility
- **Plugin Architecture**: Third-party category modules
- **Theme System**: Customizable UI themes
- **Localization**: Multi-language support
- **API Endpoints**: External tool integration

## Support and Maintenance

### Documentation
- **User Manual**: Comprehensive usage guide
- **Developer Docs**: API and extension documentation
- **Video Tutorials**: Step-by-step usage examples
- **FAQ**: Common questions and troubleshooting

### Update Strategy
- **Automatic Updates**: Optional update checking
- **Backward Compatibility**: Template format versioning
- **Migration Tools**: Data format upgrade utilities
- **Release Notes**: Detailed change documentation

---

## Development Timeline

### Week 1-2: Foundation
- [ ] Project structure setup
- [ ] Core classes implementation
- [ ] Basic GUI framework
- [ ] Category data structure

### Week 3-4: MVP Features
- [ ] All 6 category modules
- [ ] Real-time prompt generation
- [ ] Template save/load
- [ ] SFW/NSFW mode toggle

### Week 5-6: Enhancement
- [ ] Advanced template management
- [ ] Export functionality
- [ ] Custom option addition
- [ ] Prompt history

### Week 7-8: Polish
- [ ] UI/UX improvements
- [ ] Performance optimization
- [ ] Comprehensive testing
- [ ] Documentation

### Week 9-11: Professional Features
- [ ] API integrations
- [ ] Plugin system
- [ ] Advanced analytics
- [ ] Distribution preparation

---

*This document serves as the complete technical specification for the AI Art Prompt Builder project. All development should follow these guidelines and specifications to ensure consistency and quality.*
