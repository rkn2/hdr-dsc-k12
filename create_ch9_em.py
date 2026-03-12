#!/usr/bin/env python3
"""
Semantic rewriting of Chapter_9.ipynb → Chapter_9_EM.ipynb

Instead of find-and-replace, this script:
1. Loads the original notebook as JSON
2. Replaces specific cells (by index) with fully rewritten content
3. Writes Chapter_9_EM.ipynb
4. Runs a self-critic to check for leftover nonsensical content
"""

import json
import copy
import re
import sys

INPUT_NB = "Chapter_9.ipynb"
OUTPUT_NB = "Chapter_9_EM.ipynb"

# ─────────────────────────────────────────────────────────────
# CELL REPLACEMENTS
# Each key is the cell index in the original notebook.
# Each value is the new source content (as a single string).
# ─────────────────────────────────────────────────────────────

CELL_REPLACEMENTS = {}

# ── Cell 3: Interactive Experiment intro (markdown) ──────────
CELL_REPLACEMENTS[3] = """### 🧪 Interactive Experiment: The Danger of Bias

**Bias** is a systematic error. It's not just "bad luck" — it's like a load cell that is always 50 lbs off.

In this simulation, we know the **True Population Mean** compressive strength of concrete cylinders is **4000 psi**.
Try the two different sampling methods:

1.  **Simple Random Sample (SRS):** Every cylinder from the full production run has an equal chance of being selected.
    *   *Try changing the sample size.* Does the Sample Mean stay close to the True Mean?
2.  **Convenience Sample:** Imagine you only test cylinders from a high-performance batch (cured under ideal lab conditions).
    *   *What happens to the Sample Mean?*
    *   *Does increasing the sample size fix the error?* (Hint: NO!)
"""

# ── Cell 4: Widget code (code) ───────────────────────────────
CELL_REPLACEMENTS[4] = """# @title Click 'Play' to Run Code
import matplotlib.pyplot as plt
import numpy as np
import ipywidgets as widgets
from IPython.display import display

# Generate Population Data (once)
np.random.seed(42)
population_size = 1000
# True Population: Average compressive strength 4000 psi, std dev 500 psi
true_mean = 4000
population = np.random.normal(true_mean, 500, population_size)

# Create a "Biased" sub-group (e.g., high-performance batch cylinders are stronger)
# Cylinders with higher strength are more likely to be in the "Convenience" location
bias_weight = (population - 2500) / 1500
bias_probs = np.exp(bias_weight) / np.sum(np.exp(bias_weight))

def run_sampling_sim(sample_method, sample_size):
    plt.figure(figsize=(10, 6))

    # 1. Plot Population Distribution (Grey background)
    plt.hist(population, bins=30, alpha=0.3, color='grey', label='Full Production Run (Ground Truth)', density=True)
    plt.axvline(true_mean, color='black', linestyle='--', linewidth=2, label=f'True Mean ({true_mean:.0f} psi)')

    # 2. Draw Sample
    if sample_method == 'Simple Random Sample (SRS)':
        # Every cylinder has equal chance
        sample_data = np.random.choice(population, size=sample_size, replace=False)
        color = 'blue'
        title_extra = "unbiased"
    else: # Convenience Sample (Biased)
        # Stronger cylinders are more likely to be selected
        sample_data = np.random.choice(population, size=sample_size, replace=False, p=bias_probs)
        color = 'red'
        title_extra = "BIASED towards high-strength specimens"

    # 3. Plot Sample Distribution
    sample_mean = np.mean(sample_data)
    plt.hist(sample_data, bins=15, alpha=0.7, color=color, label=f'Your Sample (n={sample_size})', density=True)
    plt.axvline(sample_mean, color=color, linestyle='-', linewidth=3, label=f'Sample Mean ({sample_mean:.0f} psi)')

    plt.title(f"Sampling Method: {sample_method}\\nSample Average: {sample_mean:.0f} psi (True: {true_mean:.0f} psi)", fontsize=14)
    plt.xlabel("Compressive Strength (psi)")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Educational Note
    if sample_method != 'Simple Random Sample (SRS)' and abs(sample_mean - true_mean) > 200:
        plt.text(2200, 0.0006, "Notice: Bias pushes the\\nresult away from truth!",
                 color='red', fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
        if sample_size > 200:
             plt.text(2200, 0.0003, "Even a LARGE biased sample\\nis still WRONG!",
                 color='darkred', fontsize=12, fontweight='bold', bbox=dict(facecolor='white', alpha=0.8))

    plt.show()

# UI Elements
style = {'description_width': 'initial'}
method_dropdown = widgets.Dropdown(
    options=['Simple Random Sample (SRS)', 'Convenience Sample (High-Performance Batch)'],
    value='Simple Random Sample (SRS)',
    description='Sampling Method:',
    style=style,
    layout=widgets.Layout(width='450px')
)

size_slider = widgets.IntSlider(
    value=50,
    min=10,
    max=500,
    step=10,
    description='Sample Size (n):',
    style=style
)

ui = widgets.VBox([method_dropdown, size_slider])
out = widgets.interactive_output(run_sampling_sim, {'sample_method': method_dropdown, 'sample_size': size_slider})

display(widgets.HTML("<h3>Experiment: Random vs. Biased Sampling</h3>"))
display(widgets.HTML("<b>Goal:</b> Estimate the average compressive strength of concrete cylinders from a production run."))
display(ui, out)
"""

