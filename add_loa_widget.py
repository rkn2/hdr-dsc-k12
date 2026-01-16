import nbformat
import os

def inject_loa_widget():
    nb_path = 'Chapter_12.ipynb'
    if not os.path.exists(nb_path):
        print(f"Error: {nb_path} not found.")
        return

    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    new_widget_code = """# @title 🎰 The Lottery Fallacy Simulator - Is a number "due"?
import ipywidgets as widgets
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, HTML, clear_output

# Configuration: Simple Pick-10 lottery (numbers 0-9)
NUM_OPTIONS = 10
COLOR_COLD = '#546E7A'
COLOR_HOT = '#FFB300'
COLOR_NEUTRAL = '#1E88E5'

class LotterySim:
    def __init__(self):
        self.history = []
        self.output = widgets.Output()
        self.status = widgets.HTML("<i>Click to simulate the 'Cold Number' scenario...</i>")
        
    def find_cold_number(self, threshold=30):
        # Reset and simulate until one number hasn't appeared for 'threshold' draws
        self.history = []
        counts_since_last = np.zeros(NUM_OPTIONS)
        draws = 0
        
        while np.max(counts_since_last) < threshold:
            draw = np.random.randint(0, NUM_OPTIONS)
            self.history.append(draw)
            counts_since_last += 1
            counts_since_last[draw] = 0
            draws += 1
            if draws > 5000: break # Safety break
            
        self.cold_num = np.argmax(counts_since_last)
        self.miss_streak = int(np.max(counts_since_last))
        self.update_ui()
        self.status.value = f"<span style='color:red;'>Found it!</span> Number <b>{self.cold_num}</b> hasn't appeared in <b>{self.miss_streak}</b> draws. Many people think it is now <b>'due'</b>."

    def test_next_draws(self, trials=1000):
        if not hasattr(self, 'cold_num'):
            self.status.value = "<b>Please find a cold number first!</b>"
            return
            
        # Run many 'next draws' and see how often the 'cold' number hits
        next_draws = np.random.randint(0, NUM_OPTIONS, size=trials)
        hits = np.count_nonzero(next_draws == self.cold_num)
        expected = trials / NUM_OPTIONS
        
        with self.output:
            clear_output(wait=True)
            fig, ax = plt.subplots(figsize=(7, 4))
            unique, counts = np.unique(next_draws, return_counts=True)
            
            # Map counts to all 10 positions
            full_counts = np.zeros(NUM_OPTIONS)
            for u, c in zip(unique, counts):
                full_counts[u] = c
                
            colors = [COLOR_NEUTRAL] * NUM_OPTIONS
            colors[self.cold_num] = COLOR_HOT
            
            bars = ax.bar(range(NUM_OPTIONS), full_counts, color=colors)
            ax.axhline(expected, color='black', linestyle='--', alpha=0.5, label='Theoretical Expectation (10%)')
            
            ax.set_xticks(range(NUM_OPTIONS))
            ax.set_xlabel('Lottery Number')
            ax.set_ylabel(f'Hits in {trials} Next Draws')
            ax.set_title(f'Frequency of Outcomes Following the {self.miss_streak}-Draw Cold Streak')
            ax.legend()
            
            # Highlight the cold number result
            hit_pct = (hits/trials)*100
            self.status.value = f"<b>Results:</b> In the {trials} draws <i>after</i> the streak, number {self.cold_num} hit {hits} times (<b>{hit_pct:.1f}%</b>).<br>" + \\
                               f"It didn't come up more often just because it was 'late'. The odds were still exactly {100/NUM_OPTIONS:.0f}% every time."
            plt.show()

    def update_ui(self):
        with self.output:
            clear_output(wait=True)
            html = f"<p>Number <b>{self.cold_num}</b> is 'Cold'. It has missed {self.miss_streak} draws in a row.</p>"
            display(HTML(html))

sim = LotterySim()

# UI Parts
header = widgets.HTML(\"\"\"
<div style="background-color: #f0f4f8; padding: 15px; border-radius: 8px; border-left: 5px solid #1E88E5; margin-bottom: 10px;">
    <h3 style="margin-top: 0; color: #1E88E5;">The Nonexistent Law of Averages</h3>
    <p>A common lottery proposal is to avoid numbers that came up lately and bet on numbers that are <b>"due"</b> because they haven't appeared in a long time.</p>
    <p><b>Faulty Reasoning:</b> Proponents argue that in the long run, every number should be selected equally often, so cold numbers must "catch up." 
    In reality, the lottery machine has no memory!</p>
</div>
\"\"\")

find_btn = widgets.Button(description='Find a "Cold" Number', button_style='warning', layout=widgets.Layout(width='200px'))
test_btn = widgets.Button(description='Run 1000 Next Draws', button_style='success', layout=widgets.Layout(width='200px'))

find_btn.on_click(lambda _: sim.find_cold_number(40))
test_btn.on_click(lambda _: sim.test_next_draws(1000))

controls = widgets.HBox([find_btn, test_btn])
display(header, sim.status, controls, sim.output)
"""

    search_text = "THE LAW OF AVERAGES DOES NOT EXIST"
    found_idx = -1
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'markdown' and search_text in cell.source:
            found_idx = i
            break
            
    if found_idx != -1:
        # Keep the updated text
        intro_text = (
            "**<u>The Nonexistent Law of Averages</u>**\n\n"
            "THE LAW OF AVERAGES DOES NOT EXIST! The LLN says nothing about short-run behavior. "
            "Relative frequencies even out only in the long run, and this long run is infinitely long.\n\n"
            "<u>Example:</u> One common proposal for beating the lottery is to note which numbers have come up lately, "
            "eliminate those from consideration, and bet on numbers that have not come up for a long time. "
            "Proponents of this method argue that in the long run, every number should be selected equally often, "
            "so those that haven’t come up are due. Use the simulator below to explore why this is faulty reasoning."
        )
        nb.cells[found_idx].source = intro_text
        
        # Replace the widget cell
        widget_cell = nbformat.v4.new_code_cell(source=new_widget_code)
        widget_cell.metadata = {"cellView": "form"}
        
        if (found_idx + 1) < len(nb.cells) and nb.cells[found_idx+1].cell_type == 'code':
             nb.cells[found_idx + 1] = widget_cell
        else:
             nb.cells.insert(found_idx + 1, widget_cell)
        
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print("Lottery-themed Gambler's Fallacy widget injected.")
    else:
        print("Could not find the target section.")

if __name__ == "__main__":
    inject_loa_widget()
