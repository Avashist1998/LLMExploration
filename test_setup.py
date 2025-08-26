#!/usr/bin/env python3
"""
Test script to verify the setup and basic functionality.
This script tests the imports and basic functionality without making API calls.
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import numpy as np
        print("✅ numpy imported successfully")
    except ImportError as e:
        print(f"❌ numpy import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✅ matplotlib imported successfully")
    except ImportError as e:
        print(f"❌ matplotlib import failed: {e}")
        return False
    
    try:
        import seaborn as sns
        print("✅ seaborn imported successfully")
    except ImportError as e:
        print(f"❌ seaborn import failed: {e}")
        return False
    
    try:
        import openai
        print("✅ openai imported successfully")
    except ImportError as e:
        print(f"❌ openai import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    try:
        from scipy import stats
        print("✅ scipy imported successfully")
    except ImportError as e:
        print(f"❌ scipy import failed: {e}")
        return False
    
    return True

def test_local_modules():
    """Test if our local modules can be imported."""
    print("\n🔍 Testing local modules...")
    
    try:
        from number_generator import NumberGenerator
        print("✅ NumberGenerator imported successfully")
    except ImportError as e:
        print(f"❌ NumberGenerator import failed: {e}")
        return False
    
    try:
        from analyzer import NumberAnalyzer
        print("✅ NumberAnalyzer imported successfully")
    except ImportError as e:
        print(f"❌ NumberAnalyzer import failed: {e}")
        return False
    
    return True

def test_analyzer_functionality():
    """Test basic analyzer functionality with mock data."""
    print("\n🔍 Testing analyzer functionality...")
    
    try:
        from analyzer import NumberAnalyzer
        import numpy as np
        
        # Create mock data
        mock_results = {
            'ranges': [(0.0, 1.0), (1.0, 10.0)],
            'samples_per_range': 50,
            'runs': 2,
            'prompt_type': 'direct',
            'data': {
                'run_1': {
                    '0.0-1.0': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                    '1.0-10.0': [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5]
                },
                'run_2': {
                    '0.0-1.0': [0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95],
                    '1.0-10.0': [1.2, 2.2, 3.2, 4.2, 5.2, 6.2, 7.2, 8.2, 9.2]
                }
            }
        }
        
        analyzer = NumberAnalyzer()
        analysis = analyzer.analyze_distribution(mock_results)
        
        print("✅ Analyzer functionality test passed")
        print(f"   - Analyzed {len(analysis['range_analysis'])} ranges")
        print(f"   - Bias analysis completed")
        print(f"   - Consistency analysis completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Analyzer functionality test failed: {e}")
        return False

def test_environment():
    """Test environment setup."""
    print("\n🔍 Testing environment...")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
    else:
        print("⚠️  .env file not found (you'll need to create one)")
        print("   Copy env_example.txt to .env and add your OpenAI API key")
    
    # Check if required files exist
    required_files = [
        'number_generator.py',
        'analyzer.py', 
        'main.py',
        'requirements.txt',
        'README.md'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} missing")
            return False
    
    return True

def main():
    """Run all tests."""
    print("🧪 Setup Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_local_modules,
        test_analyzer_functionality,
        test_environment
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! Your setup is ready.")
        print("\n🚀 Next steps:")
        print("   1. Create a .env file with your OpenAI API key")
        print("   2. Run: python main.py --quick")
        print("   3. Or run: python main.py for full analysis")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Install missing dependencies: pip install -r requirements.txt")
        print("   2. Check that all files are in the correct location")
        print("   3. Ensure Python version is 3.7+")

if __name__ == "__main__":
    main() 