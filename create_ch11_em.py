#!/usr/bin/env python3
"""Semantic rewriting of Chapter_11.ipynb → Chapter_11_EM.ipynb"""
import json, copy, re

INPUT_NB = "Chapter_11.ipynb"
OUTPUT_NB = "Chapter_11_EM.ipynb"
CELL_REPLACEMENTS = {}

# ── Cell 12: Cereal box → Compliance Certificate collection ──
CELL_REPLACEMENTS[12] = """**<span class="mark">Compliance Certificate Example:</span>**

<span class="mark">Suppose a materials standards board includes compliance certificates in shipments of structural materials, hoping to encourage thorough documentation. The board announces that 20% of the shipments contain a certificate for **High-Strength Steel (HSS)**, 30% contain one for **Carbon Fiber Reinforced Polymer (CFRP)**, and the rest contain one for **Prestressed Concrete (PSC)**. You want to collect all three. How many shipments would you expect to need to receive?</span>
"""

# ── Cell 13: Simulation table — cereal → compliance certs ─────
CELL_REPLACEMENTS[13] = """**<span class="mark">Put it all together to run the simulation:</span>**

5. Run several trials.

Component Model (Key):
0, 1 = High-Strength Steel (HSS) (20%)
2, 3, 4 = Carbon Fiber (CFRP) (30%)
5, 6, 7, 8, 9 = Prestressed Concrete (PSC) (50%)

Goal: Collect all three certificates!

| Random Digits | Outcomes | Result (Success?) |
|---|---|---|
| 89064 | PSC, PSC, HSS, PSC, CFRP | Yes (5 shipments) |
| 2730 | CFRP, PSC, CFRP, HSS | Yes (4 shipments) — missing PSC, wait... |

"""

# ── Cell 14: Interactive cereal sim intro ─────────────────────
CELL_REPLACEMENTS[14] = """### Interactive Compliance Certificate Simulator

Now it's your turn! Instead of using a random number table, use this simulator to 'receive' shipments and see how long it takes to complete your certificate collection.
"""

