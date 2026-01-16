import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell
import os
import textwrap

def create_styled_lottery_content():
    # Explanation HTML
    # We strip indentation to prevent markdown code block rendering
    html = """
<div style="background-color: #f0f7fb; padding: 15px; border-radius: 5px; margin-bottom: 20px; border-left: 5px solid #007bff;">
    <h4 style="margin-top:0; color: #007bff;">🎫 Dorm Room Lottery Model</h4>
    <p><strong>Scenario:</strong> 57 students enter a lottery for 3 spots. 20 are Athletes, 37 are Non-Athletes.</p>
    <p><strong>Question:</strong> How likely is it that <em>all 3 winners</em> are Athletes?</p>
    <hr>
    <strong>Simulation Setup (Random Digits 01-99):</strong>
    <ul>
        <li><span style="background-color: #ffeeba; padding: 2px 5px; border-radius: 3px;"><strong>01 - 20</strong></span> = <strong>Athlete</strong> (20 students)</li>
        <li><span style="background-color: #e2e3e5; padding: 2px 5px; border-radius: 3px;"><strong>21 - 57</strong></span> = <strong>Non-Athlete</strong> (37 students)</li>
        <li><span style="color: #999;">58 - 99, 00</span> = Skip / Ignore</li>
        <li><em>Ignore duplicates (cannot win twice).</em></li>
    </ul>
</div>

<p><strong>Sample Trial:</strong> Using random digits <code>74 02 94 39 02 77 55...</code></p>
<table class="table" style="width: 100%; border: 1px solid #ddd;">
    <thead style="background-color: #eee;">
        <tr>
            <th>Draw</th>
            <th>Random Digit</th>
            <th>Result</th>
            <th>Selection</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>1</td><td><span style="color:#999">74</span></td><td>Skip (>57)</td><td>-</td></tr>
        <tr><td>2</td><td><span style="color:#007bff; font-weight:bold;">02</span></td><td><strong>Athlete</strong></td><td>1. Athlete</td></tr>
        <tr><td>3</td><td><span style="color:#999">94</span></td><td>Skip (>57)</td><td>-</td></tr>
        <tr><td>4</td><td><span>39</span></td><td>Non-Athlete</td><td>2. Non-Athlete</td></tr>
        <tr><td>5</td><td><span style="color:#007bff;">02</span></td><td>Duplicate</td><td>-</td></tr>
        <tr><td>6</td><td><span style="color:#999">77</span></td><td>Skip (>57)</td><td>-</td></tr>
        <tr><td>7</td><td><span>55</span></td><td>Non-Athlete</td><td>3. Non-Athlete</td></tr>
    </tbody>
</table>
<p><strong>Trial Outcome:</strong> 1 Athlete, 2 Non-Athletes. (Not an all-athlete win).</p>
"""
    return textwrap.dedent(html)

