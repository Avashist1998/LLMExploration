import os
import json
import time
import random
from typing import List, Dict, Tuple, Optional
from openai import OpenAI
from dotenv import load_dotenv
import numpy as np


class NumberGenerator:
    """
    A class to generate numbers using OpenAI models and analyze their distribution patterns.
    """

    def __init__(self, model: str = "gpt-3.5-turbo"):
        """
        Initialize the NumberGenerator with OpenAI client.

        Args:
            model (str): The OpenAI model to use for generation
        """
        load_dotenv(override=True)

        if "gpt" in model:
            self.url = "https://api.openai.com/v1"
            api_key = os.getenv("OPENAI_API_KEY")

        elif "claude" in model:
            self.url = "https://api.anthropic.com/v1/"
            api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            raise ValueError(
                "API_KEY not found in environment variables. Please set it in your .env file."
            )

        # Initialize OpenAI client with minimal configuration
        print("Initializing OpenAI client... with model: ", model)
        self.client = OpenAI(base_url=self.url, api_key=api_key)
        print("OpenAI client initialized")
        self.model = model
        print("Model set to: ", self.model)

    def generate_number(
        self, min_val: float, max_val: float, prompt_type: str = "direct"
    ) -> Optional[float]:
        """
        Generate a single number within the specified range.

        Args:
            min_val (float): Minimum value of the range
            max_val (float): Maximum value of the range
            prompt_type (str): Type of prompt to use ("direct", "creative", "precise")

        Returns:
            Optional[float]: Generated number or None if failed
        """
        prompts = {
            "direct": f"Generate a random number between {min_val} and {max_val}. Return only the number, no explanation.",
            "creative": f"Imagine you're a random number generator. Pick any number between {min_val} and {max_val}. Just return the number.",
            "precise": f"Please provide exactly one number that falls within the range [{min_val}, {max_val}]. Return only the numeric value.",
        }

        prompt = prompts.get(prompt_type, prompts["direct"])

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a precise number generator. Always respond with only the requested number.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=10,
            )

            result = response.choices[0].message.content
            if result is None:
                print("Warning: Empty response from model")
                return None

            result = result.strip()

            # Try to extract number from response
            try:
                # Remove any non-numeric characters except decimal points and minus signs
                cleaned = "".join(c for c in result if c.isdigit() or c in ".-")
                number = float(cleaned)

                # Check if number is within range
                if min_val <= number <= max_val:
                    return number
                else:
                    print(
                        f"Warning: Generated number {number} outside range [{min_val}, {max_val}]"
                    )
                    return None

            except ValueError:
                print(f"Warning: Could not parse number from response: '{result}'")
                return None

        except Exception as e:
            print(f"Error generating number: {e}")
            return None

    def generate_batch(
        self,
        min_val: float,
        max_val: float,
        count: int,
        prompt_type: str = "direct",
        delay: float = 0.1,
    ) -> List[float]:
        """
        Generate a batch of numbers within the specified range.

        Args:
            min_val (float): Minimum value of the range
            max_val (float): Maximum value of the range
            count (int): Number of numbers to generate
            prompt_type (str): Type of prompt to use
            delay (float): Delay between API calls in seconds

        Returns:
            List[float]: List of generated numbers
        """
        numbers = []

        for i in range(count):
            number = self.generate_number(min_val, max_val, prompt_type)
            if number is not None:
                numbers.append(number)

            # Add delay to avoid rate limiting
            if i < count - 1:
                time.sleep(delay)

        return numbers

    def run_consistency_test(
        self,
        ranges: List[Tuple[float, float]],
        samples_per_range: int = 100,
        runs: int = 5,
        prompt_type: str = "direct",
    ) -> Dict:
        """
        Run multiple tests to check consistency across different ranges and runs.

        Args:
            ranges (List[Tuple[float, float]]): List of (min, max) ranges to test
            samples_per_range (int): Number of samples to generate per range
            runs (int): Number of runs to perform
            prompt_type (str): Type of prompt to use

        Returns:
            Dict: Results containing all generated numbers and statistics
        """
        results = {
            "ranges": ranges,
            "samples_per_range": samples_per_range,
            "runs": runs,
            "prompt_type": prompt_type,
            "data": {},
            "statistics": {},
        }

        for run in range(runs):
            print(f"Running test {run + 1}/{runs}...")
            run_data = {}

            for min_val, max_val in ranges:
                range_key = f"{min_val}-{max_val}"
                print(
                    f"  Generating {samples_per_range} numbers in range [{min_val}, {max_val}]..."
                )

                numbers = self.generate_batch(
                    min_val, max_val, samples_per_range, prompt_type
                )
                run_data[range_key] = numbers

            results["data"][f"run_{run + 1}"] = run_data

        # Calculate statistics
        results["statistics"] = self._calculate_statistics(results["data"])

        return results

    def _calculate_statistics(self, data: Dict) -> Dict:
        """
        Calculate statistical measures for the generated data.

        Args:
            data (Dict): The generated data

        Returns:
            Dict: Statistical measures
        """
        stats = {}

        for run_key, run_data in data.items():
            stats[run_key] = {}

            for range_key, numbers in run_data.items():
                if numbers:
                    numbers_array = np.array(numbers)
                    stats[run_key][range_key] = {
                        "count": len(numbers),
                        "mean": float(np.mean(numbers_array)),
                        "std": float(np.std(numbers_array)),
                        "min": float(np.min(numbers_array)),
                        "max": float(np.max(numbers_array)),
                        "median": float(np.median(numbers_array)),
                        "q25": float(np.percentile(numbers_array, 25)),
                        "q75": float(np.percentile(numbers_array, 75)),
                    }

        return stats
