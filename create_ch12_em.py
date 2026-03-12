#!/usr/bin/env python3
"""Semantic rewriting of Chapter_12.ipynb → Chapter_12_EM.ipynb"""
import json, copy, re

INPUT_NB = "Chapter_12.ipynb"
OUTPUT_NB = "Chapter_12_EM.ipynb"
CELL_REPLACEMENTS = {}

# ── Cell 7: Café lunch → Engineering firm design options (OR rule) ──
CELL_REPLACEMENTS[7] = """**<span class="mark">How to Count</span>**

<span class="mark">Fundamental Counting Principle (Part 1: OR)</span>

- <span class="mark">If event A has m outcomes and event B has n *different* outcomes, then the number of outcomes in event A or B is m + n.</span>

> <span class="mark">Example: An engineering firm is selecting a structural connection for a joint. They can choose from 4 **bolted connection designs** or 5 **welded connection designs**. How many total connection options are available?</span>
>
> <span class="mark">$4+5 = 9$ possible connection designs.</span>

<span class="mark">Fundamental Counting Principle (Part 2: AND)</span>

- <span class="mark">If event A has m outcomes and event B has n outcomes, then event A and B together have m × n outcomes.</span>

> <span class="mark">Example: The firm must also select both a connection design AND a corrosion protection method. If there are 9 connection options and 3 corrosion protection methods, how many total design configurations are possible?</span>
>
> <span class="mark">$9 \\times 3 = 27$ total configurations.</span>
"""

# ── Cell 8: Lunch Special OR widget ───────────────────────────
CELL_REPLACEMENTS[8] = """# @title 🔩 Connection Design: Addition Rule (OR)
import ipywidgets as widgets
from IPython.display import display, HTML

def update_or_rule(bolted, welded):
    total = bolted + welded
    display(HTML(f\"\"\"
    <div style='background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; padding: 20px; border-radius: 15px; font-family: sans-serif;'>
    <h3>Rule of Addition (OR)</h3>
    <p>If you choose 1 design from Set A ({bolted} bolted options) <b>OR</b> 1 design from Set B ({welded} welded options):</p>
    <h2 style='color: #4FC3F7;'>{bolted} + {welded} = {total} total options</h2>
    </div>
    \"\"\"))

style = {'description_width': '150px'}
display(widgets.interactive(update_or_rule, 
    bolted=widgets.IntSlider(value=4, min=1, max=10, description='Bolted Designs:', style=style),
    welded=widgets.IntSlider(value=5, min=1, max=10, description='Welded Designs:', style=style)))
"""

# ── Cell 9: Hungry Special AND widget ─────────────────────────
CELL_REPLACEMENTS[9] = """# @title 🏗️ Full Design Configuration & Access Codes: Multiplication Rule (AND)
import ipywidgets as widgets
from IPython.display import display, HTML

def update_and_rule(connections, protections):
    total = connections * protections
    display(HTML(f\"\"\"
    <div style='background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; padding: 20px; border-radius: 15px; font-family: sans-serif;'>
    <h3>Rule of Multiplication (AND)</h3>
    <p>If you choose 1 connection design from {connections} options <b>AND</b> 1 protection method from {protections} options:</p>
    <h2 style='color: #4FC3F7;'>{connections} × {protections} = {total} total configurations</h2>
    </div>
    \"\"\"))

style = {'description_width': '150px'}
display(widgets.interactive(update_and_rule, 
    connections=widgets.IntSlider(value=9, min=1, max=20, description='Connection Types:', style=style),
    protections=widgets.IntSlider(value=3, min=1, max=10, description='Protection Methods:', style=style)))
"""

# ── Cell 12: Triple scoop ice cream → Structural inspection combo ──
CELL_REPLACEMENTS[12] = """**<span class="mark">Combinations</span>** are the number of different ways you can arrange a group of objects, BUT you don't care about what order the things are in.

> <span class="mark">Equation:${}_{n}{C_{r} = \\frac{n!}{r!(n - r)!}}_{}$, select any *r* items from a group of *n* different items.</span>
>
> <span class="mark">Example: A structural inspection team must select 3 bridge types to prioritize from 12 available types for this quarter's review. How many different selections are possible?</span>
>
> <span class="mark">There are ${}_{12}{C_{3} = \\frac{12!}{3!(12-3)!} = \\frac{12!}{3! \\cdot 9!} = 220}$ possible selections.</span>
"""