# ── Cell 15: Cereal Box Simulator code ────────────────────────
CELL_REPLACEMENTS[15] = """# @title 📋 Compliance Certificate Simulator - Click 'Play' to Start
import ipywidgets as widgets
from IPython.display import display, clear_output
import numpy as np
import matplotlib.pyplot as plt

class CertificateSimulator:
    def __init__(self):
        # Configuration
        self.materials = ['High-Strength Steel (HSS)', 'Carbon Fiber (CFRP)', 'Prestressed Concrete (PSC)']
        self.probs = [0.2, 0.3, 0.5]
        self.colors = {'High-Strength Steel (HSS)': '#4A90D9', 'Carbon Fiber (CFRP)': '#2ECC71', 'Prestressed Concrete (PSC)': '#E74C3C'}
        
        # Simulation State
        self.collection = set()
        self.history = []
        self.total_shipments = 0
        self.trial_results = []
        
        # UI Elements
        self.out_display = widgets.Output()
        self.out_plot = widgets.Output()
        
        self.btn_receive = widgets.Button(description="📦 Receive Shipment", button_style='success',
                                      layout=widgets.Layout(width='200px', height='40px'))
        self.btn_reset = widgets.Button(description="🔄 Reset", button_style='warning',
                                    layout=widgets.Layout(width='100px', height='40px'))
        self.btn_sim = widgets.Button(description="⚡ Simulate 1000 Trials", button_style='info',
                                  layout=widgets.Layout(width='200px', height='40px'))
        
        self.btn_receive.on_click(self.receive_shipment)
        self.btn_reset.on_click(self.reset)
        self.btn_sim.on_click(self.run_bulk_sim)
        
        self.update_display()
        display(widgets.VBox([
            widgets.HTML("<h3>📋 Compliance Certificate Collector</h3>"),
            widgets.HTML("<b>Goal:</b> Collect certificates for all 3 structural materials: HSS (20%), CFRP (30%), PSC (50%)."),
            widgets.HBox([self.btn_receive, self.btn_reset, self.btn_sim]),
            self.out_display,
            self.out_plot
        ]))
    
    def receive_shipment(self, _):
        cert = np.random.choice(self.materials, p=self.probs)
        self.total_shipments += 1
        self.history.append(cert)
        self.collection.add(cert)
        self.update_display()
        if len(self.collection) == 3:
            self.trial_results.append(self.total_shipments)
            with self.out_display:
                print(f"\\n🎉 COMPLETE! You collected all 3 certificates in {self.total_shipments} shipments!")
    
    def reset(self, _):
        self.collection = set()
        self.history = []
        self.total_shipments = 0
        self.update_display()
    
    def update_display(self):
        self.out_display.clear_output(wait=True)
        with self.out_display:
            print(f"Shipments received: {self.total_shipments}")
            print(f"Collected: {', '.join(sorted(self.collection)) if self.collection else '(none yet)'}")
            missing = set(self.materials) - self.collection
            print(f"Still need: {', '.join(sorted(missing)) if missing else 'NOTHING — Complete!'}")
            if self.history:
                recent = self.history[-10:]
                print(f"Last shipments: {' → '.join(recent)}")
    
    def run_bulk_sim(self, _):
        results = []
        for _ in range(1000):
            collected = set()
            count = 0
            while len(collected) < 3:
                cert = np.random.choice(self.materials, p=self.probs)
                collected.add(cert)
                count += 1
            results.append(count)
        self.out_plot.clear_output(wait=True)
        with self.out_plot:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.hist(results, bins=range(3, max(results)+2), edgecolor='black', alpha=0.7, color='steelblue', align='left')
            ax.axvline(np.mean(results), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(results):.1f} shipments')
            ax.set_xlabel('Number of Shipments to Complete Collection')
            ax.set_ylabel('Frequency (out of 1000 trials)')
            ax.set_title('How Many Shipments to Collect All 3 Certificates?')
            ax.legend()
            ax.grid(alpha=0.3)
            plt.tight_layout()
            plt.show()

sim = CertificateSimulator()
"""

# ── Cell 16: Simulation explanation ───────────────────────────
CELL_REPLACEMENTS[16] = """**<span class="mark">Specify how to simulate trials:</span>**

3\. Explain how you will combine the components to model a trial.
> We pretend to receive shipments (repeat components) until our certificate collection is complete. We do this by looking at each random digit and indicating what certificate it represents. We continue until we've found all three.

4\. State clearly what the response variable is.
> The response variable is **the number of shipments required** to complete the collection.
"""

# ── Cell 17: Same as 13, results table ────────────────────────
CELL_REPLACEMENTS[17] = """**<span class="mark">Put it all together to run the simulation:</span>**

5. Run several trials.

Component Model (Key):
0, 1 = High-Strength Steel (HSS) (20%)
2, 3, 4 = Carbon Fiber (CFRP) (30%)
5, 6, 7, 8, 9 = Prestressed Concrete (PSC) (50%)

Goal: Collect all three certificates!

| Random Digits | Outcomes | Result (Success?) |
|---|---|---|
| 89064 | PSC, PSC, HSS, PSC, CFRP | Yes (5 shipments) |
| 27305 | CFRP, PSC, CFRP, HSS, PSC | Yes — all 3 by shipment 4 |

"""

# ── Cell 19: World Series → Structural Testing Series ─────────
CELL_REPLACEMENTS[19] = """🏗️ **Structural Testing Series Model (2-3-2 Format)**

Scenario: **Design A** (Lab 1) vs. **Design B** (Lab 2). Best of 7 load tests. First design to pass 4 tests wins the contract.

**Lab Advantage:** The design being tested in its home lab has a 55% chance of passing any given test (due to technician familiarity with the setup).

Digit Assignment (00-99):
00 - 54 = Home Lab Design Passes (55%)
55 - 99 = Away Lab Design Passes (45%)

| Schedule: | Game | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| **Location** | | Lab 1 | Lab 1 | Lab 2 | Lab 2 | Lab 2 | Lab 1 | Lab 1 |

"""

