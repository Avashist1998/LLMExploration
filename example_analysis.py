#!/usr/bin/env python3
"""
Example analysis script demonstrating various use cases for the number generation analysis.
This script shows how to perform specific research tasks and custom analysis.
"""

from number_generator import NumberGenerator
from analyzer import NumberAnalyzer
import matplotlib.pyplot as plt
import numpy as np

def compare_models():
    """
    Compare number generation patterns between different models.
    """
    print("🔍 Comparing Models: GPT-3.5-turbo vs GPT-4")
    print("=" * 50)
    
    models = ["gpt-3.5-turbo", "gpt-4"]
    ranges = [(0.0, 1.0), (1.0, 10.0), (-1.0, 1.0)]
    samples_per_range = 30
    runs = 2
    
    results = {}
    
    for model in models:
        print(f"\n📊 Testing {model}...")
        generator = NumberGenerator(model=model)
        
        model_results = generator.run_consistency_test(
            ranges=ranges,
            samples_per_range=samples_per_range,
            runs=runs
        )
        
        results[model] = model_results
    
    # Analyze and compare
    analyzer = NumberAnalyzer()
    
    for model, model_results in results.items():
        print(f"\n📈 Analysis for {model}:")
        analysis = analyzer.analyze_distribution(model_results)
        
        for range_key, range_analysis in analysis['range_analysis'].items():
            bias = range_analysis['mean_bias']
            coverage = range_analysis['range_coverage']
            uniformity = range_analysis['uniformity_test']['is_uniform_ks']
            print(f"  {range_key}: bias={bias:.3f}, coverage={coverage:.3f}, uniform={uniformity}")

def test_prompt_strategies():
    """
    Test how different prompting strategies affect number generation.
    """
    print("\n🎯 Testing Prompt Strategies")
    print("=" * 40)
    
    prompt_types = ["direct", "creative", "precise"]
    ranges = [(0.0, 1.0), (1.0, 10.0)]
    samples_per_range = 25
    runs = 2
    
    generator = NumberGenerator()
    analyzer = NumberAnalyzer()
    
    prompt_results = {}
    
    for prompt_type in prompt_types:
        print(f"\n📝 Testing '{prompt_type}' prompt strategy...")
        
        results = generator.run_consistency_test(
            ranges=ranges,
            samples_per_range=samples_per_range,
            runs=runs,
            prompt_type=prompt_type
        )
        
        analysis = analyzer.analyze_distribution(results)
        prompt_results[prompt_type] = analysis
    
    # Compare prompt strategies
    print(f"\n📊 Prompt Strategy Comparison:")
    for prompt_type, analysis in prompt_results.items():
        print(f"\n  {prompt_type.upper()} strategy:")
        for range_key, range_analysis in analysis['range_analysis'].items():
            bias = range_analysis['mean_bias']
            coverage = range_analysis['range_coverage']
            print(f"    {range_key}: bias={bias:.3f}, coverage={coverage:.3f}")

def analyze_specific_bias():
    """
    Analyze specific bias patterns in number generation.
    """
    print("\n🎲 Analyzing Specific Bias Patterns")
    print("=" * 40)
    
    # Test ranges that might reveal specific biases
    ranges = [
        (0.0, 1.0),      # Unit interval
        (0.0, 0.5),      # Lower half
        (0.5, 1.0),      # Upper half
        (0.0, 0.1),      # Very small numbers
        (0.9, 1.0),      # Very large numbers (in unit interval)
    ]
    
    samples_per_range = 40
    runs = 2
    
    generator = NumberGenerator()
    analyzer = NumberAnalyzer()
    
    results = generator.run_consistency_test(
        ranges=ranges,
        samples_per_range=samples_per_range,
        runs=runs
    )
    
    analysis = analyzer.analyze_distribution(results)
    
    print(f"\n📊 Bias Analysis Results:")
    for range_key, range_analysis in analysis['range_analysis'].items():
        bias = range_analysis['mean_bias']
        coverage = range_analysis['range_coverage']
        uniformity = range_analysis['uniformity_test']['is_uniform_ks']
        
        bias_direction = "positive" if bias > 0 else "negative"
        print(f"  {range_key}: {bias_direction} bias ({bias:.3f}), coverage={coverage:.3f}, uniform={uniformity}")