# ── Cell 13: Pizza shop scenario ──────────────────────────────
CELL_REPLACEMENTS[13] = """### Interactive Experiments: Permutations vs. Combinations

Understanding the difference between **Order Matters** (Permutations) and **Order Doesn't Matter** (Combinations) is crucial.

**Scenario: The Structural Joint**

Imagine you are designing a structural connection.
*   **n (Total Items):** The number of fastener types available (e.g., A325 bolts, A490 bolts, rivets, welds, pins).
*   **r (Items to Choose):** The number of fastener types you want in your connection design.

**Key Question:**
*   Does the installation order matter? (Is installing "Bolts then Welds" different from "Welds then Bolts"?) → **Permutation**.
*   Does the order NOT matter? (Is a "Bolt & Weld" connection the same as a "Weld & Bolt" connection?) → **Combination**.
"""

# ── Cell 17: ATM password → Construction site access codes ────
CELL_REPLACEMENTS[17] = """<span class="mark">Example: Chances are you use an access code of some kind every day on a construction site, whether you're unlocking a crane control panel, accessing a restricted floor, or logging into a job site management system. One factor that helps make these codes secure is the large number of possibilities. In each of the situations below, how many codes are possible?</span>

<span class="mark">a. A 4-digit numeric crane access code (digits 0-9).</span>

<span class="mark">b. A 5-character site badge code that uses the format: Letter-Digit-Letter-Digit-Letter.</span>

<span class="mark">c. A 6-character equipment login with any combination of 26 letters and 10 digits.</span>
"""

# ── Cell 18: Password complexity widget ───────────────────────
CELL_REPLACEMENTS[18] = """# @title 🔐 Access Code Complexity Explorer
import ipywidgets as widgets
from IPython.display import display, HTML

def calc_codes(scenario):
    if scenario == '4-Digit Crane Code':
        total = 10**4
        desc = "10 × 10 × 10 × 10"
    elif scenario == 'L-D-L-D-L (5 chars)':
        total = 26 * 10 * 26 * 10 * 26
        desc = "26³ × 10²"
    elif scenario == '6-char Alphanumeric':
        total = 36**6
        desc = "36⁶ (26 letters + 10 digits)"
    else:
        total = 0
        desc = ""

    display(HTML(f\"\"\"
    <div style='background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); color: white; padding: 20px; border-radius: 15px; font-family: sans-serif;'>
    <h3>🔐 Scenario: {scenario}</h3>
    <p>Calculation: {desc}</p>
    <h2 style='color: #4FC3F7;'>Total possible codes: {total:,}</h2>
    <p style='color: #81C784;'>The more possibilities, the harder to crack.</p>
    </div>
    \"\"\"))

display(widgets.interactive(calc_codes, scenario=widgets.Dropdown(
    options=['4-Digit Crane Code', 'L-D-L-D-L (5 chars)', '6-char Alphanumeric'],
    description='Scenario:', style={'description_width': '100px'})))
"""

# ── Cell 19: Lotto → ASTM batch sampling ─────────────────────
CELL_REPLACEMENTS[19] = """<span class="mark">Example: An ASTM testing procedure requires selecting 6 steel specimens at random from a production lot of 49 samples. A batch passes if your 6 selected specimens all meet the yield strength specification. How many different selections of 6 from 49 are possible?</span>
"""

# ── Cell 20: Lotto widget ────────────────────────────────────
CELL_REPLACEMENTS[20] = """# @title 🔬 Specimen Selection Calculator
import ipywidgets as widgets
import math
from IPython.display import display, HTML

def update_specimen(n, r):
    combos = math.comb(n, r)
    display(HTML(f'''
    <div style='background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; padding: 20px; border-radius: 15px; font-family: sans-serif;'>
    <h3>Selecting {r} specimens from {n}</h3>
    <h2 style='color: #4FC3F7;'>There are {combos:,} unique ways to fill out a selection.</h2>
    <p>Probability of selecting 1 specific set: <b>{1/combos:.10f}</b></p>
    </div>
    '''))

style = {'description_width': '120px'}
display(widgets.interactive(update_specimen,
    n=widgets.IntSlider(value=49, min=5, max=60, description='Lot Size (n):', style=style),
    r=widgets.IntSlider(value=6, min=1, max=10, description='Specimens (r):', style=style)))
"""

