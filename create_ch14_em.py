#!/usr/bin/env python3
"""Semantic rewriting of Chapter_14.ipynb → Chapter_14_EM.ipynb"""
import json, copy, re

INPUT_NB = "Chapter_14.ipynb"
OUTPUT_NB = "Chapter_14_EM.ipynb"
CELL_REPLACEMENTS = {}

# ── Cell 3: College student survey → Structural inspection survey ──
CELL_REPLACEMENTS[3] = """**<span class="mark">General Addition Rule:</span>** For any two events A and B, <span class="mark">$P(A \\cup B) = P(A) + P(B) - P(A \\cap B)$</span>.

<span class="mark">Example: A structural inspection of a bridge inventory found that 56% of bridges show signs of deck deterioration, 62% show substructure corrosion, and 42% show both.</span>

<span class="mark">1. What's the probability that a randomly selected bridge has either deck deterioration or substructure corrosion?</span>

<span class="mark">2. What's the probability that a bridge has neither condition?</span>
"""

# ── Cell 5: Independence example — student survey → inspection ──
CELL_REPLACEMENTS[5] = """**<span class="mark">Independence:</span>**

<span class="mark">Recall: **Independence** of two events means that the outcome of one event does not influence the probability of the other.</span>

<span class="mark">Formal Definition: Events A and B are **independent** whenever **P(B|A) = P(B)**.</span>

<span class="mark">(Equivalently, events A and B are independent whenever P(A|B) = P(A).)</span>

<span class="mark">Example: A structural engineering firm inspects bridge bearings and expansion joints. Are the events "bearing deterioration" and "joint failure" independent?</span>

<span class="mark">If 18% of bridges have bearing deterioration, and 12% of all bridges have joint failure, those events are independent **only if** the rate of joint failure among bridges with bearing deterioration is also 12%.</span>
"""

# ── Cell 6: Man/pregnant → Steel beam/fatigue crack ───────────
CELL_REPLACEMENTS[6] = """**<span class="mark">Independent</span>** $\\neq$ **<span class="mark">Disjoint:</span>**

<span class="mark">Suppose you select a structural member at random from a building's steel frame. Consider these two events:</span>

- <span class="mark">A = the member you select is a **column**.</span>
- <span class="mark">B = the member you select has a **fatigue crack**.</span>

- <span class="mark">Two events could be either independent or disjoint, but not both.</span>
- <span class="mark">And they could be neither one.</span>

<span class="mark">Disjoint events are NOT independent. Think about it: if you know A happened and A and B are disjoint, then the probability of B is now zero — the knowledge changes P(B).</span>

<span class="mark">Example: A = "the member is a column" and B = "the member is a beam" are disjoint (a member can't be both). But if A = "the member is a column" and B = "the member has a fatigue crack," these could be independent (columns and beams may have similar fatigue rates) but are NOT disjoint (a column can have a fatigue crack).</span>
"""

# ── Cell 7: DWI breath/blood test → NDT ultrasonic/radiographic ──
CELL_REPLACEMENTS[7] = """**<span class="mark">Tables vs Venn Diagrams:</span>**

<span class="mark">Weld quality inspection: 78% of suspect welds get an ultrasonic test, 36% a radiographic test, and 22% both.</span>

<span class="mark">Let's use what we know to start a table:</span>

<span class="mark">1\. Are giving a suspect weld an ultrasonic test and a radiographic test mutually exclusive?</span>

<span class="mark">2\. Are giving the two tests independent?</span>
"""

# ── Cell 12: Battery factory → Bolt factory ───────────────────
CELL_REPLACEMENTS[12] = """**<span class="mark">OR</span>** <span class="mark">Example: A bolt manufacturer produces two types of fasteners, standard A325 bolts and high-strength A490 bolts. Quality inspection tests show that 2% of the A325 bolts come off the manufacturing line with a defect, while only 1% of the A490 bolts have a defect. A490 bolts make up 25% of the company's production.</span>

<span class="mark">A randomly selected bolt is found to be defective. What is the probability that it is an A490 bolt?</span>
"""

# ── Cell 13: Skittles → Fastener bin ──────────────────────────
CELL_REPLACEMENTS[13] = """**<span class="mark">Drawing Without Replacement:</span>**

<span class="mark">You just opened a bin of assorted structural fasteners. Not that you could know this, but inside are 20 fasteners: 7 hex bolts, 5 carriage bolts, 4 lag screws, 3 machine screws, and only 1 eye bolt. You reach in and begin pulling out fasteners one at a time without looking.</span>

<span class="mark">What's the probability that the first fastener is a hex bolt and the second is a machine screw?</span>

<span class="mark">P(hex 1st) = 7/20</span>

<span class="mark">P(machine 2nd | hex 1st) = 3/19 (without replacement)</span>

<span class="mark">P(hex 1st AND machine 2nd) = 7/20 × 3/19 = 21/380 ≈ 0.055</span>
"""