def test_consistency_over_time():
    """
    Test how consistent the model is over multiple runs with different delays.
    """
    print("\n⏰ Testing Consistency Over Time")
    print("=" * 40)
    
    ranges = [(0.0, 1.0), (1.0, 10.0)]
    samples_per_range = 20
    runs = 5  # More runs to test consistency
    
    generator = NumberGenerator()
    analyzer = NumberAnalyzer()
    
    results = generator.run_consistency_test(
        ranges=ranges,
        samples_per_range=samples_per_range,
        runs=runs
    )
    
    analysis = analyzer.analyze_distribution(results)
    
    print(f"\n🔄 Consistency Analysis:")
    for range_key, consistency in analysis['consistency_analysis'].items():
        cv_mean = consistency['cv_mean']
        cv_std = consistency['cv_std']
        
        consistency_level = "high" if cv_mean < 0.1 else "medium" if cv_mean < 0.2 else "low"
        print(f"  {range_key}: {consistency_level} consistency (CV={cv_mean:.3f})")

def create_custom_visualization():
    """
    Create a custom visualization focusing on specific aspects.
    """
    print("\n🎨 Creating Custom Visualization")
    print("=" * 40)
    
    ranges = [(0.0, 1.0), (1.0, 10.0), (-1.0, 1.0)]
    samples_per_range = 30
    runs = 2
    
    generator = NumberGenerator()
    analyzer = NumberAnalyzer()
    
    results = generator.run_consistency_test(
        ranges=ranges,
        samples_per_range=samples_per_range,
        runs=runs
    )
    
    analysis = analyzer.analyze_distribution(results)
    
    # Create a custom focused visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Bias comparison
    range_keys = list(analysis['range_analysis'].keys())
    biases = [analysis['range_analysis'][r]['mean_bias'] for r in range_keys]
    
    bars1 = ax1.bar(range_keys, biases, color=['red' if b > 0 else 'blue' for b in biases])
    ax1.set_title('Bias by Range')
    ax1.set_ylabel('Mean Bias')
    ax1.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax1.tick_params(axis='x', rotation=45)
    
    # 2. Coverage comparison
    coverages = [analysis['range_analysis'][r]['range_coverage'] for r in range_keys]
    ax2.bar(range_keys, coverages, color='green', alpha=0.7)
    ax2.set_title('Range Coverage')
    ax2.set_ylabel('Coverage Ratio')
    ax2.axhline(y=1.0, color='red', linestyle='--', alpha=0.7)
    ax2.tick_params(axis='x', rotation=45)
    
    # 3. Uniformity test results
    ks_p_values = [analysis['range_analysis'][r]['uniformity_test']['ks_p_value'] for r in range_keys]
    ax3.bar(range_keys, ks_p_values, color='orange', alpha=0.7)
    ax3.set_title('Uniformity Test (KS)')
    ax3.set_ylabel('P-value')
    ax3.axhline(y=0.05, color='red', linestyle='--', alpha=0.7, label='α=0.05')
    ax3.tick_params(axis='x', rotation=45)
    ax3.legend()
    
    # 4. Consistency across runs
    cv_means = [analysis['consistency_analysis'][r]['cv_mean'] for r in range_keys]
    ax4.bar(range_keys, cv_means, color='purple', alpha=0.7)
    ax4.set_title('Consistency (Coefficient of Variation)')
    ax4.set_ylabel('CV (Mean)')
    ax4.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('custom_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Custom visualization saved as 'custom_analysis.png'")

def main():
    """
    Run all example analyses.
    """
    print("🧪 Example Analysis Suite")
    print("=" * 50)
    
    # Run different types of analysis
    compare_models()
    test_prompt_strategies()
    analyze_specific_bias()
    test_consistency_over_time()
    create_custom_visualization()
    
    print(f"\n✅ All example analyses completed!")
    print(f"Check the generated files for detailed results.")

if __name__ == "__main__":
    main() 