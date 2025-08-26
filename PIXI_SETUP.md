# Pixi Setup Guide

This guide will help you set up the number generation analysis project using Pixi, which handles Python version management and dependency resolution automatically.

## 🚀 Quick Start with Pixi

### 1. Install Pixi (if not already installed)

```bash
# On macOS/Linux
curl -fsSL https://pixi.sh/install.sh | bash

# On Windows (PowerShell)
irm https://pixi.sh/install.ps1 | iex

# Or using Homebrew on macOS
brew install pixi
```

### 2. Initialize the Project

```bash
# Navigate to your project directory
cd number_generation_project

# Install dependencies and activate environment
pixi install
```

### 3. Activate the Environment

```bash
# Activate the Pixi environment
pixi shell
```

The environment will automatically:
- Use Python 3.11 (compatible with all dependencies)
- Install all required packages
- Set up the .env file from env_example.txt

### 4. Run the Analysis

```bash
# Test the setup
pixi run test

# Run quick analysis (recommended for first time)
pixi run quick

# Run full analysis
pixi run full

# Run example analyses
pixi run example
```

## 🔧 Available Commands

| Command | Description |
|---------|-------------|
| `pixi run test` | Test the setup and verify all imports work |
| `pixi run quick` | Run a quick analysis with fewer samples |
| `pixi run full` | Run the complete analysis |
| `pixi run example` | Run various example analyses |

## 📁 Project Structure with Pixi

```
number_generation_project/
├── pixi.toml              # Pixi configuration
├── setup.py               # Environment setup script
├── number_generator.py    # Core number generation logic
├── analyzer.py           # Statistical analysis and visualization
├── main.py              # Main script to run analysis
├── example_analysis.py  # Example analyses
├── test_setup.py        # Setup verification
├── requirements.txt     # Python dependencies (for reference)
├── env_example.txt      # Environment variables template
├── README.md           # Main documentation
└── PIXI_SETUP.md       # This file
```

## 🎯 Benefits of Using Pixi

1. **Python Version Management**: Automatically uses Python 3.11 (compatible with numpy)
2. **Dependency Resolution**: Handles all package compatibility issues
3. **Isolated Environment**: Doesn't interfere with your system Python
4. **Reproducible Builds**: Same environment on any machine
5. **Easy Commands**: Simple `pixi run` commands for common tasks

## 🔍 Troubleshooting

### If Pixi is not installed:
```bash
# Install Pixi first
curl -fsSL https://pixi.sh/install.sh | bash
```

### If you get permission errors:
```bash
# Make sure you have write permissions
chmod +x setup.py
```

### If the environment doesn't activate:
```bash
# Try reinstalling
pixi install --force
```

### If you need to update dependencies:
```bash
# Update the pixi.toml file, then run:
pixi install
```

## 🧪 Testing Your Setup

After setting up with Pixi, run the test to verify everything works:

```bash
pixi run test
```

You should see output like:
```
🧪 Setup Test Suite
========================================
🔍 Testing imports...
✅ numpy imported successfully
✅ pandas imported successfully
✅ matplotlib imported successfully
✅ seaborn imported successfully
✅ openai imported successfully
✅ python-dotenv imported successfully
✅ scipy imported successfully

🔍 Testing local modules...
✅ NumberGenerator imported successfully
✅ NumberAnalyzer imported successfully

🔍 Testing analyzer functionality...
✅ Analyzer functionality test passed
   - Analyzed 2 ranges
   - Bias analysis completed
   - Consistency analysis completed

🔍 Testing environment...
✅ .env file found
✅ number_generator.py found
✅ analyzer.py found
✅ main.py found
✅ requirements.txt found
✅ README.md found

========================================
📊 Test Results: 4/4 tests passed
✅ All tests passed! Your setup is ready.
```

## 🚀 Next Steps

Once your setup is verified:

1. **Run a quick test**: `pixi run quick`
2. **Explore the results**: Check the generated charts and JSON files
3. **Try different ranges**: Modify the ranges in `main.py`
4. **Compare models**: Test different OpenAI models
5. **Run examples**: `pixi run example` for advanced analyses

## 💡 Tips

- The Pixi environment uses Python 3.11, which is fully compatible with all dependencies
- Your API key is already configured in the .env file
- Use `pixi shell` to get an interactive Python environment
- All generated files will be saved in your project directory 