# ── Cell 20: World Series intro ───────────────────────────────
CELL_REPLACEMENTS[20] = """### 🏗️ Interactive Structural Testing Series Simulator

**Run the cell below** to load the simulator. You can run test-by-test or simulate the entire series 1000 times.
"""

# ── Cell 21: World Series Simulator code ──────────────────────
CELL_REPLACEMENTS[21] = """# @title 🏗️ Structural Testing Series Simulator - Click 'Play' to Start
import ipywidgets as widgets
from IPython.display import display, clear_output
import numpy as np
import matplotlib.pyplot as plt

class TestingSeriesSimulator:
    def __init__(self):
        # Config
        self.home_win_prob = 0.55
        self.schedule = ['Lab 1', 'Lab 1', 'Lab 2', 'Lab 2', 'Lab 2', 'Lab 1', 'Lab 1']
        self.design_a = "Design A"
        self.design_b = "Design B"
        self.home_lab = {self.design_a: 'Lab 1', self.design_b: 'Lab 2'}
        
        # State
        self.wins = {self.design_a: 0, self.design_b: 0}
        self.game_num = 0
        self.game_log = []
        self.series_over = False
        self.bulk_results = []
        
        # UI
        self.out = widgets.Output()
        self.out_plot = widgets.Output()
        self.btn_test = widgets.Button(description="🔬 Run Next Test", button_style='success', layout=widgets.Layout(width='180px', height='40px'))
        self.btn_reset = widgets.Button(description="🔄 Reset", button_style='warning', layout=widgets.Layout(width='100px', height='40px'))
        self.btn_sim = widgets.Button(description="⚡ Simulate 1000 Series", button_style='info', layout=widgets.Layout(width='200px', height='40px'))
        
        self.btn_test.on_click(self.play_game)
        self.btn_reset.on_click(self.reset)
        self.btn_sim.on_click(self.run_bulk)
        
        self.update()
        display(widgets.VBox([
            widgets.HTML("<h3>🏗️ Structural Testing Series: Design A vs. Design B</h3>"),
            widgets.HTML("<b>Format:</b> Best of 7 load tests. Home lab advantage: 55%."),
            widgets.HBox([self.btn_test, self.btn_reset, self.btn_sim]),
            self.out, self.out_plot
        ]))
    
    def play_game(self, _):
        if self.series_over or self.game_num >= 7:
            return
        lab = self.schedule[self.game_num]
        # Determine home design
        home_design = self.design_a if lab == 'Lab 1' else self.design_b
        away_design = self.design_b if lab == 'Lab 1' else self.design_a
        
        if np.random.random() < self.home_win_prob:
            winner = home_design
        else:
            winner = away_design
        
        self.wins[winner] += 1
        self.game_num += 1
        self.game_log.append(f"Test {self.game_num} ({lab}): {winner} passes")
        
        if self.wins[self.design_a] == 4 or self.wins[self.design_b] == 4:
            self.series_over = True
        self.update()
    
    def reset(self, _):
        self.wins = {self.design_a: 0, self.design_b: 0}
        self.game_num = 0
        self.game_log = []
        self.series_over = False
        self.update()
    
    def update(self):
        self.out.clear_output(wait=True)
        with self.out:
            print(f"Design A: {self.wins[self.design_a]} wins | Design B: {self.wins[self.design_b]} wins")
            print(f"Tests completed: {self.game_num}/7")
            for entry in self.game_log:
                print(f"  {entry}")
            if self.series_over:
                winner = self.design_a if self.wins[self.design_a] == 4 else self.design_b
                print(f"\\n🏆 {winner} wins the contract in {self.game_num} tests!")
    
    def run_bulk(self, _):
        a_wins_series = 0
        lengths = []
        for _ in range(1000):
            w = {self.design_a: 0, self.design_b: 0}
            for g in range(7):
                lab = self.schedule[g]
                home = self.design_a if lab == 'Lab 1' else self.design_b
                away = self.design_b if lab == 'Lab 1' else self.design_a
                winner = home if np.random.random() < self.home_win_prob else away
                w[winner] += 1
                if w[self.design_a] == 4 or w[self.design_b] == 4:
                    lengths.append(g + 1)
                    if w[self.design_a] == 4:
                        a_wins_series += 1
                    break
        
        self.out_plot.clear_output(wait=True)
        with self.out_plot:
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            axes[0].bar(['Design A', 'Design B'], [a_wins_series, 1000-a_wins_series], color=['steelblue', 'coral'])
            axes[0].set_title(f'Series Wins (1000 simulations)')
            axes[0].set_ylabel('Count')
            axes[1].hist(lengths, bins=range(4, 9), edgecolor='black', alpha=0.7, align='left', color='steelblue')
            axes[1].set_xlabel('Series Length (# of tests)')
            axes[1].set_ylabel('Frequency')
            axes[1].set_title(f'Series Length Distribution (Mean: {np.mean(lengths):.1f})')
            plt.tight_layout()
            plt.show()

sim = TestingSeriesSimulator()
"""

