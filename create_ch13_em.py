#!/usr/bin/env python3
"""Semantic rewriting of Chapter_13.ipynb → Chapter_13_EM.ipynb
Chapter 13 is mostly context-neutral (dice, formal probability notation).
Only the traffic light example needs conversion."""
import json, copy, re

INPUT_NB = "Chapter_13.ipynb"
OUTPUT_NB = "Chapter_13_EM.ipynb"
CELL_REPLACEMENTS = {}

# ── Cell 9: Traffic light → Structural monitoring alarm ───────
CELL_REPLACEMENTS[9] = """**<span class="mark">Examples:</span>**

<span class="mark">We opened the last chapter by looking at the structural monitoring sensor on a bridge pier, observing that when we check the sensor reading, the indicator is green (safe) about 35% of the time.</span>

<span class="mark">If P(green/safe) = 0.35, what's the probability the indicator is NOT green?</span>

<span class="mark">P(not green) = 1 − P(green) = 1 − 0.35 = 0.65</span>

<span class="mark">If P(green/safe) = 0.35 and P(yellow/caution) = 0.04, what is P(red/alert)?</span>

<span class="mark">P(green) + P(yellow) + P(red) = 1, so P(red) = 1 − 0.35 − 0.04 = 0.61.</span>

- <span class="mark">A correctly designed reinforced concrete beam has a much better than 50-50 chance of safely carrying its design load.</span>
"""

# ── Cell 10: Traffic light model intro ────────────────────────
CELL_REPLACEMENTS[10] = """### Interactive Experiment: The Structural Monitoring Model

Probability describes the long-run frequency of an event. A legitimate probability model must satisfy two rules:
1. Any probability is a number between 0 and 1.
2. The sum of logical outcomes must equal 1.

**Scenario:** A structural health monitoring sensor on a bridge pier has three states:
*   🟢 **Safe** (P = ?)
*   🟡 **Caution** (P = ?)
*   🔴 **Alert** (P = 1 − P(safe) − P(caution))

Use the sliders below to set P(Safe) and P(Caution) and observe the resulting P(Alert) and how it behaves over many sensor readings.
"""

# ── Cell 11: Traffic simulation code ──────────────────────────
CELL_REPLACEMENTS[11] = """# @title Click 'Play' to Run Code
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display, clear_output

def run_sensor_simulation(p_safe, p_caution, n_readings):
    # Calculate P(Alert) ensuring sum = 1
    p_alert = round(1.0 - p_safe - p_caution, 2)
    
    if p_alert < 0:
        print("Error: P(Safe) + P(Caution) cannot exceed 1.0!")
        return
    
    # Simulate sensor readings
    outcomes = np.random.choice(['Safe', 'Caution', 'Alert'], size=n_readings, p=[p_safe, p_caution, p_alert])
    
    counts = {'Safe': 0, 'Caution': 0, 'Alert': 0}
    for o in outcomes:
        counts[o] += 1
    
    # Calculate observed frequencies
    freqs = {k: v/n_readings for k, v in counts.items()}
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left: Theoretical vs Observed
    categories = ['Safe', 'Caution', 'Alert']
    theoretical = [p_safe, p_caution, p_alert]
    observed = [freqs[c] for c in categories]
    colors = ['#4CAF50', '#FFC107', '#F44336']
    
    x = np.arange(len(categories))
    width = 0.35
    axes[0].bar(x - width/2, theoretical, width, label='Theoretical', color=colors, alpha=0.5, edgecolor='black')
    axes[0].bar(x + width/2, observed, width, label=f'Observed (n={n_readings})', color=colors, edgecolor='black')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels([f'🟢 {categories[0]}', f'🟡 {categories[1]}', f'🔴 {categories[2]}'])
    axes[0].set_ylabel('Probability / Frequency')
    axes[0].set_title('Theoretical vs. Observed Sensor Readings')
    axes[0].legend()
    axes[0].set_ylim(0, 1)
    
    # Right: Cumulative frequency convergence
    cumulative = np.cumsum([1 if o == 'Safe' else 0 for o in outcomes]) / np.arange(1, n_readings+1)
    axes[1].plot(cumulative, color='green', alpha=0.7)
    axes[1].axhline(p_safe, color='black', linestyle='--', label=f'True P(Safe) = {p_safe}')
    axes[1].set_xlabel('Number of Sensor Readings')
    axes[1].set_ylabel('Cumulative Proportion of Safe Readings')
    axes[1].set_title('Law of Large Numbers: Convergence to True Probability')
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print(f"Theoretical: P(Safe)={p_safe}, P(Caution)={p_caution}, P(Alert)={p_alert}")
    print(f"Observed:    P(Safe)={freqs['Safe']:.3f}, P(Caution)={freqs['Caution']:.3f}, P(Alert)={freqs['Alert']:.3f}")

style = {'description_width': 'initial'}
display(widgets.interactive(run_sensor_simulation,
    p_safe=widgets.FloatSlider(value=0.35, min=0.0, max=1.0, step=0.01, description='P(Safe):', style=style),
    p_caution=widgets.FloatSlider(value=0.04, min=0.0, max=0.5, step=0.01, description='P(Caution):', style=style),
    n_readings=widgets.IntSlider(value=100, min=10, max=5000, step=10, description='# Readings:', style=style)))
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
    bad = ["traffic light", "College and Main", "intersection"]
    print("\n--- Coherence Critic ---")
    fails = 0
    for w in bad:
        if w.lower() in clean.lower():
            print(f"  ❌ FAIL: Found \"{w}\"")
            fails += 1
    if fails == 0:
        print("  🎉 All clear!")

if __name__ == "__main__":
    main()
