#!/usr/bin/env python3
"""
Setup script for the number generation analysis project.
This script runs when the Pixi environment is activated.
"""

import os
import shutil

def setup_environment():
    """Set up the environment for the project."""
    print("🔧 Setting up number generation analysis environment...")
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        if os.path.exists('env_example.txt'):
            shutil.copy('env_example.txt', '.env')
            print("✅ Created .env file from env_example.txt")
        else:
            print("⚠️  env_example.txt not found. Please create .env file manually.")
    else:
        print("✅ .env file already exists")
    
    print("🚀 Environment setup complete!")
    print("\n📋 Available commands:")
    print("  pixi run test    - Test the setup")
    print("  pixi run quick   - Run quick analysis")
    print("  pixi run full    - Run full analysis")
    print("  pixi run example - Run example analyses")

if __name__ == "__main__":
    setup_environment() 