# ── Cell 22: Dorm lottery → Lab Assignment Lottery ────────────
CELL_REPLACEMENTS[22] = """🔬 **Lab Assignment Lottery Model**

Scenario: 57 engineers enter a lottery for 3 premium lab bench assignments. 20 are from the **Structures Team**, 37 are from **Other Teams**.

Question: How likely is it that all 3 winners are from the Structures Team?

Simulation Setup (Random Digits 01-99):
01 - 20 = Structures Team (20 engineers)
21 - 57 = Other Teams (37 engineers)
58 - 99, 00 = Skip / Ignore

Ignore duplicates (cannot win twice).
Select 3 winners per trial.
"""

# ── Cell 23: Dorm lottery intro ───────────────────────────────
CELL_REPLACEMENTS[23] = """### 🔬 Interactive Lab Assignment Lottery Simulator

**Run the cell below** to simulate the lottery.
"""

# ── Cell 24: Dorm Lottery Simulator code ──────────────────────
CELL_REPLACEMENTS[24] = """# @title 🔬 Lab Assignment Lottery Simulator - Click 'Play' to Start
import ipywidgets as widgets
from IPython.display import display, clear_output
import numpy as np
import matplotlib.pyplot as plt

class LabLotterySimulator:
    def __init__(self):
        # Configuration
        self.total_engineers = 57
        self.num_structures = 20
        self.spots = 3
        
        # Simulation State
        self.results = []
        self.current_draw = []
        
        # UI
        self.out = widgets.Output()
        self.out_plot = widgets.Output()
        self.btn_draw = widgets.Button(description="🎲 Draw 3 Winners", button_style='success',
                                    layout=widgets.Layout(width='180px', height='40px'))
        self.btn_sim = widgets.Button(description="⚡ Simulate 10,000 Draws", button_style='info',
                                  layout=widgets.Layout(width='200px', height='40px'))
        
        self.btn_draw.on_click(self.draw)
        self.btn_sim.on_click(self.bulk_sim)
        
        display(widgets.VBox([
            widgets.HTML("<h3>🔬 Lab Assignment Lottery</h3>"),
            widgets.HTML("<b>Setup:</b> 57 engineers (20 Structures Team, 37 Others). Drawing 3 winners."),
            widgets.HBox([self.btn_draw, self.btn_sim]),
            self.out, self.out_plot
        ]))
    
    def draw(self, _):
        # Create population: 20 structures, 37 others
        pool = ['Structures']*self.num_structures + ['Other']*( self.total_engineers - self.num_structures)
        winners = np.random.choice(pool, size=self.spots, replace=False)
        structures_count = list(winners).count('Structures')
        self.results.append(structures_count)
        
        self.out.clear_output(wait=True)
        with self.out:
            print(f"Draw #{len(self.results)}: {list(winners)}")
            print(f"Structures Team winners: {structures_count} out of {self.spots}")
            if structures_count == self.spots:
                print("⚠️ ALL winners are from the Structures Team!")
            all_structures = sum(1 for r in self.results if r == self.spots)
            print(f"\\nRunning total: {all_structures}/{len(self.results)} draws had ALL Structures winners ({100*all_structures/len(self.results):.1f}%)")
    
    def bulk_sim(self, _):
        pool = ['Structures']*self.num_structures + ['Other']*(self.total_engineers - self.num_structures)
        counts = []
        for _ in range(10000):
            winners = np.random.choice(pool, size=self.spots, replace=False)
            counts.append(list(winners).count('Structures'))
        
        all_three = sum(1 for c in counts if c == 3)
        
        self.out_plot.clear_output(wait=True)
        with self.out_plot:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.hist(counts, bins=[-0.5, 0.5, 1.5, 2.5, 3.5], edgecolor='black', alpha=0.7, color='steelblue')
            ax.set_xticks([0, 1, 2, 3])
            ax.set_xlabel('Number of Structures Team Winners')
            ax.set_ylabel('Frequency (out of 10,000)')
            ax.set_title(f'Lab Lottery: P(All 3 from Structures) = {all_three/10000:.4f} ({all_three}/10,000)')
            ax.grid(alpha=0.3)
            plt.tight_layout()
            plt.show()

sim = LabLotterySimulator()
"""