# ── Cell 5: Historical anecdote — Landon → Tacoma Narrows (markdown) ──
CELL_REPLACEMENTS[5] = """**<span class="mark">Do you remember the Tacoma Narrows Bridge?</span>**

- <span class="mark">In 1940, the Tacoma Narrows Bridge in Washington State was one of the longest suspension bridges ever built. Engineers had conducted extensive wind tunnel testing before construction — they had a large "sample" of wind-load data.</span>

- <span class="mark">Their data predicted the bridge could easily handle sustained winds of 120 mph.</span>

- <span class="mark">On November 7, 1940, the bridge collapsed catastrophically in winds of only 42 mph — well within the bridge's supposed safe range.</span>

- <span class="mark">The engineers' sample wasn't representative of real-world conditions.</span>

- <span class="mark">Wind tunnel tests had only measured **steady-state** (laminar) wind loads. But in the real world, winds are turbulent and oscillating. The tests systematically excluded the kind of aerodynamic flutter that ultimately destroyed the bridge.</span>

- <span class="mark">This is the same lesson as with any biased sample: **no matter how much data you collect, if it's systematically missing a key part of the picture, your conclusions can be catastrophically wrong.**</span>
"""

# ── Cell 7: Idea 3 — minor tweak (markdown) ─────────────────
CELL_REPLACEMENTS[7] = """**<span class="mark">Idea 3: It's the Sample Size</span>**

<span class="mark">The **size of the sample**, not the size of the population, matters most.</span>

- <span class="mark">A sample of 100 can represent a single bridge or an entire highway system.</span>

- <span class="mark">The fraction of the population sampled does not matter.</span>

- <span class="mark">The necessary size of the sample depends on what is being estimated.</span>
"""

# ── Cell 8: Sample Size experiment intro (markdown) ──────────
CELL_REPLACEMENTS[8] = """
### Interactive Experiment: The Power of Sample Size

One of the key ideas in sampling is that **size matters**.
*   A small sample (e.g., testing 5 concrete cylinders) can yield results very far from the truth just by random chance.
*   A large sample (e.g., testing 500 cylinders) tends to be much closer to the truth.

**Try it:**
Move the slider to increase the **Sample Size ($n$)**.
Notice how the blue line (your sample average) swings wildly at the beginning but "settles down" near the red line (the true population average) as $n$ gets larger.

"""

# ── Cell 10: Does a Census Make Sense? (markdown) ────────────
CELL_REPLACEMENTS[10] = """**<span class="mark"><u>Does a Census Make Sense?</u></span>**

<span class="mark">Wouldn't it be better to just include everyone and \u201csample\u201d the entire population?</span>

- <span class="mark">Such a special sample is called a **census**.</span>

<span class="mark">There are problems with taking a census:</span>

- <span class="mark">It can be difficult to complete a census—there always seem to be some individuals who are hard (or expensive) to locate or hard to measure; or it may be impractical.</span>

  - <span class="mark">For example, destructive material testing (like crushing concrete cylinders to find their compressive strength) literally destroys the specimen — you can't test every single one or you'd have nothing left to build with.</span>

- <span class="mark">Populations rarely stand still. Even if you could take a census, the population changes while you work, so it's never possible to get a perfect measure.</span>

"""