def create_widget_code():
    return """import ipywidgets as widgets
from IPython.display import display, clear_output
import numpy as np
import matplotlib.pyplot as plt

class DormLotterySimulator:
    def __init__(self):
        # Configuration
        self.total_students = 57
        self.num_athletes = 20
        self.spots = 3
        
        # Simulation State
        self.results = [] # Store count of athletes in each trial (0, 1, 2, or 3)
        self.current_winners = []
        
        # UI Elements
        self.out_display = widgets.Output()
        self.out_plot = widgets.Output()
        
        self.btn_draw = widgets.Button(description="Run 1 Lottery", button_style='info', icon='ticket')
        self.btn_sim_1000 = widgets.Button(description="Simulate 1000 Lotteries", button_style='success', icon='fast-forward')
        self.btn_reset = widgets.Button(description="Reset Stats", button_style='warning', icon='refresh')
        
        self.btn_draw.on_click(self.on_draw)
        self.btn_sim_1000.on_click(self.on_sim_1000)
        self.btn_reset.on_click(self.on_reset)
        
        self.dashboard = widgets.VBox([
            widgets.HTML("<h3>🎫 Interactive Lottery Simulator</h3>"),
            widgets.HTML(f"<p>Draw <strong>{self.spots}</strong> winners from <strong>{self.total_students}</strong> students ({self.num_athletes} Athletes).</p>"),
            widgets.HBox([self.btn_draw, self.btn_reset]),
            self.out_display,
            widgets.HTML("<hr>"),
            self.btn_sim_1000,
            self.out_plot
        ])
        
        self.update_display()

    def run_lottery(self):
        # Create pool: 1=Athlete, 0=Non-Athlete
        pool = [1]*self.num_athletes + [0]*(self.total_students - self.num_athletes)
        # Draw without replacement
        winners = np.random.choice(pool, size=self.spots, replace=False)
        return winners

    def on_draw(self, b):
        self.current_winners = self.run_lottery()
        athlete_count = sum(self.current_winners)
        self.results.append(athlete_count)
        self.update_display()

    def on_sim_1000(self, b):
        new_results = [sum(self.run_lottery()) for _ in range(1000)]
        self.results.extend(new_results)
        self.current_winners = []
        self.update_display()
        self.update_plot()

    def on_reset(self, b):
        self.results = []
        self.current_winners = []
        self.out_plot.clear_output()
        self.update_display()

    def update_display(self):
        with self.out_display:
            clear_output(wait=True)
            
            # Show last draw if exists
            if len(self.current_winners) > 0:
                html_draw = '<div style="margin: 10px 0; font-size: 1.1em;">Last Draw: '
                for is_athlete in self.current_winners:
                    if is_athlete:
                        html_draw += '<span style="background:#ffeeba; border:1px solid #ffdf7e; padding:3px 8px; border-radius:10px; margin-right:5px;">🏃 Athlete</span>'
                    else:
                        html_draw += '<span style="background:#e2e3e5; border:1px solid #dae0e5; padding:3px 8px; border-radius:10px; margin-right:5px;">🎓 Student</span>'
                html_draw += '</div>'
                display(widgets.HTML(html_draw))
                
                if sum(self.current_winners) == 3:
                    display(widgets.HTML('<div style="color:red; font-weight:bold;">⚠️ ALL ATHLETES! (Suspicious?)</div>'))

    def update_plot(self):
        with self.out_plot:
            clear_output(wait=True)
            if not self.results: return
            
            counts = [self.results.count(i) for i in range(4)]
            total = len(self.results)
            
            plt.figure(figsize=(8, 4))
            bars = plt.bar(['0 Athletes', '1 Athlete', '2 Athletes', '3 Athletes'], counts, color=['#e2e3e5', '#badce3', '#ffeeba', '#f5c6cb'])
            
            # Add percentages
            for bar, count in zip(bars, counts):
                if count > 0:
                    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{count/total:.1%}', 
                             ha='center', va='bottom', fontweight='bold')
            
            plt.title(f"Outcomes of {total} Simulated Lotteries")
            plt.ylabel("Frequency")
            plt.grid(axis='y', alpha=0.3)
            plt.show()

# Run
lottery_sim = DormLotterySimulator()
display(lottery_sim.dashboard)
"""

def update_notebook():
    nb_path = 'Chapter_11.ipynb'
    if not os.path.exists(nb_path):
        print(f"Error: {nb_path} not found.")
        return

    print(f"Reading {nb_path}...")
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Search for "Example 2" to identify the cell
    target_idx = -1
    for i, cell in enumerate(nb.cells):
        if "**Example 2:**" in cell.source:
            target_idx = i
            break
            
    if target_idx == -1:
        print("Could not find Example 2 cell.")
        return

    print(f"Found Example 2 at cell {target_idx}. Updating content...")
    
    # 1. Update the static markdown cell
    nb.cells[target_idx].source = create_styled_lottery_content()
    
    # 2. Inject the widget immediately after
    # Check if widget is already there
    if target_idx + 1 < len(nb.cells) and "class DormLotterySimulator" in nb.cells[target_idx+1].source:
        print("Widget code already exists. Updating it...")
        nb.cells[target_idx+1].source = create_widget_code()
    else:
        print("Injecting new widget code...")
        
        # Create Header Cell
        header_cell = new_markdown_cell("### 🎫 Interactive Lottery Simulator\n\n**Run the cell below** to simulate the lottery.")
        
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