# ── Cell 21: County legislature committee → Engineering review panel ──
CELL_REPLACEMENTS[21] = """<span class="mark">Example: A professional engineering organization consists of 13 licensed engineers, 8 structural engineers and 5 geotechnical engineers. They're forming a 4-person review panel to evaluate a proposed foundation design. How many different panels could be formed if the group will consist of:</span>

<span class="mark">a) 4 geotechnical engineers?</span>

<span class="mark">b) 4 structural engineers?</span>

<span class="mark">c) 2 structural and 2 geotechnical engineers?</span>
"""

# ── Cell 22: Committee widget ─────────────────────────────────
CELL_REPLACEMENTS[22] = """# @title 🏛️ Review Panel Combination Builder
import ipywidgets as widgets
import math
from IPython.display import display, HTML

def build_panel(struct_pick, geotech_pick):
    # Total available: 8 Structural, 5 Geotechnical
    if struct_pick > 8 or geotech_pick > 5:
        print("Not enough engineers available!")
        return
    s_ways = math.comb(8, struct_pick)
    g_ways = math.comb(5, geotech_pick)
    total = s_ways * g_ways
    display(HTML(f'''
    <div style='background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; padding: 20px; border-radius: 15px; font-family: sans-serif;'>
    <h3>Review Panel Builder</h3>
    <p>Choosing {struct_pick} from 8 Structural Engineers: C(8,{struct_pick}) = {s_ways}</p>
    <p>Choosing {geotech_pick} from 5 Geotechnical Engineers: C(5,{geotech_pick}) = {g_ways}</p>
    <h2 style='color: #4FC3F7;'>Total panels: {s_ways} × {g_ways} = {total}</h2>
    </div>
    '''))

style = {'description_width': '180px'}
display(widgets.interactive(build_panel,
    struct_pick=widgets.IntSlider(value=2, min=0, max=8, description='Structural Engineers:', style=style),
    geotech_pick=widgets.IntSlider(value=2, min=0, max=5, description='Geotechnical Engineers:', style=style)))
"""

# ── Cell 23: Varsity lottery → Structures team lottery ────────
CELL_REPLACEMENTS[23] = """<span class="mark">Example: In the last chapter, we asked whether there was something suspicious about a lab assignment random draw. A total of 57 engineers, including 20 from the same project team, applied for just 3 highly desirable lab bench assignments. When all 3 winners turned out to be from that project team, the other engineers cried foul.</span>

<span class="mark">Use combinations to assess their claim. Is this just bad luck, or strong evidence of bias?</span>

<span class="mark">$P(\\text{all 3 from project team}) = \\frac{\\binom{20}{3}}{\\binom{57}{3}}$</span>
"""

# ── Cell 24: Varsity lottery widget ───────────────────────────
CELL_REPLACEMENTS[24] = """# @title 🔬 Lab Assignment Lottery: Probability Calculator
import ipywidgets as widgets
import math
from IPython.display import display, HTML

def calc_lottery(n_total, k_team, r_winners):
    if r_winners > n_total or k_team > n_total:
        return
    total_ways = math.comb(n_total, r_winners)
    # Success means picking r_winners all from the team
    if r_winners > k_team:
        success = 0
    else:
        success = math.comb(k_team, r_winners)
    prob = success / total_ways if total_ways > 0 else 0
    display(HTML(f'''
    <div style='background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; padding: 20px; border-radius: 15px; font-family: sans-serif;'>
    <h3>🔬 Lab Assignment Probability</h3>
    <p>Total ways to choose {r_winners} from {n_total}: C({n_total},{r_winners}) = {total_ways:,}</p>
    <p>Ways to choose {r_winners} from the project team of {k_team}: C({k_team},{r_winners}) = {success:,}</p>
    <h2 style='color: #4FC3F7;'>P(all {r_winners} from team) = {success}/{total_ways:,} = {prob:.6f} ({prob*100:.3f}%)</h2>
    </div>
    '''))

style = {'description_width': '180px'}
display(widgets.interactive(calc_lottery,
    n_total=widgets.IntSlider(value=57, min=10, max=100, description='Total Engineers:', style=style),
    k_team=widgets.IntSlider(value=20, min=1, max=50, description='Project Team Size:', style=style),
    r_winners=widgets.IntSlider(value=3, min=1, max=10, description='Winners Drawn:', style=style)))
"""

