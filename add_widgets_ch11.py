
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell
import os

def create_widget_code():
    return """
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display, clear_output

def run_lln_simulation(n_trials=100):
    # Simulate n_trials coin flips (0 for Tails, 1 for Heads)
    flips = np.random.choice([0, 1], size=n_trials)
    
    # Calculate cumulative proportion of heads
    cumulative_heads = np.cumsum(flips)
    trials = np.arange(1, n_trials + 1)
    proportions = cumulative_heads / trials
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(trials, proportions, label='Proportion of Heads', color='blue', linewidth=1)
    plt.axhline(0.5, color='red', linestyle='--', label='Theoretical Probability (0.5)')
    plt.ylim(0, 1)
    plt.title(f'Law of Large Numbers: {n_trials} Coin Flips')
    plt.xlabel('Number of Trials')
    plt.ylabel('Proportion of Heads')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

# Interactive controls
style = {'description_width': 'initial'}
n_trials_slider = widgets.IntSlider(value=100, min=10, max=2000, step=10, description='Number of Trials:', style=style)

ui = widgets.VBox([n_trials_slider])
out = widgets.interactive_output(run_lln_simulation, {'n_trials': n_trials_slider})

display(ui, out)
"""

def create_intro_markdown():
    return """
### Interactive Experiment: The Law of Large Numbers

**Simulation** allows us to imitate a real process to understand its behavior. One of the most important principles in statistics is the **Law of Large Numbers**, which states that as we perform more and more trials of a random process, the average result approaches the expected value.

In the simulation below, we flip a fair coin (probability of Heads = 0.5) many times.
*   **Move the slider** to increase the number of trials.
*   Observe how the "Proportion of Heads" fluctuates when $n$ is small but settles closer to the red dashed line (0.5) as $n$ gets larger.
"""

def inject_widgets(notebook_path, output_path):
    print(f"Reading {notebook_path}...")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Find insertion point: After "Simulation:" section (Cell 2 in inspection)
    # We look for the cell containing "**<u>Simulation:</u>**"
    insert_idx = -1
    for i, cell in enumerate(nb.cells):
        if "**<u>Simulation:</u>**" in cell.source:
            insert_idx = i + 1
            break
    
    if insert_idx == -1:
        print("Warning: Target cell '**<u>Simulation:</u>**' not found. Appending to end.")
        insert_idx = len(nb.cells)
    else:
        print(f"Inserting widgets after cell {insert_idx-1}...")

    # Create new cells
    intro_cell = new_markdown_cell(create_intro_markdown())
    widget_cell = new_code_cell(create_widget_code())

    # Insert cells
    nb.cells.insert(insert_idx, intro_cell)
    nb.cells.insert(insert_idx + 1, widget_cell)

    print(f"Saving to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Done!")

if __name__ == "__main__":
    inject_widgets("Chapter_11.ipynb", "Chapter_11.ipynb")
