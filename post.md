---
author: "Abhay Vashist"
title: "LLM Number Generation"
date: 2025-08-27T02:27:22+0000
description: "Can LLM generate numbers"
tags: ["llm", "python", "visualization"]
series: ["Personal Project"]
aliases: ["/llm_number_generation"]
weight: 1
draft: false
ShowToc: true
TocOpen: true
cover:
    image: 
---

## Exploring the Randomness of LLMs

Large Language Models (LLMs) have become central to modern development—powering everything from **RAG systems** to **AI agents** that assist with our daily tasks.

Yet, most developers who rely on LLMs rarely pause to **explore their behavior**. Instead, they rely on benchmarks, anecdotal usage, or viral posts on X to form their mental models of what LLMs can (or cannot) do.

I believe this is risky—it creates a gap between people who use these models and those who deeply evaluate them. To help bridge that gap, I decided to run a simple but fun experiment:

## Can LLMs Generate Random Numbers?

At first glance, this seems trivial. We know that LLMs cannot produce true randomness—they don’t have an internal random number generator. But the real question is:

👉 *Do LLMs show bias toward certain numbers when asked to generate a random one?*
👉 *Does this bias change across different models or families of models?*

That’s what I set out to explore.

---

### Experiment Setup

I designed a small test program to measure four things:

* The **range of values** generated when asked for random numbers
* The **bias** compared to a uniform random distribution
* The **consistency** of results across trials
* How results vary across **different models and families**

**Prompts used:**

```python
prompts = {
    "direct": f"Generate a random number between {min_val} and {max_val}. Return only the number, no explanation.",
    "creative": f"Imagine you're a random number generator. Pick any number between {min_val} and {max_val}. Just return the number.",
    "precise": f"Please provide exactly one number that falls within the range [{min_val}, {max_val}]. Return only the numeric value.",
}
```

**Models tested:**

* GPT-4.1
* GPT-4.1 Mini
* Claude 3.5 Haiku
* Claude 4 Sonnet

**Experiment parameters:**

* Number of trials = 5
* Temperature = 0.7
* Number ranges tested:

  * \[-1, 1]
  * \[-10, 10]
  * \[-100, 0]
  * \[0, 1]
  * \[0, 100]
  * \[1, 10]
  * \[1, 100]


**Total Cost:**
- OpenAI API Cost = $10
- Claude API Cost = $10

---

### Results

#### GPT-4.1 Mini


![](https://raw.githubusercontent.com/Avashist1998/LLMExploration/refs/heads/main/plots/gpt-4.1-mini-200-samples-5-trials/analysis_results_gpt-4.1-mini_visualizations.png)


![](https://raw.githubusercontent.com/Avashist1998/LLMExploration/refs/heads/main/plots/gpt-4.1-mini-200-samples-5-trials/bias_analysis.png)


#### GPT-4.1

![](https://raw.githubusercontent.com/Avashist1998/LLMExploration/refs/heads/main/plots/gpt-4.1-200-samples-5-trials/analysis_results_gpt-4.1_visualizations.png)



![](https://raw.githubusercontent.com/Avashist1998/LLMExploration/refs/heads/main/plots/gpt-4.1-200-samples-5-trials/bias_analysis.png)

#### Claude 3.5 Haiku

![](https://raw.githubusercontent.com/Avashist1998/LLMExploration/refs/heads/main/plots/claude-3-5-haiku-200-sample-5-trials/analysis_results_claude-3-5-haiku-20241022_visualizations.png)

![](https://raw.githubusercontent.com/Avashist1998/LLMExploration/refs/heads/main/plots/claude-3-5-haiku-200-sample-5-trials/bias_analysis.png)

#### Claude 3.7 Sonnet

---


### Learnings

This is just the beginning—I’ll share the charts and visualizations next to show how each model behaves under the same conditions. The patterns are… surprising.

