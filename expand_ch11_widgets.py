
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell
import os

def create_run_length_code():
    return """
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display

def run_length_sim(n_flips=50):
    # Simulate fair coin flips
    flips = np.random.choice(['H', 'T'], size=n_flips)
    
    # Calculate Run Lengths
    runs = []
    current_run = 1
    for i in range(1, len(flips)):
        if flips[i] == flips[i-1]:
            current_run += 1
        else:
            runs.append(current_run)
            current_run = 1
    runs.append(current_run)
    
    # Plotting
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: The Sequence Grid
    # Visualize flips as a grid of colored tiles
    cols = 10
    rows = n_flips // cols + (1 if n_flips % cols > 0 else 0)
    
    for i, f in enumerate(flips):
        r = i // cols
        c = i % cols
        color = 'blue' if f == 'H' else 'orange'
        rect = plt.Rectangle((c, -r), 1, 1, facecolor=color, edgecolor='white')
        ax1.add_patch(rect)
        ax1.text(c+0.5, -r+0.5, f, ha='center', va='center', color='white', weight='bold')

    ax1.set_xlim(0, cols)
    ax1.set_ylim(-rows, 0)
    ax1.axis('off')
    ax1.set_title(f"Sequence of {n_flips} Flips (Blue=H, Orange=T)")
    
    # Plot 2: Histogram of Run Lengths
    max_run = max(runs) if runs else 0
    counts, bins, patches = ax2.hist(runs, bins=range(1, max_run+2), align='left', rwidth=0.8, color='purple', alpha=0.7)
    ax2.set_xticks(range(1, max_run+1))
    ax2.set_xlabel('Run Length')
    ax2.set_ylabel('Frequency')
    ax2.set_title(f"Distribution of Streaks (Max Run: {max_run})")
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()

display(widgets.interactive(run_length_sim, 
                            n_flips=widgets.IntSlider(value=50, min=20, max=200, step=10, description='Total Flips:')))
"""

def create_intro_markdown():
    return """
### Interactive Experiment: The "Hot Hand" Fallacy

Humans are terrible at spotting true randomness. We typically think "random" means "alternating" (H T H T H T).
In reality, true randomness often contains **streaks** (long runs of the same outcome, like H H H H H).

**Explore:**
*   Simulate 50 or 100 coin flips.
*   Look at the "Sequence" grid. Do you see clusters of Blue (Heads) or Orange (Tails)? 
*   Look at the "Distribution Check" graph. Note the **Max Run Length**. It is not uncommon to see a run of 5, 6, or even 7 heads in a row purely by chance!
"""

def inject_widgets(notebook_path, output_path):
    print(f"Reading {notebook_path}...")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Insert after "Randomness:" (Cell 1 usually)
    idx = -1
    for i, cell in enumerate(nb.cells):
        if "**<u>Randomness:</u>**" in cell.source:
            idx = i + 1
            break
            
    if idx != -1:
        print(f"Injecting Run Length Widget after cell {idx-1}...")
        nb.cells.insert(idx, new_markdown_cell(create_intro_markdown()))
        nb.cells.insert(idx + 1, new_code_cell(create_run_length_code()))
    else:
        print("Warning: Target cell 'Randomness' not found. Appending to beginning.")
        nb.cells.insert(1, new_markdown_cell(create_intro_markdown()))
        nb.cells.insert(2, new_code_cell(create_run_length_code()))

    print(f"Saving to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Done!")

if __name__ == "__main__":
    inject_widgets("Chapter_11.ipynb", "Chapter_11.ipynb")
