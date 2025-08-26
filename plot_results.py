#!/usr/bin/env python3
"""
Script to generate and save distribution plots of number generation results.
This creates visualizations that help understand the model's prediction patterns.
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
from pathlib import Path

def get_results_and_ranges(results: Dict):
    """Helper to extract data and ranges from possibly nested results dict."""
    if 'data' in results and 'ranges' in results:
        return results['data'], results['ranges']
    elif 'results' in results and 'data' in results['results'] and 'ranges' in results['results']:
        return results['results']['data'], results['results']['ranges']
    else:
        raise KeyError("Could not find 'data' and 'ranges' in results file.")

def create_distribution_plots(results: Dict, save_dir: str = "plots"):
    """
    Create and save distribution plots for the number generation results.
    
    Args:
        results (Dict): Results from the number generation analysis
        save_dir (str): Directory to save the plots
    """
    # Create plots directory if it doesn't exist
    Path(save_dir).mkdir(exist_ok=True)
    
    # Set up plotting style
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # Use helper to extract data and ranges
    data, ranges = get_results_and_ranges(results)
    
    print(f"📊 Creating distribution plots...")
    print(f"📁 Saving plots to: {save_dir}/")
    
    # 1. Individual range distributions
    create_individual_distributions(data, ranges, save_dir)
    
    # 2. Combined distribution comparison
    create_combined_distribution(data, ranges, save_dir)
    
    # 3. Run-by-run comparison
    create_run_comparison(data, ranges, save_dir)
    
    # 4. Bias visualization
    create_bias_visualization(data, ranges, save_dir)
    
    # 5. Coverage analysis
    create_coverage_analysis(data, ranges, save_dir)
    
    print(f"✅ All plots saved to {save_dir}/")

def create_individual_distributions(data: Dict, ranges: List[Tuple[float, float]], save_dir: str):
    """Create individual distribution plots for each range."""
    
    for min_val, max_val in ranges:
        range_key = f"{min_val}-{max_val}"
        all_numbers = []
        
        # Collect all numbers for this range across all runs
        for run_key, run_data in data.items():
            if range_key in run_data:
                all_numbers.extend(run_data[range_key])
        
        if all_numbers:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Histogram
            ax1.hist(all_numbers, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            ax1.axvline(np.mean(all_numbers), color='red', linestyle='--', 
                       label=f'Mean: {np.mean(all_numbers):.3f}')
            ax1.axvline((min_val + max_val) / 2, color='green', linestyle='--', 
                       label=f'Expected: {(min_val + max_val) / 2:.3f}')
            ax1.set_xlabel('Generated Numbers')
            ax1.set_ylabel('Frequency')
            ax1.set_title(f'Distribution for Range [{min_val}, {max_val}]')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Box plot
            ax2.boxplot(all_numbers, vert=True)
            ax2.set_ylabel('Generated Numbers')
            ax2.set_title(f'Box Plot for Range [{min_val}, {max_val}]')
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(f"{save_dir}/distribution_{range_key.replace('.', '_')}.png", 
                       dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"  📈 Saved: distribution_{range_key.replace('.', '_')}.png")

def create_combined_distribution(data: Dict, ranges: List[Tuple[float, float]], save_dir: str):
    """Create a combined distribution plot comparing all ranges."""
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Collect all data
    all_data = []
    labels = []
    
    for min_val, max_val in ranges:
        range_key = f"{min_val}-{max_val}"
        numbers = []
        
        for run_key, run_data in data.items():
            if range_key in run_data:
                numbers.extend(run_data[range_key])
        
        if numbers:
            all_data.append(numbers)
            labels.append(f'[{min_val}, {max_val}]')
    
    # Overlaid histograms
    for i, (numbers, label) in enumerate(zip(all_data, labels)):
        ax1.hist(numbers, bins=15, alpha=0.6, label=label, density=True)
    
    ax1.set_xlabel('Generated Numbers')
    ax1.set_ylabel('Density')
    ax1.set_title('Distribution Comparison Across All Ranges')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Box plots side by side
    ax2.boxplot(all_data, labels=labels)
    ax2.set_ylabel('Generated Numbers')
    ax2.set_title('Box Plot Comparison Across All Ranges')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{save_dir}/combined_distributions.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  📊 Saved: combined_distributions.png")

def create_run_comparison(data: Dict, ranges: List[Tuple[float, float]], save_dir: str):
    """Create plots comparing results across different runs."""
    
    for min_val, max_val in ranges:
        range_key = f"{min_val}-{max_val}"
        
        # Collect data by run
        run_data = []
        run_labels = []
        
        for run_key, run_data_dict in data.items():
            if range_key in run_data_dict and run_data_dict[range_key]:
                run_data.append(run_data_dict[range_key])
                run_labels.append(run_key.replace('_', ' ').title())
        
        if len(run_data) > 1:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Box plots by run
            ax1.boxplot(run_data, labels=run_labels)
            ax1.set_ylabel('Generated Numbers')
            ax1.set_title(f'Consistency Across Runs: [{min_val}, {max_val}]')
            ax1.grid(True, alpha=0.3)
            
            # Mean comparison
            means = [np.mean(numbers) for numbers in run_data]
            expected_mean = (min_val + max_val) / 2
            
            bars = ax2.bar(run_labels, means, alpha=0.7)
            ax2.axhline(y=expected_mean, color='red', linestyle='--', 
                       label=f'Expected: {expected_mean:.3f}')
            ax2.set_ylabel('Mean Value')
            ax2.set_title(f'Mean Values by Run: [{min_val}, {max_val}]')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            # Color bars based on bias
            for bar, mean in zip(bars, means):
                if mean > expected_mean:
                    bar.set_color('red')
                else:
                    bar.set_color('blue')
            
            plt.tight_layout()
            plt.savefig(f"{save_dir}/run_comparison_{range_key.replace('.', '_')}.png", 
                       dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"  🔄 Saved: run_comparison_{range_key.replace('.', '_')}.png")

def create_bias_visualization(data: Dict, ranges: List[Tuple[float, float]], save_dir: str):
    """Create bias analysis visualization."""
    
    biases = []
    range_labels = []
    coverages = []
    
    for min_val, max_val in ranges:
        range_key = f"{min_val}-{max_val}"
        all_numbers = []
        
        for run_key, run_data in data.items():
            if range_key in run_data:
                all_numbers.extend(run_data[range_key])
        
        if all_numbers:
            numbers_array = np.array(all_numbers)
            expected_mean = (min_val + max_val) / 2
            actual_mean = np.mean(numbers_array)
            bias = actual_mean - expected_mean
            
            # Calculate coverage
            range_width = max_val - min_val
            actual_range = np.max(numbers_array) - np.min(numbers_array)
            coverage = actual_range / range_width
            
            biases.append(bias)
            coverages.append(coverage)
            range_labels.append(f'[{min_val}, {max_val}]')
    
    # Create bias visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Bias bar chart
    bars1 = ax1.bar(range_labels, biases, color=['red' if b > 0 else 'blue' for b in biases])
    ax1.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax1.set_ylabel('Bias (Actual - Expected Mean)')
    ax1.set_title('Bias Analysis by Range')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3)
    
    # Coverage bar chart
    ax2.bar(range_labels, coverages, color='green', alpha=0.7)
    ax2.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Full Coverage')
    ax2.set_ylabel('Coverage Ratio')
    ax2.set_title('Range Coverage Analysis')
    ax2.tick_params(axis='x', rotation=45)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Bias vs Coverage scatter
    ax3.scatter(coverages, biases, s=100, alpha=0.7)
    ax3.set_xlabel('Coverage Ratio')
    ax3.set_ylabel('Bias')
    ax3.set_title('Bias vs Coverage Relationship')
    ax3.grid(True, alpha=0.3)
    
    # Add range labels to scatter points
    for i, label in enumerate(range_labels):
        ax3.annotate(label, (coverages[i], biases[i]), 
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    # Summary statistics
    ax4.axis('off')
    summary_text = f"""
    Summary Statistics:
    
    Total Ranges: {len(ranges)}
    Average Bias: {np.mean(biases):.3f}
    Bias Std Dev: {np.std(biases):.3f}
    Average Coverage: {np.mean(coverages):.3f}
    
    Most Biased Range: {range_labels[np.argmax(np.abs(biases))]}
    Least Covered Range: {range_labels[np.argmin(coverages)]}
    """
    ax4.text(0.1, 0.5, summary_text, transform=ax4.transAxes, 
             fontsize=12, verticalalignment='center',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(f"{save_dir}/bias_analysis.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  📊 Saved: bias_analysis.png")

def create_coverage_analysis(data: Dict, ranges: List[Tuple[float, float]], save_dir: str):
    """Create detailed coverage analysis."""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    for min_val, max_val in ranges:
        range_key = f"{min_val}-{max_val}"
        all_numbers = []
        
        for run_key, run_data in data.items():
            if range_key in run_data:
                all_numbers.extend(run_data[range_key])
        
        if all_numbers:
            numbers_array = np.array(all_numbers)
            
            # Plot 1: Number distribution with range boundaries
            ax1.scatter([range_key] * len(numbers_array), numbers_array, 
                       alpha=0.6, s=20, label=f'[{min_val}, {max_val}]')
            ax1.axhline(y=min_val, color='red', linestyle='--', alpha=0.7)
            ax1.axhline(y=max_val, color='red', linestyle='--', alpha=0.7)
            ax1.axhline(y=(min_val + max_val) / 2, color='green', linestyle='-', alpha=0.5)
    
    ax1.set_ylabel('Generated Numbers')
    ax1.set_title('Number Distribution vs Range Boundaries')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Coverage heatmap
    coverage_data = []
    range_names = []
    
    for min_val, max_val in ranges:
        range_key = f"{min_val}-{max_val}"
        all_numbers = []
        
        for run_key, run_data in data.items():
            if range_key in run_data:
                all_numbers.extend(run_data[range_key])
        
        if all_numbers:
            numbers_array = np.array(all_numbers)
            range_width = max_val - min_val
            actual_range = np.max(numbers_array) - np.min(numbers_array)
            coverage = actual_range / range_width
            
            coverage_data.append(coverage)
            range_names.append(f'[{min_val}, {max_val}]')
    
    im = ax2.imshow([coverage_data], cmap='RdYlGn', aspect='auto')
    ax2.set_xticks(range(len(range_names)))
    ax2.set_xticklabels(range_names, rotation=45)
    ax2.set_yticks([])
    ax2.set_title('Coverage Heatmap (Green=Good, Red=Poor)')
    
    # Add coverage values as text
    for i, coverage in enumerate(coverage_data):
        ax2.text(i, 0, f'{coverage:.2f}', ha='center', va='center', 
                color='black', fontweight='bold')
    
    plt.colorbar(im, ax=ax2, label='Coverage Ratio')
    
    plt.tight_layout()
    plt.savefig(f"{save_dir}/coverage_analysis.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  📈 Saved: coverage_analysis.png")

def load_results_from_file(filename: str) -> Dict:
    """Load results from a JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File {filename} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"❌ Error parsing JSON file {filename}.")
        return {}

def main():
    """Main function to create plots from saved results."""
    print("🎨 Number Generation Distribution Plotter")
    print("=" * 50)
    
    # Look for results files
    results_files = [
        "analysis_results_claude-3-5-haiku-20241022.json"
        # "analysis_results_gpt-4.1.json",
        # "analysis_results_gpt-4.1-mini.json",
        # "analysis_results_gpt-3.5-turbo.json",
        # "analysis_results.json",
        # "quick_test_results.json"
    ]
    
    results = None
    for filename in results_files:
        if os.path.exists(filename):
            print(f"📁 Found results file: {filename}")
            results = load_results_from_file(filename)
            if results:
                break
    
    if not results:
        print("❌ No results file found. Please run the analysis first:")
        print("   pixi run quick  # for quick test")
        print("   pixi run full   # for full analysis")
        return
    
    # Create plots
    create_distribution_plots(results, "plots")
    
    print(f"\n✅ All plots created successfully!")
    print(f"📁 Check the 'plots/' directory for visualizations")

if __name__ == "__main__":
    main() 