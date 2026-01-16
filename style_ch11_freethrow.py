import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell
import os
import textwrap

def create_styled_freethrow_content():
    # Explanation HTML
    html = """
<div style="background-color: #fdf2e9; padding: 15px; border-radius: 5px; margin-bottom: 20px; border-left: 5px solid #d35400;">
    <h4 style="margin-top:0; color: #d35400;">🏀 Free Throw Model</h4>
    <p><strong>Scenario:</strong> Sean shoots free throws. Modeling streaks, sets, and foul shots.</p>
    <p><strong>Accuracy:</strong> Starts at <strong>80%</strong>, improves to <strong>86%</strong>.</p>
    <hr>
    <strong>Digit Assignment (00-99) for 80% Shooter:</strong>
    <ul>
        <li><span style="background-color: #dff0d8; padding: 2px 5px; border-radius: 3px;"><strong>00 - 79</strong></span> = <strong>Hit</strong> (Makes the shot)</li>
        <li><span style="background-color: #f2dede; padding: 2px 5px; border-radius: 3px;"><strong>80 - 99</strong></span> = <strong>Miss</strong></li>
    </ul>
    
    <p><em>Note: If accuracy changes to 86%, the range becomes 00-85 for Hits.</em></p>
</div>

<p><strong>Sample Trial (Streak to Miss, 80%):</strong> Digits <code>73 18 95...</code></p>
<table class="table" style="width: 100%; border: 1px solid #ddd;">
    <thead style="background-color: #eee;">
        <tr>
            <th>Shot</th>
            <th>Digit</th>
            <th>Result</th>
            <th>Streak Status</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>1</td><td><span style="color:green; font-weight:bold;">73</span></td><td>Hit</td><td>Continue</td></tr>
        <tr><td>2</td><td><span style="color:green; font-weight:bold;">18</span></td><td>Hit</td><td>Continue</td></tr>
        <tr><td>3</td><td><span style="color:red; font-weight:bold;">95</span></td><td><strong>Miss</strong> (>79)</td><td><strong>STOP</strong></td></tr>
    </tbody>
</table>
<p><strong>Result:</strong> Made 2 shots before missing.</p>
"""
    return textwrap.dedent(html)

