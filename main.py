#!/usr/bin/env python3
"""
Main script for analyzing number generation patterns from AI models.
This script demonstrates how to use the NumberGenerator and NumberAnalyzer classes
to study model biases and consistency in number generation.
"""

import os
import sys
from number_generator import NumberGenerator
from analyzer import NumberAnalyzer

MODELS = [
    "gpt-3.5-turbo",
    "gpt-4.1-mini",
    "gpt-4.1",
    "claude-3-5-haiku-20241022",
    "claude-3-7-sonnet-20250219",
    "claude-sonnet-4-20250514",
]


def main():
    """
    Main function to run the number generation analysis.
    """
    print("🤖 AI Model Number Generation Analysis")
    print("=" * 50)

    # Configuration
    model = MODELS[-1]  # You can change this to other models like "gpt-4"

    # Define the ranges to test
    ranges = [
        (0.0, 1.0),  # Unit interval
        (1.0, 10.0),  # Small positive integers
        (1.0, 100.0),  # Larger positive integers
        (-1.0, 1.0),  # Symmetric around zero
        (0.0, 100.0),  # Large positive range
        (-100.0, 0.0),  # Large negative range
        (-10.0, 10.0),  # Symmetric larger range
    ]

    # Test parameters
    samples_per_range = 200  # Number of samples per range (reduce for faster testing)
    runs = 5  # Number of runs for consistency testing
    prompt_type = "direct"  # Prompt type: "direct", "creative", or "precise"

    try:
        # Initialize the number generator
        print(f"Initializing NumberGenerator with model: {model}")
        generator = NumberGenerator(model=model)

        # Initialize the analyzer
        print("Initializing NumberAnalyzer...")
        analyzer = NumberAnalyzer()

        print(f"\n📊 Running analysis with parameters:")
        print(f"   - Model: {model}")
        print(f"   - Ranges: {ranges}")
        print(f"   - Samples per range: {samples_per_range}")
        print(f"   - Number of runs: {runs}")
        print(f"   - Prompt type: {prompt_type}")
        print(f"   - Total API calls: {len(ranges) * samples_per_range * runs}")

        # Run the consistency test
        print(f"\n🚀 Starting number generation...")
        results = generator.run_consistency_test(
            ranges=ranges,
            samples_per_range=samples_per_range,
            runs=runs,
            prompt_type=prompt_type,
        )

        print(f"\n✅ Number generation completed!")
        print(
            f"   - Total numbers generated: {sum(len(run_data[range_key]) for run_key, run_data in results['data'].items() for range_key in run_data)}"
        )

        # Analyze the results
        print(f"\n📈 Analyzing results...")
        analysis = analyzer.analyze_distribution(results)

        # Print summary
        print(f"\n📋 Analysis Summary:")
        print(f"   - Ranges tested: {len(ranges)}")
        print(f"   - Overall bias: {analysis['bias_analysis']['mean_bias']:.4f}")
        print(
            f"   - Bias standard deviation: {analysis['bias_analysis']['bias_std']:.4f}"
        )

        # Print detailed results for each range
        print(f"\n📊 Detailed Results by Range:")
        for range_key, range_analysis in analysis["range_analysis"].items():
            print(f"\n   Range {range_key}:")
            print(f"     - Total samples: {range_analysis['total_samples']}")
            print(f"     - Actual mean: {range_analysis['actual_mean']:.3f}")
            print(f"     - Expected mean: {range_analysis['expected_mean']:.3f}")
            print(f"     - Bias: {range_analysis['mean_bias']:.3f}")
            print(f"     - Range coverage: {range_analysis['range_coverage']:.3f}")

            uniformity = range_analysis["uniformity_test"]
            print(
                f"     - KS test uniform: {uniformity['is_uniform_ks']} (p={uniformity['ks_p_value']:.4f})"
            )
            print(
                f"     - Chi² test uniform: {uniformity['is_uniform_chi2']} (p={uniformity['chi2_p_value']:.4f})"
            )

        # Print consistency results
        print(f"\n🔄 Consistency Analysis:")
        for range_key, consistency in analysis["consistency_analysis"].items():
            print(f"   Range {range_key}:")
            print(f"     - Mean consistency (CV): {consistency['cv_mean']:.4f}")
            print(f"     - Std consistency (CV): {consistency['cv_std']:.4f}")

        # Create visualizations
        print(f"\n🎨 Creating visualizations...")
        analyzer.create_visualizations(
            results, analysis, f"plots/analysis_results_{model}"
        )

        # Save results
        print(f"\n💾 Saving results...")
        analyzer.save_results(
            results, analysis, f"/results/analysis_results_{model}.json"
        )

        print(f"\n✅ Analysis completed successfully!")
        print(
            f"   - Visualizations saved as: analysis_results_{model}_visualizations.png"
        )
        print(f"   - Data saved as: analysis_results_{model}.json")
        print(
            f"   - Run 'python plot_results.py' to generate detailed distribution plots"
        )

    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Please make sure you have set your OPENAI_API_KEY in the .env file.")
        print("You can copy env_example.txt to .env and add your API key.")
        sys.exit(1)

    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)


def run_quick_test():
    """
    Run a quick test with fewer samples for faster results.
    """
    print("🔬 Quick Test Mode")
    print("=" * 30)

    # model = "gpt-4.1"
    model = MODELS[3]
    ranges = [(0.0, 1.0), (1.0, 10.0), (-1.0, 1.0)]
    samples_per_range = 20
    runs = 2

    try:
        print("Initializing NumberGenerator...")
        generator = NumberGenerator(model=model)
        print("Initializing NumberAnalyzer...")
        analyzer = NumberAnalyzer()

        print("Running quick test...")
        print(
            f"Running quick test with {samples_per_range} samples per range, {runs} runs..."
        )

        results = generator.run_consistency_test(
            ranges=ranges, samples_per_range=samples_per_range, runs=runs
        )

        analysis = analyzer.analyze_distribution(results)

        print(f"\nQuick Test Results:")
        for range_key, range_analysis in analysis["range_analysis"].items():
            bias = range_analysis["mean_bias"]
            coverage = range_analysis["range_coverage"]
            print(f"  {range_key}: bias={bias:.3f}, coverage={coverage:.3f}")

        # Save results for plotting
        analyzer.save_results(results, analysis, "quick_test_results.json")

        print(f"\n✅ Quick test completed!")
        print(f"📁 Results saved to: quick_test_results.json")
        print(f"🎨 Run 'pixi run plot' to generate distribution plots")

    except Exception as e:
        print(f"❌ Quick test failed: {e}")


if __name__ == "__main__":
    # Check if user wants to run quick test
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        run_quick_test()
    else:
        main()