# ── Cell 25: Free throw title ─────────────────────────────────
CELL_REPLACEMENTS[25] = """### Example 3: Beam Load Testing
"""

# ── Cell 26: Free throw model description ─────────────────────
CELL_REPLACEMENTS[26] = """🏗️ **Beam Load Test Model**

Scenario: A quality engineer runs load tests on steel beams. Modeling continuous testing, batch testing, and sequential load protocols.

**Reliability:** Starts at 80% pass rate, improves to 86% with upgraded fabrication.

Digit Assignment (00-99) for 80% Reliability:
00 - 79 = Pass (beam meets load specification)
80 - 99 = Fail

Note: If reliability improves to 86%, the range becomes 00-85 for Pass.

Sample Trial (Test until Failure, 80%):
Digits 73 18 95...
Shots: Pass Pass **Fail** → Streak of 2 passes before first failure.
"""

# ── Cell 27: Free throw lab intro ─────────────────────────────
CELL_REPLACEMENTS[27] = """### 🏗️ Interactive Beam Load Test Lab

**Run the cell below** to start testing. Change the **Scenario** dropdown to match the question (Continuous Testing vs Batch of 5).
"""

# ── Cell 28: Free Throw Simulator code ────────────────────────
CELL_REPLACEMENTS[28] = """# @title 🏗️ Beam Load Test Simulator - Click 'Play' to Start
import ipywidgets as widgets
from IPython.display import display, clear_output
import numpy as np
import matplotlib.pyplot as plt

class BeamLoadSimulator:
    def __init__(self):
        # Config
        self.reliability = 80
        self.mode = 'continuous'  # 'continuous' (geo), 'batch5' (binom), 'dual_load'
        
        # UI Elements
        self.out_display = widgets.Output()
        self.out_plot = widgets.Output()
        
        self.accuracy_slider = widgets.IntSlider(value=80, min=50, max=99, step=1,
                                               description='Reliability %:', style={'description_width': 'initial'})
        self.mode_dropdown = widgets.Dropdown(
            options=[('Test Beams until Failure', 'continuous'),
                     ('Batch of 5 Beams', 'batch5'),
                     ('Sequential Load Test', 'dual_load')],
            value='continuous', description='Scenario:', style={'description_width': 'initial'})
        
        self.btn_test = widgets.Button(description="🔬 Run Test", button_style='success',
                                    layout=widgets.Layout(width='150px', height='40px'))
        self.btn_sim = widgets.Button(description="⚡ Simulate 1000", button_style='info',
                                  layout=widgets.Layout(width='180px', height='40px'))
        self.btn_reset = widgets.Button(description="🔄 Reset", button_style='warning',
                                    layout=widgets.Layout(width='100px', height='40px'))
        
        self.btn_test.on_click(self.run_one)
        self.btn_sim.on_click(self.run_bulk)
        self.btn_reset.on_click(self.reset)
        
        # State
        self.results = []
        
        display(widgets.VBox([
            widgets.HTML("<h3>🏗️ Beam Load Test Simulator</h3>"),
            widgets.HBox([self.accuracy_slider, self.mode_dropdown]),
            widgets.HBox([self.btn_test, self.btn_sim, self.btn_reset]),
            self.out_display, self.out_plot
        ]))
    
    def run_one(self, _):
        p = self.accuracy_slider.value / 100
        mode = self.mode_dropdown.value
        
        if mode == 'continuous':
            # Test until first failure
            count = 0
            while np.random.random() < p:
                count += 1
            result = count
            label = f"Passed {count} beams before failure"
        elif mode == 'batch5':
            # Count passes out of 5
            passes = sum(1 for _ in range(5) if np.random.random() < p)
            result = passes
            label = f"Passed {passes}/5 beams"
        else:  # dual_load
            # First test: if pass, do second test
            first = np.random.random() < p
            if first:
                second = np.random.random() < p
                result = 2 if second else 1
                label = f"First: PASS, Second: {'PASS' if second else 'FAIL'} → {result} point(s)"
            else:
                result = 0
                label = f"First: FAIL → 0 points"
        
        self.results.append(result)
        self.out_display.clear_output(wait=True)
        with self.out_display:
            print(f"Trial #{len(self.results)}: {label}")
            print(f"Average so far: {np.mean(self.results):.2f}")
    
    def run_bulk(self, _):
        p = self.accuracy_slider.value / 100
        mode = self.mode_dropdown.value
        results = []
        
        for _ in range(1000):
            if mode == 'continuous':
                count = 0
                while np.random.random() < p:
                    count += 1
                results.append(count)
            elif mode == 'batch5':
                results.append(sum(1 for _ in range(5) if np.random.random() < p))
            else:
                first = np.random.random() < p
                if first:
                    second = np.random.random() < p
                    results.append(2 if second else 1)
                else:
                    results.append(0)
        
        self.out_plot.clear_output(wait=True)
        with self.out_plot:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.hist(results, bins=range(min(results), max(results)+2), edgecolor='black', alpha=0.7, color='steelblue', align='left')
            ax.axvline(np.mean(results), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(results):.2f}')
            mode_labels = {'continuous': 'Passes Before Failure', 'batch5': 'Passes out of 5', 'dual_load': 'Points Scored'}
            ax.set_xlabel(mode_labels.get(mode, 'Result'))
            ax.set_ylabel('Frequency')
            ax.set_title(f'1000 Simulations ({self.accuracy_slider.value}% reliability)')
            ax.legend()
            ax.grid(alpha=0.3)
            plt.tight_layout()
            plt.show()
    
    def reset(self, _):
        self.results = []
        self.out_display.clear_output()
        self.out_plot.clear_output()

sim = BeamLoadSimulator()
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
    bad = ["cereal", "Simone Biles", "Caitlin Clark", "Serena Williams",
           "athlete", "free throw", "basketball", "Philly", "Boston",
           "Red Sox", "Phillies", "dorm room", "varsity", "Sean"]
    print("\n--- Coherence Critic ---")
    fails = 0
    for w in bad:
        if w.lower() in clean.lower():
            print(f"  ❌ FAIL: Found \"{w}\"")
            fails += 1
    if fails == 0:
        print("  🎉 All clear!")
    
    print("\n--- Nonsense Critic (rewritten cells) ---")
    nb_c = json.load(open(OUTPUT_NB))
    for idx in sorted(CELL_REPLACEMENTS.keys()):
        cell = nb_c["cells"][idx]
        src = "".join(cell.get("source", "")) if isinstance(cell.get("source"), list) else cell.get("source", "")
        preview = re.sub(r'<[^>]+>', '', src)
        preview = re.sub(r'\s+', ' ', preview).strip()[:180]
        print(f"  Cell {idx}: {preview}...")

if __name__ == "__main__":
    main()
