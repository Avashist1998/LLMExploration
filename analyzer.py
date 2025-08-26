import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
from scipy import stats
import json


class NumberAnalyzer:
    """
    A class to analyze the distribution and consistency of generated numbers.
    """

    def __init__(self):
        """Initialize the analyzer with plotting style."""
        plt.style.use("seaborn-v0_8")
        sns.set_palette("husl")

    def analyze_distribution(self, results: Dict) -> Dict:
        """
        Analyze the distribution of generated numbers across different ranges.

        Args:
            results (Dict): Results from NumberGenerator.run_consistency_test()

        Returns:
            Dict: Analysis results including distribution statistics
        """
        analysis = {
            "range_analysis": {},
            "bias_analysis": {},
            "consistency_analysis": {},
        }

        ranges = results["ranges"]
        data = results["data"]

        # Analyze each range
        for min_val, max_val in ranges:
            range_key = f"{min_val}-{max_val}"
            all_numbers = []

            # Collect all numbers for this range across all runs
            for run_key, run_data in data.items():
                if range_key in run_data:
                    all_numbers.extend(run_data[range_key])

            if all_numbers:
                numbers_array = np.array(all_numbers)
                expected_mean = (min_val + max_val) / 2
                expected_std = (max_val - min_val) / np.sqrt(
                    12
                )  # For uniform distribution

                analysis["range_analysis"][range_key] = {
                    "total_samples": len(numbers_array),
                    "actual_mean": float(np.mean(numbers_array)),
                    "expected_mean": expected_mean,
                    "mean_bias": float(np.mean(numbers_array) - expected_mean),
                    "actual_std": float(np.std(numbers_array)),
                    "expected_std": expected_std,
                    "std_ratio": float(np.std(numbers_array) / expected_std),
                    "min": float(np.min(numbers_array)),
                    "max": float(np.max(numbers_array)),
                    "range_coverage": float(
                        (np.max(numbers_array) - np.min(numbers_array))
                        / (max_val - min_val)
                    ),
                    "uniformity_test": self._test_uniformity(
                        numbers_array, min_val, max_val
                    ),
                }

        # Analyze bias patterns across ranges
        analysis["bias_analysis"] = self._analyze_bias_patterns(
            analysis["range_analysis"]
        )

        # Analyze consistency across runs
        analysis["consistency_analysis"] = self._analyze_consistency(data, ranges)

        return analysis

    def _test_uniformity(
        self, numbers: np.ndarray, min_val: float, max_val: float
    ) -> Dict:
        """
        Test if the numbers follow a uniform distribution.

        Args:
            numbers (np.ndarray): Array of numbers
            min_val (float): Minimum value of the range
            max_val (float): Maximum value of the range

        Returns:
            Dict: Uniformity test results
        """
        # Normalize numbers to [0, 1] range
        normalized = (numbers - min_val) / (max_val - min_val)

        # Perform Kolmogorov-Smirnov test for uniformity
        ks_statistic, p_value = stats.kstest(normalized, "uniform")

        # Perform chi-square test (divide into bins)
        bins = np.linspace(0, 1, 11)  # 10 bins
        observed, _ = np.histogram(normalized, bins=bins)
        expected = (
            len(normalized) / 10
        )  # Expected count per bin for uniform distribution
        chi2_statistic, chi2_p_value = stats.chisquare(observed, [expected] * 10)

        return {
            "ks_statistic": float(ks_statistic),
            "ks_p_value": float(p_value),
            "is_uniform_ks": p_value > 0.05,
            "chi2_statistic": float(chi2_statistic),
            "chi2_p_value": float(chi2_p_value),
            "is_uniform_chi2": chi2_p_value > 0.05,
        }

    def _analyze_bias_patterns(self, range_analysis: Dict) -> Dict:
        """
        Analyze bias patterns across different ranges.

        Args:
            range_analysis (Dict): Analysis results for each range

        Returns:
            Dict: Bias pattern analysis
        """
        biases = []
        ranges = []

        for range_key, analysis in range_analysis.items():
            biases.append(analysis["mean_bias"])
            ranges.append(range_key)

        return {
            "mean_bias": float(np.mean(biases)),
            "bias_std": float(np.std(biases)),
            "bias_range": float(np.max(biases) - np.min(biases)),
            "bias_by_range": dict(zip(ranges, biases)),
        }

    def _analyze_consistency(
        self, data: Dict, ranges: List[Tuple[float, float]]
    ) -> Dict:
        """
        Analyze consistency across different runs.

        Args:
            data (Dict): Generated data across runs
            ranges (List[Tuple[float, float]]): List of ranges

        Returns:
            Dict: Consistency analysis results
        """
        consistency = {}

        for min_val, max_val in ranges:
            range_key = f"{min_val}-{max_val}"
            run_means = []
            run_stds = []

            for run_key, run_data in data.items():
                if range_key in run_data and run_data[range_key]:
                    numbers = np.array(run_data[range_key])
                    run_means.append(np.mean(numbers))
                    run_stds.append(np.std(numbers))

            if run_means:
                consistency[range_key] = {
                    "mean_consistency": float(
                        np.std(run_means)
                    ),  # Lower is more consistent
                    "std_consistency": float(np.std(run_stds)),
                    "cv_mean": float(
                        np.std(run_means) / np.mean(run_means)
                    ),  # Coefficient of variation
                    "cv_std": float(np.std(run_stds) / np.mean(run_stds)),
                    "run_means": [float(m) for m in run_means],
                    "run_stds": [float(s) for s in run_stds],
                }

        return consistency

    def create_visualizations(
        self, results: Dict, analysis: Dict, save_path: str = "analysis_results"
    ):
        """
        Create comprehensive visualizations of the analysis results.

        Args:
            results (Dict): Results from NumberGenerator.run_consistency_test()
            analysis (Dict): Analysis results from analyze_distribution()
            save_path (str): Path to save the visualizations
        """
        # Create figure with subplots
        fig = plt.figure(figsize=(20, 16))

        # 1. Distribution plots for each range
        self._plot_distributions(results, fig, 2, 3, 1)

        # 2. Bias analysis
        self._plot_bias_analysis(analysis, fig, 2, 3, 2)

        # 3. Consistency across runs
        self._plot_consistency(analysis, fig, 2, 3, 3)

        # 4. Uniformity test results
        self._plot_uniformity_tests(analysis, fig, 2, 3, 4)

        # 5. Range coverage analysis
        self._plot_range_coverage(analysis, fig, 2, 3, 5)

        # 6. Summary statistics
        self._plot_summary_stats(results, fig, 2, 3, 6)

        plt.tight_layout()
        plt.savefig(f"{save_path}_visualizations.png", dpi=300, bbox_inches="tight")
        plt.show()

    def _plot_distributions(self, results: Dict, fig, rows: int, cols: int, pos: int):
        """Plot distributions for each range."""
        ax = plt.subplot(rows, cols, pos)

        data = results["data"]
        ranges = results["ranges"]

        for min_val, max_val in ranges:
            range_key = f"{min_val}-{max_val}"
            all_numbers = []

            for run_key, run_data in data.items():
                if range_key in run_data:
                    all_numbers.extend(run_data[range_key])

            if all_numbers:
                ax.hist(
                    all_numbers, alpha=0.6, label=f"[{min_val}, {max_val}]", bins=20
                )

        ax.set_xlabel("Generated Numbers")
        ax.set_ylabel("Frequency")
        ax.set_title("Distribution by Range")
        ax.legend()
        ax.grid(True, alpha=0.3)

    def _plot_bias_analysis(self, analysis: Dict, fig, rows: int, cols: int, pos: int):
        """Plot bias analysis."""
        ax = plt.subplot(rows, cols, pos)

        range_analysis = analysis["range_analysis"]
        ranges = list(range_analysis.keys())
        biases = [range_analysis[r]["mean_bias"] for r in ranges]

        bars = ax.bar(range(len(ranges)), biases)
        ax.set_xlabel("Range")
        ax.set_ylabel("Mean Bias")
        ax.set_title("Bias Analysis by Range")
        ax.set_xticks(range(len(ranges)))
        ax.set_xticklabels(ranges, rotation=45)

        # Color bars based on bias direction
        for bar, bias in zip(bars, biases):
            if bias > 0:
                bar.set_color("red")
            else:
                bar.set_color("blue")

        ax.axhline(y=0, color="black", linestyle="-", alpha=0.5)
        ax.grid(True, alpha=0.3)

    def _plot_consistency(self, analysis: Dict, fig, rows: int, cols: int, pos: int):
        """Plot consistency across runs."""
        ax = plt.subplot(rows, cols, pos)

        consistency = analysis["consistency_analysis"]
        ranges = list(consistency.keys())
        cv_means = [consistency[r]["cv_mean"] for r in ranges]

        ax.bar(range(len(ranges)), cv_means)
        ax.set_xlabel("Range")
        ax.set_ylabel("Coefficient of Variation (Mean)")
        ax.set_title("Consistency Across Runs")
        ax.set_xticks(range(len(ranges)))
        ax.set_xticklabels(ranges, rotation=45)
        ax.grid(True, alpha=0.3)

    def _plot_uniformity_tests(
        self, analysis: Dict, fig, rows: int, cols: int, pos: int
    ):
        """Plot uniformity test results."""
        ax = plt.subplot(rows, cols, pos)

        range_analysis = analysis["range_analysis"]
        ranges = list(range_analysis.keys())
        ks_p_values = [
            range_analysis[r]["uniformity_test"]["ks_p_value"] for r in ranges
        ]
        chi2_p_values = [
            range_analysis[r]["uniformity_test"]["chi2_p_value"] for r in ranges
        ]

        x = np.arange(len(ranges))
        width = 0.35

        ax.bar(x - width / 2, ks_p_values, width, label="KS Test", alpha=0.7)
        ax.bar(x + width / 2, chi2_p_values, width, label="Chi² Test", alpha=0.7)

        ax.set_xlabel("Range")
        ax.set_ylabel("P-value")
        ax.set_title("Uniformity Test Results")
        ax.set_xticks(x)
        ax.set_xticklabels(ranges, rotation=45)
        ax.axhline(y=0.05, color="red", linestyle="--", alpha=0.7, label="α=0.05")
        ax.legend()
        ax.grid(True, alpha=0.3)

    def _plot_range_coverage(self, analysis: Dict, fig, rows: int, cols: int, pos: int):
        """Plot range coverage analysis."""
        ax = plt.subplot(rows, cols, pos)

        range_analysis = analysis["range_analysis"]
        ranges = list(range_analysis.keys())
        coverages = [range_analysis[r]["range_coverage"] for r in ranges]

        ax.bar(range(len(ranges)), coverages)
        ax.set_xlabel("Range")
        ax.set_ylabel("Coverage Ratio")
        ax.set_title("Range Coverage Analysis")
        ax.set_xticks(range(len(ranges)))
        ax.set_xticklabels(ranges, rotation=45)
        ax.axhline(y=1.0, color="red", linestyle="--", alpha=0.7, label="Full Coverage")
        ax.legend()
        ax.grid(True, alpha=0.3)

    def _plot_summary_stats(self, results: Dict, fig, rows: int, cols: int, pos: int):
        """Plot summary statistics."""
        ax = plt.subplot(rows, cols, pos)

        # Create a summary table
        stats_data = []
        for min_val, max_val in results["ranges"]:
            range_key = f"{min_val}-{max_val}"
            all_numbers = []

            for run_key, run_data in results["data"].items():
                if range_key in run_data:
                    all_numbers.extend(run_data[range_key])

            if all_numbers:
                numbers_array = np.array(all_numbers)
                stats_data.append(
                    [
                        range_key,
                        len(numbers_array),
                        f"{np.mean(numbers_array):.3f}",
                        f"{np.std(numbers_array):.3f}",
                        f"{np.min(numbers_array):.3f}",
                        f"{np.max(numbers_array):.3f}",
                    ]
                )

        # Create table
        table = ax.table(
            cellText=stats_data,
            colLabels=["Range", "Count", "Mean", "Std", "Min", "Max"],
            cellLoc="center",
            loc="center",
        )
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)

        ax.set_title("Summary Statistics")
        ax.axis("off")

    def save_results(
        self, results: Dict, analysis: Dict, filename: str = "analysis_results.json"
    ):
        """
        Save results and analysis to a JSON file.

        Args:
            results (Dict): Results from NumberGenerator.run_consistency_test()
            analysis (Dict): Analysis results from analyze_distribution()
            filename (str): Output filename
        """
        output = {
            "results": results,
            "analysis": analysis,
            "summary": self._create_summary(analysis),
        }

        with open(filename, "w") as f:
            json.dump(output, f, indent=2, default=str)

        print(f"Results saved to {filename}")

    def _create_summary(self, analysis: Dict) -> Dict:
        """
        Create a summary of the analysis results.

        Args:
            analysis (Dict): Analysis results

        Returns:
            Dict: Summary of key findings
        """
        range_analysis = analysis["range_analysis"]
        bias_analysis = analysis["bias_analysis"]
        consistency_analysis = analysis["consistency_analysis"]

        summary = {
            "total_ranges_tested": len(range_analysis),
            "overall_bias": bias_analysis["mean_bias"],
            "most_biased_range": max(
                bias_analysis["bias_by_range"].items(), key=lambda x: abs(x[1])
            )[0],
            "least_consistent_range": min(
                consistency_analysis.items(), key=lambda x: x[1]["cv_mean"]
            )[0],
            "uniformity_findings": {},
        }

        # Count uniformity test results
        uniform_ks = 0
        uniform_chi2 = 0
        total_tests = len(range_analysis)

        for range_key, range_data in range_analysis.items():
            uniformity = range_data["uniformity_test"]
            if uniformity["is_uniform_ks"]:
                uniform_ks += 1
            if uniformity["is_uniform_chi2"]:
                uniform_chi2 += 1

        summary["uniformity_findings"] = {
            "ks_test_uniform": f"{uniform_ks}/{total_tests}",
            "chi2_test_uniform": f"{uniform_chi2}/{total_tests}",
            "ks_uniformity_rate": uniform_ks / total_tests,
            "chi2_uniformity_rate": uniform_chi2 / total_tests,
        }

        return summary
