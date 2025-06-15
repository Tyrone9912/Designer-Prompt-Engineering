#!/usr/bin/env python3
"""
Test script to verify core functionality without GUI display
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from modules.core.prompt_generator import PromptGenerator, CategorySelection
from modules.core.template_manager import TemplateManager
from modules.core.config_manager import ConfigManager

def test_prompt_generation():
    """Test prompt generation functionality"""
    print("Testing prompt generation...")
    
    generator = PromptGenerator()
    
    subject_selection = CategorySelection(
        category="subjects",
        selection_id="person_adult",
        custom_text="beautiful woman",
        weight=1.2,
        modifiers=["highly detailed", "professional"]
    )
    
    style_selection = CategorySelection(
        category="styles", 
        selection_id="photorealistic",
        custom_text="",
        weight=1.0,
        modifiers=["sharp focus"]
    )
    
    generator.add_category_selection("subjects", subject_selection)
    generator.add_category_selection("styles", style_selection)
    
    prompt = generator.generate_prompt()
    print(f"Generated prompt: {prompt}")
    
    stats = generator.get_prompt_stats()
    print(f"Prompt stats: {stats}")
    
    return len(prompt) > 0

def test_template_management():
    """Test template save/load functionality"""
    print("\nTesting template management...")
    
    manager = TemplateManager()
    
    test_selections = {
        "subjects": CategorySelection(
            category="subjects",
            selection_id="test",
            custom_text="test subject",
            weight=1.0,
            modifiers=["test modifier"]
        )
    }
    
    template_name = "test_template"
    template_id = manager.save_template(
        name=template_name,
        description="Test template description", 
        categories=test_selections,
        generated_prompt="test subject, test modifier",
        mode="SFW",
        tags=["test"]
    )
    print(f"Template save success: {template_id is not None}")
    print(f"Template ID: {template_id}")
    
    loaded_template = manager.load_template(template_id)
    print(f"Template load success: {loaded_template is not None}")
    
    if loaded_template:
        print(f"Loaded template name: {loaded_template.name}")
        print(f"Loaded template categories count: {len(loaded_template.categories)}")
    
    return template_id is not None and loaded_template is not None

def test_config_management():
    """Test configuration management"""
    print("\nTesting configuration management...")
    
    config = ConfigManager()
    
    config.set("test_key", "test_value")
    value = config.get("test_key")
    print(f"Config test success: {value == 'test_value'}")
    
    config.set("prompt.default_mode", "NSFW")
    mode = config.get("prompt.default_mode")
    print(f"Mode setting success: {mode == 'NSFW'}")
    
    geometry = config.get_window_geometry()
    print(f"Window geometry: {geometry}")
    
    return value == "test_value" and mode == "NSFW"

def test_data_loading():
    """Test category data loading"""
    print("\nTesting category data loading...")
    
    categories = ["subjects", "styles", "compositions", "environments", "lighting", "technical"]
    
    for category in categories:
        data_path = f"modules/data/categories/{category}.json"
        if os.path.exists(data_path):
            print(f"✓ {category}.json exists")
            try:
                import json
                with open(data_path, 'r') as f:
                    data = json.load(f)
                    sfw_count = len(data.get("sfw_options", []))
                    nsfw_count = len(data.get("nsfw_options", []))
                    modifiers_count = len(data.get("common_modifiers", []))
                    print(f"  - SFW options: {sfw_count}, NSFW options: {nsfw_count}, Modifiers: {modifiers_count}")
            except Exception as e:
                print(f"  - Error loading {category}: {e}")
                return False
        else:
            print(f"✗ {category}.json missing")
            return False
    
    return True

def main():
    """Run all tests"""
    print("=== AI Art Prompt Builder Core Functionality Test ===\n")
    
    tests = [
        ("Data Loading", test_data_loading),
        ("Prompt Generation", test_prompt_generation),
        ("Template Management", test_template_management),
        ("Configuration Management", test_config_management)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            print(f"✓ {test_name}: {'PASSED' if result else 'FAILED'}")
        except Exception as e:
            results.append((test_name, False))
            print(f"✗ {test_name}: FAILED - {e}")
        print()
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print("=== Test Summary ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All core functionality tests PASSED!")
        print("The AI Art Prompt Builder Phase 1 MVP is ready for GUI testing on a desktop environment.")
    else:
        print("❌ Some tests failed. Please review the implementation.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
