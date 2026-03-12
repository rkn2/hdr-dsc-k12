#!/usr/bin/env python3
"""Semantic rewriting of Chapter_15.ipynb → Chapter_15_EM.ipynb"""
import json, copy, re

INPUT_NB = "Chapter_15.ipynb"
OUTPUT_NB = "Chapter_15_EM.ipynb"
CELL_REPLACEMENTS = {}

# ── Cell 2: Insurance expected value → Structural warranty ────
CELL_REPLACEMENTS[2] = """**<span class="mark">Probability Models</span>**

<span class="mark">A **probability model** for a random variable consists of:</span>

- <span class="mark">the collection of all possible values of a random variable, and</span>
- <span class="mark">the probabilities that the values occur.</span>

<span class="mark">Of particular interest is the value we expect a random variable to take on in the long run, notated *μ* (for population mean) or *E(X)* for **expected value**.</span>

<span class="mark">The **expected value** of a (discrete) random variable can be found by summing the products of each possible value by the probability that it occurs:</span>

> <span class="mark">$E(X) = \\sum x \\cdot P(x)$</span>

<span class="mark">Example: A structural engineering firm offers a 5-year retrofit warranty on bridge decks. Based on historical data:</span>

| <span class="mark">Outcome</span> | <span class="mark">Payout (x)</span> | <span class="mark">Probability P(x)</span> |
|---|---|---|
| <span class="mark">No claim</span> | <span class="mark">$0</span> | <span class="mark">0.90</span> |
| <span class="mark">Minor repair</span> | <span class="mark">$5,000</span> | <span class="mark">0.07</span> |
| <span class="mark">Major repair</span> | <span class="mark">$25,000</span> | <span class="mark">0.025</span> |
| <span class="mark">Full replacement</span> | <span class="mark">$100,000</span> | <span class="mark">0.005</span> |

<span class="mark">$E(X) = 0(0.90) + 5000(0.07) + 25000(0.025) + 100000(0.005) = \\$1,475$</span>

<span class="mark">The firm should charge **more than $1,475** per warranty to cover expected costs and remain profitable.</span>
"""

# ── Cell 4: Geometric model — generic → weld inspection waiting ──
CELL_REPLACEMENTS[4] = """### Interactive Experiment: The Waiting Game (Geometric Model)

While the **Binomial** model counts successes in a fixed number of trials, the **Geometric** model counts how many trials it takes to get **one** success.

*   **Example:** How many welds must an inspector examine before finding the first defect? If the defect rate is *p* = 0.05 (5%), you might inspect many welds before finding one.

*   **Explore:** Change *p* and see how the "Wait Time" changes. If *p* is small (rare defects), you might wait a long time!
"""

# ── Cell 7: M&M's gimmick → Structural bolt QC ───────────────
CELL_REPLACEMENTS[7] = """**<span class="mark">RECALL:</span>** <span class="mark">In n trials, there are ways to have k successes.</span>

<span class="mark">Binomial probability model for Bernoulli trials: Binom(n,p)</span>

<span class="mark">n = number of trials</span>
<span class="mark">p = probability of success</span>
<span class="mark">q = 1 – p = probability of failure</span>
<span class="mark">X = \\# of successes in n trials</span>

$$

<span class="mark">Examples: A quality control protocol flags 30% of high-strength bolts for additional torque verification. These flagged bolts are mixed randomly in the production bins. You pull 12 bolts from a bin one at a time.</span>

<span class="mark">a) How many flagged bolts do you expect to find?</span>

<span class="mark">$E(X) = np = 12(0.30) = 3.6$ flagged bolts.</span>

<span class="mark">b) What is the standard deviation?</span>

<span class="mark">$SD(X) = \\sqrt{npq} = \\sqrt{12(0.30)(0.70)} = \\sqrt{2.52} \\approx 1.59$ bolts.</span>

<span class="mark">c) It would be unusual to find more than $3.6 + 2(1.59) = 6.78$, or about 7 flagged bolts in a sample of 12.</span>
"""

# ── Cell 10: Mortality/insurance → Structural reliability ──────
CELL_REPLACEMENTS[10] = """**<span class="mark">Normal Approximation for the Binomial Model:</span>**

- <span class="mark">Binomial problems sometimes cover too many options.</span>

- <span class="mark">When a binomial problem grows to be big and unwieldy, we can use a Normal Model!</span>

- <span class="mark">**The Success/Failure Condition** states that a Binomial model is approximately Normal if:</span>

  - <span class="mark">np ≥ 10 and nq ≥ 10. (We expect at least 10 successes and at least 10 failures.)</span>

<span class="mark">Example: Structural reliability analysis shows that a particular type of steel connection has a 97% probability of withstanding its design load over a 50-year service life. An engineer inspects 200 such connections in a building.</span>

<span class="mark">Find the probability that more than 8 connections will fail to meet specification during the service life.</span>

<span class="mark">n = 200, p = 0.03 (failure probability), q = 0.97</span>

<span class="mark">np = 6, nq = 194 → np < 10, so the Normal approximation is borderline. Let's check with an exact Binomial calculation as well.</span>

<span class="mark">$\\mu = np = 6$, $\\sigma = \\sqrt{npq} = \\sqrt{200(0.03)(0.97)} \\approx 2.41$</span>

<span class="mark">$z = \\frac{8.5 - 6}{2.41} \\approx 1.04$</span>

<span class="mark">$P(X > 8) \\approx P(z > 1.04) \\approx 0.149$</span>
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
    bad = ["insurance", "M&M", "speckle", "groovy", "candy", "candies",
           "mortality", "actuary", "actuaries", "die until"]
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
