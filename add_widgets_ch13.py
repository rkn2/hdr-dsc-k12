
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell
import os

def create_widget_code():
    return """
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display, clear_output

def run_traffic_simulation(p_green, p_yellow, n_trials):
    # Calculate P(Red) ensuring sum is 1.0 (handling float precision)
    p_red = 1.0 - (p_green + p_yellow)
    
    if p_red < 0:
        print("Error: Probabilities cannot sum to more than 1. Please reduce Green or Yellow.")
        return

    # Define states and probabilities
    states = ['Green', 'Yellow', 'Red']
    probs = [p_green, p_yellow, p_red]
    colors = ['green', 'yellow', 'red']
    
    # Simulate
    results = np.random.choice(states, size=n_trials, p=probs)
    
    # Count occurrences
    counts = {state: np.sum(results == state) for state in states}
    empirical_probs = [counts[s]/n_trials for s in states]
    
    # Plotting
    plt.figure(figsize=(10, 6))
    
    # Theoretical Bars
    plt.bar([x - 0.2 for x in range(3)], probs, width=0.4, label='Theoretical Probability', color='lightgray', alpha=0.8)
    
    # Empirical Bars
    plt.bar([x + 0.2 for x in range(3)], empirical_probs, width=0.4, label=f'Observed Frequency (n={n_trials})', color=colors, alpha=0.7, edgecolor='black')
    
    plt.xticks(range(3), states)
    plt.ylabel('Probability / Frequency')
    plt.ylim(0, 1.0)
    plt.title(f'Traffic Light Simulation: {n_trials} Trials')
    plt.legend()
    
    # Text statistics
    stats_text = (
        f"Theoretical: G={p_green:.2f}, Y={p_yellow:.2f}, R={p_red:.2f} (Sum={sum(probs):.2f})\\n"
        f"Observed:    G={empirical_probs[0]:.2f}, Y={empirical_probs[1]:.2f}, R={empirical_probs[2]:.2f}"
    )
    plt.text(0.5, -0.15, stats_text, ha='center', transform=plt.gca().transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
    
    plt.grid(axis='y', alpha=0.3)
    plt.show()

# Controls
style = {'description_width': 'initial'}
p_green_slider = widgets.FloatSlider(value=0.35, min=0, max=1.0, step=0.05, description='P(Green):', style=style)
p_yellow_slider = widgets.FloatSlider(value=0.05, min=0, max=1.0, step=0.05, description='P(Yellow):', style=style)
n_trials_slider = widgets.IntSlider(value=100, min=10, max=1000, step=10, description='Number of Drivers:', style=style)

def update_ui(change):
    # Ensure P(Green) + P(Yellow) <= 1
    if p_green_slider.value + p_yellow_slider.value > 1.0:
        # Adjust yellow to fit if possible, or green
        if change['owner'] == p_green_slider:
            p_yellow_slider.value = max(0, 1.0 - p_green_slider.value)
        else:
            p_green_slider.value = max(0, 1.0 - p_yellow_slider.value)

p_green_slider.observe(update_ui, names='value')
p_yellow_slider.observe(update_ui, names='value')

ui = widgets.VBox([p_green_slider, p_yellow_slider, n_trials_slider])
out = widgets.interactive_output(run_traffic_simulation, {'p_green': p_green_slider, 'p_yellow': p_yellow_slider, 'n_trials': n_trials_slider})

display(ui, out)
"""

def create_intro_markdown():
    return """
### Interactive Experiment: The Traffic Light Model

Probability describes the long-run frequency of an event. A legitimate probability model must satisfy two rules:
1.  Any probability is a number between 0 and 1.
2.  The sum of logical outcomes must equal 1.

**Scenario:** You are approaching a traffic light.
Use the sliders below to set the probabilities for Green and Yellow lights. The probability of Red is calculated automatically to ensure the sum is 1.
Simulate many drivers arriving at the light and compare the **Observed Frequency** (bars) with the **Theoretical Probability** (gray shadow).
"""

def inject_widgets(notebook_path, output_path):
    print(f"Reading {notebook_path}...")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Find insertion point: After "Examples:" section (Cell 7)
    insert_idx = -1
    for i, cell in enumerate(nb.cells):
        if "**<u>Examples:</u>**" in cell.source:
            insert_idx = i + 1
            break
    
    if insert_idx == -1:
        print("Warning: Target cell 'Examples' not found. Appending to end.")
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
    inject_widgets("Chapter_13.ipynb", "Chapter_13.ipynb")