def create_widget_code():
    return """import ipywidgets as widgets
from IPython.display import display, clear_output
import numpy as np
import matplotlib.pyplot as plt

class FreeThrowSimulator:
    def __init__(self):
        # Config
        self.accuracy = 80
        self.mode = 'streak' # 'streak' (geo), 'set5' (binom), '1and1'
        
        # UI Elements
        self.out_display = widgets.Output()
        self.out_plot = widgets.Output()
        
        # Controls
        self.sld_accuracy = widgets.IntSlider(value=80, min=50, max=100, step=1, description='Accuracy %')
        self.dd_mode = widgets.Dropdown(
            options=[
                ('Shoot until Miss (Streak)', 'streak'), 
                ('Set of 5 Shots', 'set5'), 
                ('1-and-1 Foul Shot', '1and1')
            ],
            value='streak',
            description='Scenario:'
        )
        
        self.btn_shoot = widgets.Button(description="Shoot!", button_style='warning', icon='basketball-ball')
        self.btn_sim_1000 = widgets.Button(description="Simulate 1000 Trials", button_style='success', icon='fast-forward')
        
        self.sld_accuracy.observe(self.on_config_change, names='value')
        self.dd_mode.observe(self.on_mode_change, names='value')
        self.btn_shoot.on_click(self.on_shoot)
        self.btn_sim_1000.on_click(self.on_sim_1000)
        
        # State
        self.last_result = None
        self.sim_results = []
        
        self.dashboard = widgets.VBox([
            widgets.HTML("<h3>🏀 Interactive Free Throw Lab</h3>"),
            widgets.HBox([self.dd_mode, self.sld_accuracy]),
            widgets.HTML("<hr>"),
            widgets.HBox([self.btn_shoot, self.btn_sim_1000]),
            self.out_display,
            self.out_plot
        ])
        
        self.update_display()

    def on_config_change(self, change):
        self.accuracy = self.sld_accuracy.value
        self.last_result = None
        self.sim_results = []
        self.out_plot.clear_output()
        self.update_display()

    def on_mode_change(self, change):
        self.mode = self.dd_mode.value
        self.last_result = None
        self.sim_results = []
        self.out_plot.clear_output() # Clear plot on mode switch to avoid confusion
        self.update_display()

    def make_shot(self):
        return np.random.rand() < (self.accuracy / 100.0)

    def run_trial(self):
        prob = self.accuracy / 100.0
        
        if self.mode == 'streak':
            shots = 0
            while True:
                if np.random.rand() < prob:
                    shots += 1
                else:
                    return shots # Returned value is number of hits BEFORE miss
                    
        elif self.mode == 'set5':
            makes = sum([1 for _ in range(5) if np.random.rand() < prob])
            return makes
            
        elif self.mode == '1and1':
            # 1-and-1 logic:
            # First shot: If miss -> 0 pts. If make -> Earn 2nd shot.
            # Second shot: If miss -> 1 pt. If make -> 2 pts.
            if np.random.rand() < prob: # Made 1st
                if np.random.rand() < prob: # Made 2nd
                    return 2
                else:
                    return 1
            else:
                return 0

    def on_shoot(self, b):
        # Visual single trial
        prob = self.accuracy / 100.0
        
        if self.mode == 'streak':
            makes = 0
            history = []
            while True:
                is_make = np.random.rand() < prob
                history.append(is_make)
                if is_make: makes += 1
                else: break
            self.last_result = {'type': 'streak', 'makes': makes, 'history': history}
            
        elif self.mode == 'set5':
            history = [np.random.rand() < prob for _ in range(5)]
            self.last_result = {'type': 'set5', 'makes': sum(history), 'history': history}
            
        elif self.mode == '1and1':
            history = []
            pts = 0
            # Shot 1
            s1 = np.random.rand() < prob
            history.append(s1)
            if s1:
                # Shot 2
                s2 = np.random.rand() < prob
                history.append(s2)
                pts = 2 if s2 else 1
            else:
                pts = 0
                
            self.last_result = {'type': '1and1', 'pts': pts, 'history': history}
            
        self.update_display()

    def on_sim_1000(self, b):
        self.sim_results = [self.run_trial() for _ in range(1000)]
        self.update_plot()
        
    def update_display(self):
        with self.out_display:
            clear_output(wait=True)
            
            if self.last_result:
                r = self.last_result
                html = "<div style='font-size: 1.2em; margin-top:10px;'>"
                
                # Visual balls
                balls = ""
                for h in r['history']:
                    if h: balls += "🟢 "
                    else: balls += "🔴 "
                
                if r['type'] == 'streak':
                    html += f"Result: <strong>{r['makes']} Makes</strong> in a row.<br>{balls}"
                elif r['type'] == 'set5':
                    html += f"Result: <strong>{r['makes']} / 5</strong> Made.<br>{balls}"
                elif r['type'] == '1and1':
                    html += f"Result: <strong>{r['pts']} Points</strong>.<br>{balls}"
                
                html += "</div>"
                display(widgets.HTML(html))

    def update_plot(self):
        with self.out_plot:
            clear_output(wait=True)
            if not self.sim_results: return
            
            plt.figure(figsize=(8, 4))
            
            # Bins depend on mode
            if self.mode == 'streak':
                # Geometric can be long, clip at 15 for viz
                data = [min(x, 15) for x in self.sim_results]
                max_val = max(data) if data else 5
                bins = np.arange(0, max_val + 2) - 0.5
                plt.hist(data, bins=bins, color='#d35400', alpha=0.7, edgecolor='white')
                plt.xlabel("Shots Made Before Miss")
                
            elif self.mode == 'set5':
                bins = np.arange(0, 7) - 0.5
                plt.hist(self.sim_results, bins=bins, color='#e67e22', alpha=0.7, edgecolor='white')
                plt.xlabel("Shots Made out of 5")
                plt.xticks(range(6))
                
            elif self.mode == '1and1':
                bins = np.arange(0, 4) - 0.5
                plt.hist(self.sim_results, bins=bins, color='#f39c12', alpha=0.7, edgecolor='white')
                plt.xlabel("Points Scored (0, 1, or 2)")
                plt.xticks([0, 1, 2])
            
            plt.title(f"Distribution of 1000 Trials (Acc: {self.accuracy}%)")
            plt.ylabel("Frequency")
            plt.show()

# Run
ft_sim = FreeThrowSimulator()
display(ft_sim.dashboard)
"""

def update_notebook():
    nb_path = 'Chapter_11.ipynb'
    if not os.path.exists(nb_path):
        print(f"Error: {nb_path} not found.")
        return

    print(f"Reading {nb_path}...")
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Search for "Example 3" to identify the cell
    target_idx = -1
    for i, cell in enumerate(nb.cells):
        if "**Example 3:**" in cell.source:
            target_idx = i
            break
            
    if target_idx == -1:
        print("Could not find Example 3 cell.")
        return

    print(f"Found Example 3 at cell {target_idx}. Updating content...")
    
    # 1. Update the static markdown cell
    nb.cells[target_idx].source = create_styled_freethrow_content()
    
    # 2. Inject the widget immediately after
    # Check if widget is already there
    if target_idx + 1 < len(nb.cells) and "class FreeThrowSimulator" in nb.cells[target_idx+1].source:
        print("Widget code already exists. Updating it...")
        nb.cells[target_idx+1].source = create_widget_code()
    else:
        print("Injecting new widget code...")
        
        # Create Header Cell
        header_cell = new_markdown_cell("### 🏀 Interactive Free Throw Lab\n\n**Run the cell below** to start shooting. Change the **Scenario** dropdown to match the question (Streak vs Set of 5).")
        
        # Create Code Cell
        code_cell = new_code_cell(create_widget_code())
        
        # Insert both
        nb.cells.insert(target_idx + 1, header_cell)
        nb.cells.insert(target_idx + 2, code_cell)

    print(f"Saving to {nb_path}...")
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Done!")

if __name__ == "__main__":
    update_notebook()