# ── Cell 14: Disease testing → NDT flaw detection ─────────────
CELL_REPLACEMENTS[14] = """### Interactive Experiment: Conditional Probability Tree

Conditional probability can be counter-intuitive.

**Scenario:** A non-destructive testing (NDT) scan detects a flaw in a critical weld. The equipment is 95% accurate. Does the weld actually have a flaw?

Maybe not! If flaws are rare enough, the **False Positives** (good welds flagged as defective) can vastly outnumber the **True Positives** (actually flawed welds correctly detected).

**Explore:**
*   Adjust the **True Flaw Rate** (how common flaws actually are in production).
*   Adjust the **Test Accuracy** (Detection Rate and False Positive Rate).
*   Watch how the probability tree reveals the *actual* chance the weld is flawed, given a positive test result.
"""

# ── Cell 15: Disease testing code → NDT flaw detection code ───
CELL_REPLACEMENTS[15] = '''# @title Click 'Play' to Run Code

import ipywidgets as widgets
import matplotlib.pyplot as plt
from IPython.display import display

def plot_tree_diagram(p_flaw, p_detect_given_flaw, p_detect_given_good):
    # Complement probabilities
    p_good = 1 - p_flaw
    p_miss_given_flaw = 1 - p_detect_given_flaw
    p_clear_given_good = 1 - p_detect_given_good
    
    # Path Probabilities
    p_f_det = p_flaw * p_detect_given_flaw
    p_f_miss = p_flaw * p_miss_given_flaw
    p_g_det = p_good * p_detect_given_good
    p_g_clear = p_good * p_clear_given_good
    
    # Total Detections
    p_detected = p_f_det + p_g_det
    
    # Bayes Theorem: P(Flaw | Detected)
    p_flaw_given_detect = p_f_det / p_detected if p_detected > 0 else 0
    
    # Visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    
    root = (1, 5)
    f_node = (4, 7)
    g_node = (4, 3)
    fd_node = (7, 8)
    fm_node = (7, 6)
    gd_node = (7, 4)
    gc_node = (7, 2)
    
    ax.plot([root[0], f_node[0]], [root[1], f_node[1]], 'k-', lw=1)
    ax.plot([root[0], g_node[0]], [root[1], g_node[1]], 'k-', lw=1)
    ax.plot([f_node[0], fd_node[0]], [f_node[1], fd_node[1]], 'k-', lw=1)
    ax.plot([f_node[0], fm_node[0]], [f_node[1], fm_node[1]], 'k-', lw=1)
    ax.plot([g_node[0], gd_node[0]], [g_node[1], gd_node[1]], 'k-', lw=1)
    ax.plot([g_node[0], gc_node[0]], [g_node[1], gc_node[1]], 'k-', lw=1)
    
    ax.plot(*root, 'ko')
    
    ax.text(2.5, 6.2, f"Flawed\\n{p_flaw:.2%}", ha='right')
    ax.text(2.5, 3.8, f"Good\\n{p_good:.2%}", ha='right')
    
    ax.text(5.5, 7.8, f"Detected\\n{p_detect_given_flaw:.2%}", ha='right', color='green')
    ax.text(5.5, 6.2, f"Missed\\n{p_miss_given_flaw:.2%}", ha='right', color='red')
    ax.text(5.5, 3.8, f"False Alarm\\n{p_detect_given_good:.2%}", ha='right', color='green')
    ax.text(5.5, 2.2, f"Cleared\\n{p_clear_given_good:.2%}", ha='right', color='red')
    
    ax.text(7.2, 8, f"True Detection\\nP={p_f_det:.4f}", va='center')
    ax.text(7.2, 6, f"Missed Flaw\\nP={p_f_miss:.4f}", va='center')
    ax.text(7.2, 4, f"False Alarm\\nP={p_g_det:.4f}", va='center')
    ax.text(7.2, 2, f"True Clear\\nP={p_g_clear:.4f}", va='center')
    
    plt.title(f"Conditional Probability Tree Diagram\\nP(Flaw | Detection) = {p_flaw_given_detect:.2%}", fontsize=14)
    plt.show()

style = {'description_width': 'initial'}
p_flaw = widgets.FloatLogSlider(value=0.01, base=10, min=-4, max=-1, step=0.1, description='Flaw Rate P(F):', style=style)
p_sens = widgets.FloatSlider(value=0.95, min=0.5, max=1.0, step=0.01, description='Detection Rate P(D|F):', style=style)
p_false_alarm = widgets.FloatSlider(value=0.05, min=0.0, max=0.2, step=0.01, description='False Alarm P(D|G):', style=style)

ui = widgets.VBox([p_flaw, p_sens, p_false_alarm])
out = widgets.interactive_output(plot_tree_diagram, 
                                 {'p_flaw': p_flaw, 
                                  'p_detect_given_flaw': p_sens, 
                                  'p_detect_given_good': p_false_alarm})

display(ui, out)
'''

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
    bad = ["college student", "campus residence", "meal program", "pregnant",
           "Skittles", "candy", "disease", "DWI", "DUI", "breath test",
           "drunk driving", "battery", "rechargeable"]
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
