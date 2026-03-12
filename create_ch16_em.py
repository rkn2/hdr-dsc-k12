#!/usr/bin/env python3
"""Semantic rewriting of Chapter_16.ipynb → Chapter_16_EM.ipynb"""
import json, copy, re

INPUT_NB = "Chapter_16.ipynb"
OUTPUT_NB = "Chapter_16_EM.ipynb"
CELL_REPLACEMENTS = {}

# ── Cell 3: Assumptions — speeders, voters, M&Ms → EM examples ──
CELL_REPLACEMENTS[3] = """**<span class="mark">Assumptions and Conditions:</span>**

- <span class="mark">**The Independence Assumption:** The sampled values must be independent of each other.</span>

- <span class="mark">**Randomization Condition**: The sample should be a simple random sample of the population.</span>

- <span class="mark">**10% Condition:** the sample size, n, must be no larger than 10% of the population</span>

- <span class="mark">**The Sample Size Assumption:** The sample size, n, must be large enough.</span>

  - <span class="mark">**Success/Failure Condition:** The sample size has to be big enough so that both np (number of successes) and nq (number of failures) are at least 10.</span>

  - <span class="mark">Basically, we need a large enough sample that is not too large.</span>

<span class="mark">Examples:</span>

<span class="mark">1. Of all concrete cylinders produced by a batch plant, 80% exceed the minimum 28-day compressive strength specification. What proportion of conforming cylinders might we see among the next 50 cylinders tested?</span>

<span class="mark">2. We don't know it, but 52% of bridges in a state's inventory are rated "Good" or better. We inspect a random sample of 300 bridges. What might the percentage of "Good"-rated bridges appear to be in our sample?</span>

<span class="mark">3. High-strength bolts with proper pre-tension are supposed to make up 30% of all bolts in a structural connection. In a large shipment of 250 bolts, what is the probability that we find at least 25% are properly pre-tensioned?</span>
"""

# ── Cell 4: Vocabulary + voter/medicine examples → EM examples ──
CELL_REPLACEMENTS[4] = """**<span class="mark">Key Vocabulary:</span>**

- <span class="mark">Standard error: When we estimate the standard deviation of a sampling distribution using statistics found from the data, the estimate is called a standard error:</span>

> <span class="mark">$SE(\\widehat{p}) = \\sqrt{\\frac{\\widehat{p}\\widehat{q}}{n}}$</span>

- <span class="mark">Confidence level: A level C confidence interval for a model parameter is an interval of values usually of the form *Estimate ± Margin of Error* found from data in such a way that C% of all random samples will yield intervals that capture the true parameter value.</span>

- <span class="mark">Confidence interval: A confidence interval for the true value of a proportion. The confidence interval is</span>

> <span class="mark">$\\widehat{p} \\pm z*SE\\left( \\ \\widehat{p}\\ \\right)$</span>
>
> <span class="mark">where z\\* is a critical value from the Standard Normal model corresponding to the specified confidence level.</span>

- <span class="mark">Margin of error: In a confidence interval, the extent of the interval on either side of the observed statistic value is called the margin of error. A margin of error is typically the product of a critical value from the sampling distribution and a standard error from the data. A small margin of error corresponds to a confidence interval that pins down the parameter precisely. A large margin of error corresponds to a confidence interval that gives relatively little information about the estimated parameter. For a proportion</span>

> <span class="mark">$ME = z* \\cdot SE(\\widehat{p})$</span>

- <span class="mark">Critical value: The number of standard errors to move away from the sample statistic to specify an interval that corresponds to the specified level of confidence. The critical value, denoted z\\*, is usually found from a table or with technology.</span>

<span class="mark">Examples:</span>

<span class="mark">Your state DOT inspects a random sample of 330 bridges, finding 144 that are rated "structurally deficient." Create a 95% confidence interval for the actual proportion of structurally deficient bridges statewide.</span>

<span class="mark">A materials study finds that 27% of 53 concrete cylinders from a new mix design meet the enhanced strength specification. Create a 95% confidence interval for the true pass rate. Why is this interval so wide? Make it narrower – 90% confidence. What are the advantages and disadvantages?</span>

<span class="mark">What sample size would we need in a follow-up study if we want a margin of error of 5% with 98% confidence?</span>

<span class="mark">What sample size does it take to estimate the proportion of non-conforming welds in a fabrication shop with a margin of error of 3%?</span>
"""


def main():
    with open(INPUT_NB, "r", encoding="utf-8") as f:
        nb = json.load(f)
    nb_em = copy.deepcopy(nb)
    for idx, new_source in CELL_REPLACEMENTS.items():
        if idx < len(nb_em["cells"]):
            cell = nb_em["cells"][idx]
            if isinstance(cell.get("source"), list):
                lines = new_source.split("\n")
                cell["source"] = [line + "\n" for line in lines[:-1]] + [lines[-1]]
            else:
                cell["source"] = new_source
    with open(OUTPUT_NB, "w", encoding="utf-8") as f:
        json.dump(nb_em, f, indent=1)
    print(f"✅ Created {OUTPUT_NB}")

    with open(OUTPUT_NB, "r") as f:
        text = f.read()
    clean = re.sub(r'data:image/[^"]+', '', text)
    bad = ["voter", "school budget", "election", "M&M", "groovy", "candies",
           "speeders", "interstate", "medicine", "cure rate"]
    print("\n--- Coherence Critic ---")
    fails = 0
    for w in bad:
        if w.lower() in clean.lower():
            print(f"  ❌ FAIL: Found \"{w}\"")
            fails += 1
    if fails == 0:
        print("  🎉 All clear!")
    
    print("\n--- Nonsense Critic ---")
    nb_c = json.load(open(OUTPUT_NB))
    for idx in sorted(CELL_REPLACEMENTS.keys()):
        cell = nb_c["cells"][idx]
        src = "".join(cell.get("source", "")) if isinstance(cell.get("source"), list) else cell.get("source", "")
        preview = re.sub(r'<[^>]+>', '', src)
        preview = re.sub(r'\s+', ' ', preview).strip()[:180]
        print(f"  Cell {idx}: {preview}...")

if __name__ == "__main__":
    main()
