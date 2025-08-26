# AI Model Number Generation Analysis

A comprehensive tool for analyzing number generation patterns from AI models like OpenAI's GPT models. This project helps you understand model biases, consistency, and distribution patterns when generating numbers across different ranges.

## 🎯 Features

- **Multi-range Testing**: Test number generation across various ranges (0-1, 1-10, 1-100, -1-1, etc.)
- **Bias Analysis**: Identify if models have preferences for certain number ranges or values
- **Consistency Testing**: Measure how consistent models are across multiple runs
- **Statistical Analysis**: Perform uniformity tests (Kolmogorov-Smirnov, Chi-square) to check if distributions are truly random
- **Visualization**: Generate comprehensive charts and graphs showing distribution patterns
- **Multiple Prompt Types**: Test different prompting strategies ("direct", "creative", "precise")
- **Export Results**: Save analysis results as JSON files for further processing

## 📊 What You Can Analyze

1. **Distribution Bias**: Does the model prefer certain numbers within a range?
2. **Range Coverage**: How well does the model cover the entire specified range?
3. **Consistency**: How reproducible are the results across multiple runs?
4. **Uniformity**: Do the generated numbers follow a uniform distribution?
5. **Prompt Sensitivity**: How do different prompting strategies affect results?

## 🚀 Quick Start

### Option 1: Using Pixi (Recommended)

Pixi handles Python version management and dependency resolution automatically, making it perfect for this project.

```bash
# Install Pixi (if not already installed)
curl -fsSL https://pixi.sh/install.sh | bash

# Navigate to project directory
cd number_generation_project

# Install dependencies and activate environment
pixi install

# Test the setup
pixi run test

# Run quick analysis (recommended for first time)
pixi run quick

# Run full analysis
pixi run full
```

**Benefits of Pixi:**
- Automatically uses Python 3.11 (compatible with all dependencies)
- Handles all package compatibility issues
- Isolated environment that doesn't interfere with your system Python
- Simple commands: `pixi run quick`, `pixi run full`, etc.

See [PIXI_SETUP.md](PIXI_SETUP.md) for detailed Pixi instructions.

### Option 2: Manual Setup

```bash
# Clone or download the project
cd number_generation_project

# Install dependencies
pip install -r requirements.txt

# Set up your OpenAI API key
cp env_example.txt .env
# Edit .env and add your OpenAI API key
```

**Note:** If you're using Python 3.12, you may encounter compatibility issues with numpy. Pixi is recommended for automatic version management.

## 📁 Project Structure

```
number_generation_project/
├── pixi.toml              # Pixi configuration (Python 3.11 + dependencies)
├── setup.py               # Environment setup script
├── number_generator.py    # Core number generation logic
├── analyzer.py           # Statistical analysis and visualization
├── main.py              # Main script to run analysis
├── example_analysis.py  # Example analyses
├── test_setup.py        # Setup verification
├── requirements.txt     # Python dependencies (for reference)
├── env_example.txt      # Environment variables template
├── README.md           # This file
└── PIXI_SETUP.md       # Pixi setup guide
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
DEFAULT_MODEL=gpt-3.5-turbo
```

### Customizing Analysis

You can modify the analysis parameters in `main.py`:

```python
# Test different ranges
ranges = [
    (0.0, 1.0),      # Unit interval
    (1.0, 10.0),     # Small positive integers
    (1.0, 100.0),    # Larger positive integers
    (-1.0, 1.0),     # Symmetric around zero
    (0.0, 100.0),    # Large positive range
    (-10.0, 10.0),   # Symmetric larger range
]

# Adjust test parameters
samples_per_range = 50  # Number of samples per range
runs = 3               # Number of runs for consistency testing
prompt_type = "direct" # Prompt type: "direct", "creative", or "precise"
```

## 📈 Understanding the Results

### Key Metrics

1. **Mean Bias**: Difference between actual and expected mean
   - Positive: Model tends toward higher values
   - Negative: Model tends toward lower values

2. **Range Coverage**: How much of the specified range is actually used
   - 1.0: Full range coverage
   - <1.0: Model doesn't use the full range

3. **Uniformity Tests**: 
   - **KS Test**: Kolmogorov-Smirnov test for uniformity
   - **Chi² Test**: Chi-square test for uniformity
   - p > 0.05: Distribution is uniform
   - p < 0.05: Distribution is not uniform

4. **Consistency (CV)**: Coefficient of variation across runs
   - Lower values = more consistent
   - Higher values = less consistent

### Output Files

- `analysis_results_{model}_visualizations.png`: Comprehensive charts
- `analysis_results_{model}.json`: Detailed data and statistics

## 🔬 Advanced Usage

### Using Different Models

```python
from number_generator import NumberGenerator

# Test different models
generator_gpt35 = NumberGenerator("gpt-3.5-turbo")
generator_gpt4 = NumberGenerator("gpt-4")

# Compare results
results_35 = generator_gpt35.run_consistency_test(ranges, samples_per_range, runs)
results_4 = generator_gpt4.run_consistency_test(ranges, samples_per_range, runs)
```

### Custom Analysis

```python
from analyzer import NumberAnalyzer

analyzer = NumberAnalyzer()

# Analyze specific results
analysis = analyzer.analyze_distribution(results)

# Create custom visualizations
analyzer.create_visualizations(results, analysis, "my_custom_analysis")

# Save results
analyzer.save_results(results, analysis, "my_results.json")
```

### Testing Different Prompt Types

```python
# Test different prompting strategies
prompt_types = ["direct", "creative", "precise"]

for prompt_type in prompt_types:
    results = generator.run_consistency_test(
        ranges=ranges,
        samples_per_range=samples_per_range,
        runs=runs,
        prompt_type=prompt_type
    )
    # Analyze results for each prompt type
```

## 🧪 Example Results

Here's what you might see in the analysis:

```
📊 Detailed Results by Range:

   Range 0.0-1.0:
     - Total samples: 150
     - Actual mean: 0.523
     - Expected mean: 0.500
     - Bias: 0.023
     - Range coverage: 0.987
     - KS test uniform: True (p=0.1234)
     - Chi² test uniform: True (p=0.2345)

   Range 1.0-10.0:
     - Total samples: 150
     - Actual mean: 5.234
     - Expected mean: 5.500
     - Bias: -0.266
     - Range coverage: 0.945
     - KS test uniform: False (p=0.0123)
     - Chi² test uniform: False (p=0.0234)
```

## 💡 Research Applications

This tool is useful for:

- **AI Safety Research**: Understanding model biases in numerical reasoning
- **Model Evaluation**: Comparing different models' number generation capabilities
- **Prompt Engineering**: Finding optimal prompting strategies for numerical tasks
- **Educational Research**: Studying how AI models understand mathematical concepts
- **Quality Assurance**: Ensuring models generate appropriate numerical outputs

## ⚠️ Important Notes

1. **API Costs**: Each number generation requires an API call. Monitor your usage!
2. **Rate Limiting**: The tool includes delays between calls to avoid rate limits
3. **Sample Size**: Larger sample sizes provide more reliable results but cost more
4. **Model Variability**: Results may vary between different model versions

## 🤝 Contributing

Feel free to contribute by:
- Adding new analysis metrics
- Improving visualizations
- Adding support for other AI models
- Enhancing the documentation

## 📄 License

This project is open source. Feel free to use and modify for your research needs.

## 🔗 Dependencies

- `openai`: OpenAI API client
- `numpy`: Numerical computing
- `pandas`: Data manipulation
- `matplotlib`: Plotting
- `seaborn`: Statistical visualizations
- `scipy`: Statistical tests
- `python-dotenv`: Environment variable management 