# ── Cell 25: DVD Grab Bag → Materials Testing Kit ─────────────
CELL_REPLACEMENTS[25] = """<span class="mark">Example: A Materials Testing Kit contains 6 specimens chosen at random from 15 recently delivered material samples, including 4 steel coupons, 8 concrete cylinders, and 3 timber prisms. Find the probability you get:</span>

<span class="mark">a) nothing but concrete cylinders.</span>

<span class="mark">b) 3 of the steel coupons and 3 of the concrete cylinders.</span>

<span class="mark">c) all 3 of the timber prisms and any 3 other specimens.</span>
"""

# ── Cell 26: DVD Grab Bag widget ──────────────────────────────
CELL_REPLACEMENTS[26] = """# @title 🧪 Materials Testing Kit Probability Explorer
import ipywidgets as widgets
import math
from IPython.display import display, HTML

def calc_kit(n_steel, n_concrete, n_timber, k_pick):
    total_in_kit = n_steel + n_concrete + n_timber
    if k_pick > total_in_kit:
        display(HTML("Error: You cannot pick more specimens than are in the kit."))
        return
    total_ways = math.comb(total_in_kit, k_pick)
    
    # Scenario A: All concrete
    if k_pick <= n_concrete:
        a_ways = math.comb(n_concrete, k_pick)
        a_prob = a_ways / total_ways
    else:
        a_ways = 0
        a_prob = 0
    
    # Scenario B: Half steel, half concrete (if k_pick is even)
    half = k_pick // 2
    if half <= n_steel and half <= n_concrete and k_pick % 2 == 0:
        b_ways = math.comb(n_steel, half) * math.comb(n_concrete, half)
        b_prob = b_ways / total_ways
    else:
        b_ways = "N/A"
        b_prob = 0
    
    # Scenario C: All timber + rest from others
    rest = k_pick - n_timber
    if rest >= 0 and n_timber <= k_pick:
        c_ways = math.comb(n_timber, n_timber) * math.comb(n_steel + n_concrete, rest)
        c_prob = c_ways / total_ways
    else:
        c_ways = 0
        c_prob = 0

    display(HTML(f'''
    <div style='background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; padding: 20px; border-radius: 15px; font-family: sans-serif;'>
    <h3>🧪 Materials Testing Kit: {k_pick} from {total_in_kit}</h3>
    <p>Total ways: C({total_in_kit},{k_pick}) = {total_ways:,}</p>
    <hr>
    <p><b>A)</b> All concrete: {a_ways:,} ways → P = {a_prob:.6f}</p>
    <p><b>B)</b> {half} steel + {half} concrete: {b_ways} ways → P = {b_prob:.6f}</p>
    <p><b>C)</b> All {n_timber} timber + {rest} others: {c_ways:,} ways → P = {c_prob:.6f}</p>
    </div>
    '''))

style = {'description_width': '150px'}
display(widgets.interactive(calc_kit,
    n_steel=widgets.IntSlider(value=4, min=0, max=10, description='Steel Coupons:', style=style),
    n_concrete=widgets.IntSlider(value=8, min=0, max=15, description='Concrete Cylinders:', style=style),
    n_timber=widgets.IntSlider(value=3, min=0, max=10, description='Timber Prisms:', style=style),
    k_pick=widgets.IntSlider(value=6, min=1, max=15, description='Specimens Picked:', style=style)))
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
    bad = ["pizza", "pepperoni", "mushroom", "topping", "ice cream", "scoop",
           "ATM", "password", "lotto", "lottery", "Pick-6", "bettor",
           "Democrat", "Republican", "legislature", "DVD", "comedy",
           "drama", "animated", "café", "lunch", "salad", "sandwich",
           "varsity", "dorm"]
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
