#!/usr/bin/env python3
"""Semantic rewriting of Chapter_10.ipynb → Chapter_10_EM.ipynb"""
import json, copy, re

INPUT_NB = "Chapter_10.ipynb"
OUTPUT_NB = "Chapter_10_EM.ipynb"
CELL_REPLACEMENTS = {}

# ── Cell 2: Retrospective or Prospective examples ─────────────
CELL_REPLACEMENTS[2] = """**<span class="mark">Retrospective or Prospective?</span>**

- <span class="mark">A structural engineering firm wants to study the impact of concrete curing temperature on 28-day compressive strength. They prepare 200 cylinders at varying temperatures and test them over the next 6 months.</span>

- <span class="mark">A research team investigates how weld preheat temperature affects fatigue life in steel connections. They track a set of welded beams over a year of cyclic loading, recording preheat conditions and crack initiation at regular intervals.</span>

- <span class="mark">A group of forensic engineers wanted to study the effects of chloride exposure on reinforcement corrosion. They gathered inspection records of 500 bridges that had already shown spalling and delamination and examined their exposure histories to determine if there was a pattern.</span>

- <span class="mark">A team of materials scientists studies the potential connection between aggregate alkalinity and alkali-silica reaction (ASR) in concrete. They identify a group of structures diagnosed with ASR cracking and review their mix designs to see if reactive aggregates were used.</span>

- <span class="mark">Researchers are interested in the long-term durability of fiber-reinforced polymer (FRP) wraps on bridge columns. They retrofit 1,000 columns that do not currently show distress and track environmental exposure and structural performance over the next 10 years.</span>

- <span class="mark">A structural forensics team examines the effect of construction sequence on residual stresses. They review past project records and survey experienced engineers about observed distortions in welded members.</span>

- <span class="mark">An infrastructure researcher studies the impact of cathodic protection on reducing reinforcement corrosion rates. They identify bridge decks scheduled for cathodic protection installation and measure corrosion potential changes over the next decade.</span>
"""

# ── Cell 4: Lurking variables examples ─────────────────────────
CELL_REPLACEMENTS[4] = """**<span class="mark">What could be the lurking variable?</span>**

<span class="mark">Study 1: Researchers find that bridges with more expansion joints have higher rates of deck deterioration.</span>

<span class="mark">Study 2: Structures that receive more frequent inspections tend to receive lower condition ratings.</span>

<span class="mark">Study 3: Construction projects that use more advanced surveying equipment tend to have fewer alignment errors.</span>

<span class="mark">Study 4: Cities with more high-rise buildings have higher rates of foundation settlement.</span>

<span class="mark">Study 5**:** Fabrication shops with more overhead cranes tend to produce heavier steel assemblies.</span>
"""

# ── Cell 19: Randomized Block Design examples ─────────────────
CELL_REPLACEMENTS[19] = """**<span class="mark">Examples of Randomized Block Design:</span>**

<u>Experimental Design 1: Testing the Effects of Steel Alloys on Weld Fatigue Life</u>

Experiment: Researchers want to test the effects of three different steel alloys (A36, A572, and A992) on weld fatigue life in structural connections. They divide the test specimens into blocks based on joint configuration (single-V groove, double-V groove, and fillet weld). Within each block, they randomly assign specimens to each alloy treatment. This randomization process ensures that each type of joint configuration is represented in each treatment group, reducing the potential confounding effects of joint geometry on fatigue life.

<u>Experimental Design 2: Testing the Efficacy of Corrosion Protection Methods</u>

Experiment: Researchers want to evaluate the efficacy of three corrosion protection methods (galvanization, epoxy coating, and cathodic protection) for steel reinforcement in concrete. They group test specimens into blocks defined by exposure environment (marine splash zone, industrial atmosphere, and rural atmosphere). Within each block, specimens are randomly assigned to each protection method. This randomization process ensures that each exposure environment is represented in each treatment group, reducing the potential confounding effects of environment on corrosion outcomes.

<u>Experimental Design 3: Assessing the Effects of Different Connection Types on Structural Performance</u>

Experiment: A structural engineering firm wants to determine the impact of three different connection types (bolted, welded, and riveted) on the moment capacity of beam-column joints. They group test specimens by steel section size (W8, W12, and W16). Within each section size block, specimens are randomly assigned to each connection type. This randomization process ensures that each section size is represented in each connection type group, controlling for potential differences in section properties on moment capacity.
"""

# ── Cell 21: Confounding factor examples ──────────────────────
CELL_REPLACEMENTS[21] = """**<span class="mark">What could be the confounding factor?</span>**

<span class="mark">Experiment 1: A study tests a new concrete admixture by applying it to half of a batch plant's pours and comparing the 28-day compressive strength with the other half, which does not receive the admixture. The treated pours are placed during cooler morning hours, while the untreated pours are placed in the afternoon heat.</span>

<span class="mark">Experiment 2**:** A firm implements a new welding procedure on one fabrication line and compares defect rates to a line that uses the traditional procedure. The new procedure is introduced on the line staffed by the most experienced welders.</span>

<span class="mark">Experiment 3: A lab tests a new accelerated curing method by assigning concrete cylinders to the method based on the batch they came from. Cylinders from higher-slump batches are placed in the accelerated curing chamber.</span>

<span class="mark">Experiment 4: Researchers compare the fatigue life of two steel alloys. Specimens from one alloy are also stress-relieved by heat treatment before testing, while specimens from the other alloy are not.</span>

<span class="mark">Experiment 5: A DOT compares the effectiveness of two bridge deck sealants by applying them to bridges that volunteered for the program versus bridges that did not.</span>
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

    # Self-Critic
    with open(OUTPUT_NB, "r") as f:
        text = f.read()
    clean = re.sub(r'data:image/[^"]+', '', text)
    bad = ["fertilizer", "crop yield", "farmer", "ice cream shop", "drowning",
           "tutoring", "coffee shop", "crime rate", "convertible", "rainfall",
           "sleep quality", "screen time", "study habits", "test scores",
           "smoking", "lung cancer", "pesticide", "Parkinson", "sugary beverages",
           "diabetes", "fitness program", "gym", "diet plan", "weight loss",
           "work-from-home"]
    print("\n--- Coherence Critic ---")
    fails = 0
    for w in bad:
        if w.lower() in clean.lower():
            print(f"  ❌ FAIL: Found \"{w}\"")
            fails += 1
    if fails == 0:
        print("  🎉 All clear!")
    
    print("\n--- Nonsense Critic ---")
    nb_check = json.load(open(OUTPUT_NB, "r"))
    for idx in sorted(CELL_REPLACEMENTS.keys()):
        cell = nb_check["cells"][idx]
        src = "".join(cell.get("source", "")) if isinstance(cell.get("source"), list) else cell.get("source", "")
        preview = re.sub(r'<[^>]+>', '', src)
        preview = re.sub(r'\s+', ' ', preview).strip()[:200]
        print(f"  Cell {idx}: {preview}...")

if __name__ == "__main__":
    main()