# ── Cell 12: Parameter vs Statistic example (markdown) ───────
CELL_REPLACEMENTS[12] = """**<span class="mark">Example:</span>**

The Federal Highway Administration (FHWA) maintains the National Bridge Inventory, a database of every bridge in the United States. To assess structural conditions more efficiently, they conducted a detailed inspection of a "nationally representative sample" of 2032 bridges. Identify each of the following as a **parameter** or **statistic**:

1.  The proportion of all American bridges that are rated "structurally deficient."

2.  The proportion of these 2032 bridges that are rated "structurally deficient."

3.  The proportion of steel bridges in this sample that are rated "structurally deficient."

4.  The average annual maintenance cost for the bridges in this study.

5.  The average annual maintenance cost for all American bridges.
"""

# ── Cell 19: Systematic Sample (markdown) ────────────────────
CELL_REPLACEMENTS[19] = """**<span class="mark">Systematic Sample:</span>**

- <span class="mark">Individuals are selected systematically.</span>

  - <span class="mark">For example, every 10th weld on a structural steel fabrication line.</span>

  - <span class="mark">To make it random, you must still start the systematic selection from a randomly selected individual.</span>

- <span class="mark">Can be less expensive than true random sampling.</span>
"""

# ── Cell 23: Multistage title (markdown) ─────────────────────
CELL_REPLACEMENTS[23] = """**<span class="mark"><u>Example of Multistage Sampling in National Bridge Inspection</u></span>**
"""

# ── Cell 24: Stage 1 (markdown) ──────────────────────────────
CELL_REPLACEMENTS[24] = """**<span class="mark">Stage 1: Stratification by Climate Zone (Stratified Sampling)</span>**

- <span class="mark">The country is divided into AASHTO climate zones (e.g., Wet-Freeze, Wet-No Freeze, Dry-Freeze, Dry-No Freeze).</span>

- <span class="mark">This ensures that bridges exposed to different environmental stresses (freeze-thaw cycles, coastal salt spray, arid conditions) are represented proportionally.</span>
"""

# ── Cell 25: Stage 2 (markdown) ──────────────────────────────
CELL_REPLACEMENTS[25] = """**<span class="mark">Stage 2: Selection of State DOTs (Cluster Sampling)</span>**

- <span class="mark">Within each climate zone, a random selection of state Departments of Transportation (DOTs) is chosen.</span>

- <span class="mark">This reduces the need to inspect bridges in every state, making the program more practical and cost-effective.</span>
"""

# ── Cell 26: Stage 3 (markdown) ──────────────────────────────
CELL_REPLACEMENTS[26] = """**<span class="mark">Stage 3: Selection of Bridge Types (Cluster or Systematic Sampling)</span>**

- <span class="mark">Within each selected state, bridges are grouped by structural type (steel girder, prestressed concrete, timber, truss).</span>

- <span class="mark">A systematic approach (e.g., every 5th bridge on the state's inventory list) may be used to select candidates from each type.</span>
"""

# ── Cell 27: Stage 4 (markdown) ──────────────────────────────
CELL_REPLACEMENTS[27] = """**<span class="mark">Stage 4: Random Selection of Individual Bridges (Simple Random Sampling)</span>**

- <span class="mark">Within the selected bridge types, individual bridges are randomly chosen for detailed load rating and inspection.</span>

- <span class="mark">Inspectors may use techniques like random number generators applied to the bridge ID list to avoid selection bias.</span>
"""

# ── Cell 28: Why Multistage? (markdown) ──────────────────────
CELL_REPLACEMENTS[28] = """**<span class="mark">Why Use Multistage Sampling?</span>**

<span class="mark">✅ Cost Efficiency: Instead of inspecting every bridge in the country, breaking the population into stages reduces the number of field crews needed.</span>

<span class="mark">✅ Improved Representation: It ensures different climate zones, structural types (steel/concrete/timber), and settings (urban/rural) are included.</span>

<span class="mark">✅ Practicality: It would be impossible to perform detailed load tests on all 600,000+ U.S. bridges, but multistage sampling allows for a manageable and logistically feasible way to obtain a representative assessment of the nation's infrastructure.</span>

**<span class="mark"><u>"[Practice? We talkin' 'bout practice?](https://youtu.be/eGDBR2L5kzI)"</u></span>**

<span class="mark">Now is a good time to try a little practice. Make a copy of the document, [<u>Sample Surveys Practice</u>](https://docs.google.com/document/d/1SSrgcw_cI5Ggoweb1b0kBKy4TrStGqmTsP2d3N_Q8N4/edit?usp=sharing), and save it to your Drive. We will complete the first problem together.</span>
"""


