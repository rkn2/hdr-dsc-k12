import nbformat
import os

def inject_lln_widget():
    nb_path = 'Chapter_12.ipynb'
    if not os.path.exists(nb_path):
        print(f"Error: {nb_path} not found.")
        return

    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    new_widget_code = """# @title 📈 Law of Large Numbers Simulator - Click 'Run Simulation'
import ipywidgets as widgets
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, HTML, clear_output

# Configuration
TRUE_PROB = 60 # Default true probability (60%)
COLOR_GREEN = '#2E7D32'
COLOR_RED = '#C62828'

# State management
class LLNSimulator:
    def __init__(self):
        self.days = []
        self.outcomes = []
        self.percentages = []
        self.current_day = 0
        self.successes = 0
        
        self.plot_out = widgets.Output()
        self.table_out = widgets.Output()
        
    def reset(self):
        self.days = []
        self.outcomes = []
        self.percentages = []
        self.current_day = 0
        self.successes = 0
        self.update_display()
        
    def run_trials(self, count):
        new_outcomes = np.random.random(count) < (TRUE_PROB / 100.0)
        for result in new_outcomes:
            self.current_day += 1
            if result: self.successes += 1
            self.days.append(self.current_day)
            self.outcomes.append('Green' if result else 'Red')
            self.percentages.append((self.successes / self.current_day) * 100)
        self.update_display()

    def update_display(self):
        with self.plot_out:
            clear_output(wait=True)
            if not self.days:
                fig, ax = plt.subplots(figsize=(7, 5))
                ax.set_xlim(0, 1000)
                ax.set_ylim(0, 100)
                ax.set_ylabel('Percent Green', fontsize=12)
                ax.set_xlabel('Day Number', fontsize=12)
                ax.set_title('Accumulated Percentage over Time', fontsize=14)
                plt.show()
                return

            fig, ax = plt.subplots(figsize=(7, 5))
            ax.plot(self.days, self.percentages, color=COLOR_GREEN, linewidth=2)
            ax.axhline(y=TRUE_PROB, color='#555', linestyle='--', alpha=0.5, label=f'True Prob ({TRUE_PROB}%)')
            
            ax.set_ylim(0, 100)
            ax.set_ylabel('Percent Green', fontsize=12)
            ax.set_xlabel('Day Number', fontsize=12)
            ax.set_title('Accumulated Percentage over Time', fontsize=14)
            ax.grid(True, linestyle=':', alpha=0.6)
            
            # Show landmark ticks
            landmarks = [1, 2, 6, 100, 300, 500, 800]
            current_ticks = [t for t in landmarks if t <= self.current_day]
            if self.current_day not in current_ticks: current_ticks.append(self.current_day)
            ax.set_xticks(sorted(list(set(current_ticks))))
            
            plt.show()

        with self.table_out:
            clear_output(wait=True)
            if not self.days:
                display(HTML("<p style='color:#777;'>No data yet.</p>"))
                return
            
            html = '<div style="max-height: 300px; overflow-y: auto;"><table style="width:100%; border-collapse: collapse; text-align: center; font-family: sans-serif; font-size: 0.9em;">'
            html += '<tr style="background-color: #f2f2f2; position: sticky; top: 0;"><th>Day</th><th>Light</th><th>% Green</th></tr>'
            
            if len(self.days) <= 12:
                rows = range(len(self.days))
            else:
                rows = list(range(5)) + [None] + list(range(len(self.days)-5, len(self.days)))

            for i in rows:
                if i is None:
                    html += '<tr><td colspan="3" style="padding: 5px; color: #999;">... skipping ...</td></tr>'
                    continue
                c = COLOR_GREEN if self.outcomes[i] == 'Green' else COLOR_RED
                bg = "#fff" if i % 2 == 0 else "#fafafa"
                html += f'<tr style="background-color: {bg}; border-bottom: 1px solid #eee;">'
                html += f'<td style="padding: 5px;">{self.days[i]}</td>'
                html += f'<td style="padding: 5px; color:{c}; font-weight:bold;">{self.outcomes[i]}</td>'
                html += f'<td style="padding: 5px;">{self.percentages[i]:.1f}%</td></tr>'
            html += '</table></div>'
            display(HTML(html))

sim = LLNSimulator()

header = widgets.HTML(\"\"\"
<div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 5px solid #2E7D32; margin-bottom: 10px;">
    <h3 style="margin-top: 0; color: #2E7D32;">The Law of Large Numbers (LLN)</h3>
    <p style="margin-bottom: 5px;">The <b>Law of Large Numbers</b> states that the long-run relative frequency of repeated independent events gets closer and closer to a single value—the theoretical probability.</p>
    <p style="margin-top: 0;">Because this definition is based on repeatedly observing trial outcomes, it is often called <b>empirical probability</b>.</p>
</div>
\"\"\")

batch_dropdown = widgets.Dropdown(
    options=[('Add 1 Day', 1), ('Add 5 Days', 5), ('Add 50 Days', 50), ('Add 100 Days', 100), ('Add 500 Days', 500)],
    value=1,
    description='Step:',
    style={'description_width': 'initial'}
)

run_btn = widgets.Button(description='Run Simulation', button_style='primary', icon='play', layout=widgets.Layout(width='150px'))
reset_btn = widgets.Button(description='Reset', button_style='', layout=widgets.Layout(width='80px'))

def on_run(_): sim.run_trials(batch_dropdown.value)
def on_reset(_): sim.reset()

run_btn.on_click(on_run)
reset_btn.on_click(on_reset)

footer = widgets.HTML(\"\"\"
<div style="margin-top: 10px; padding: 10px; border-top: 1px solid #eee;">
    <p style="font-size: 0.95em; color: #444;">
        <b>Summary:</b> Observe the <i>Percent Green</i> line. At low day numbers, the percentage is volatile and can jump significantly with each new trial. 
        As you simulate more days, the percentage <b>settles down</b> and stabilizes around the theoretical probability (60%), visually demonstrating the Law of Large Numbers.
    </p>
</div>
\"\"\")

controls_box = widgets.VBox([
    widgets.HTML("<b>Interactive Data Table & Controls</b>"),
    sim.table_out,
    widgets.VBox([batch_dropdown, widgets.HBox([run_btn, reset_btn])], layout=widgets.Layout(margin='10px 0 0 0'))
], layout=widgets.Layout(width='38%', margin='0 0 0 20px'))

main_content = widgets.HBox([sim.plot_out, controls_box], layout=widgets.Layout(align_items='flex-start'))

display(header, main_content, footer)
sim.run_trials(1)
"""

    search_text = "You keep track of what happens at an intersection each day"
    found_idx = -1
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'markdown' and search_text in cell.source:
            found_idx = i
            break
            
    if found_idx != -1:
        # Create the markdown section header
        header_text = "**<u>The Law of Large Numbers</u>**\n\n<u>Example:</u> You keep track of what happens at an intersection each day. A graph of the accumulated percentage of green lights looks like this:"
        nb.cells[found_idx].source = header_text
        
        # Check if the next cell is our widget already (since we might be re-running)
        if (found_idx + 1) < len(nb.cells) and nb.cells[found_idx+1].cell_type == 'code' and 'LLNSimulator' in nb.cells[found_idx+1].source:
             nb.cells[found_idx + 1].source = new_widget_code
        else:
             widget_cell = nbformat.v4.new_code_cell(source=new_widget_code)
             widget_cell.metadata = {"cellView": "form"}
             nb.cells.insert(found_idx + 1, widget_cell)
        
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print("Widget injected/updated successfully.")
    else:
        print("Could not find the target section for the simulation.")

if __name__ == "__main__":
    inject_lln_widget()