def main():
    # ── Load ──
    with open(INPUT_NB, "r", encoding="utf-8") as f:
        nb = json.load(f)

    nb_em = copy.deepcopy(nb)

    # ── Apply replacements ──
    for idx, new_source in CELL_REPLACEMENTS.items():
        if idx < len(nb_em["cells"]):
            cell = nb_em["cells"][idx]
            if isinstance(cell.get("source"), list):
                cell["source"] = new_source.split("\n")
                # Re-add newlines to each line except the last
                cell["source"] = [line + "\n" for line in cell["source"][:-1]] + [cell["source"][-1]]
            else:
                cell["source"] = new_source
        else:
            print(f"WARNING: Cell index {idx} is out of range (notebook has {len(nb_em['cells'])} cells)")

    # ── Save ──
    with open(OUTPUT_NB, "w", encoding="utf-8") as f:
        json.dump(nb_em, f, indent=1)
    print(f"✅ Created {OUTPUT_NB}")

    # ── Self-Critic ──
    print("\n" + "=" * 60)
    print("SELF-CRITIC: Checking output quality...")
    print("=" * 60)

    with open(OUTPUT_NB, "r", encoding="utf-8") as f:
        full_text = f.read()

    # 1. Coherence Critic: check for leftover general-context words
    print("\n--- Coherence Critic: Leftover General Terms ---")
    bad_words = [
        "basketball", "voter", "teenager", "pizza", "cereal",
        "athlete", "playing basketball", "Landon", "Roosevelt",
        "Kaiser", "Generation M", "batting order", "free throw",
        "Pepperoni", "ice cream", "DVD"
    ]
    all_pass = True
    for w in bad_words:
        if w.lower() in full_text.lower():
            print(f"  ❌ FAIL: Found \"{w}\"")
            all_pass = False
        else:
            print(f"  ✅ PASS: No \"{w}\"")
    if all_pass:
        print("  🎉 All clear — no leftover general terms found!")

    # 2. Nonsense Critic: print first 150 chars of each rewritten cell
    print("\n--- Nonsense Critic: First 150 chars of each rewritten cell ---")
    nb_check = json.load(open(OUTPUT_NB, "r", encoding="utf-8"))
    for idx in sorted(CELL_REPLACEMENTS.keys()):
        cell = nb_check["cells"][idx]
        src = cell.get("source", "")
        if isinstance(src, list):
            src = "".join(src)
        # Strip HTML tags for readability
        clean = re.sub(r"<[^>]+>", "", src)
        clean = re.sub(r"\s+", " ", clean).strip()
        preview = clean[:150]
        print(f"  Cell {idx}: {preview}...")

    # 3. Math Preservation Critic: check code cells
    print("\n--- Math Preservation Critic: Code cell integrity ---")
    for idx in sorted(CELL_REPLACEMENTS.keys()):
        cell = nb_check["cells"][idx]
        if cell.get("cell_type") == "code":
            src = cell.get("source", "")
            if isinstance(src, list):
                src = "".join(src)
            np_count = src.count("np.")
            plt_count = src.count("plt.")
            widget_count = src.count("widgets.")
            print(f"  Cell {idx} (code): np.={np_count}, plt.={plt_count}, widgets.={widget_count}")

    # 4. Contextual Consistency Critic
    print("\n--- Contextual Consistency Critic ---")
    # Check that engineering terms are used consistently
    em_terms = ["compressive strength", "psi", "concrete", "bridge", "inspection"]
    for term in em_terms:
        count = full_text.lower().count(term)
        if count > 0:
            print(f"  ✅ \"{term}\" appears {count} time(s)")
        else:
            print(f"  ⚠️  \"{term}\" not found — may need to add engineering context")

    print("\n" + "=" * 60)
    print("CRITIC COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
