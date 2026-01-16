
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell
import os

def create_dice_code():
    return """
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display

def dice_sim(n_rolls=100):
    # Simulate rolling two dice
    die1 = np.random.randint(1, 7, size=n_rolls)
    die2 = np.random.randint(1, 7, size=n_rolls)
    sums = die1 + die2
    
    # Analyze Frequency
    values, counts = np.unique(sums, return_counts=True)
    freqs = counts / n_rolls
    
    # Theoretical Probabilities
    # Sums: 2(1/36), 3(2/36), 4(3/36), 5(4/36), 6(5/36), 7(6/36), ...
    theoretical_probs = {
        2: 1/36, 3: 2/36, 4: 3/36, 5: 4/36, 6: 5/36, 
        7: 6/36, 8: 5/36, 9: 4/36, 10: 3/36, 11: 2/36, 12: 1/36
    }
    
    # Plotting
    plt.figure(figsize=(10, 6))
    
    # Bar Chart
    possible_sums = np.arange(2, 13)
    theory_vals = [theoretical_probs[s] for s in possible_sums]
    
    plt.bar(possible_sums - 0.2, theory_vals, width=0.4, label='Theoretical Probability', color='gray', alpha=0.6)
    plt.bar(values + 0.2, freqs, width=0.4, label=f'Simulated (n={n_rolls})', color='blue', alpha=0.8)
    
    plt.xticks(possible_sums)
    plt.xlabel('Sum of Two Dice')
    plt.ylabel('Probability')
    plt.title(f"Rolling Two Dice: Why is 7 Lucky?")
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    plt.show()

display(widgets.interactive(dice_sim, 
                            n_rolls=widgets.IntSlider(value=100, min=10, max=5000, step=10, description='Rolls:')))
"""

def create_intro_markdown():
    return """
### Interactive Experiment: The Sample Space of Dice

When we roll **one** die, every number (1-6) is equally likely (1/6).
But when we roll **two** dice and add them up, the sums are **NOT equally likely**.

**Explore:**
*   Why is **7** the most common number?
*   Why are **2** ("Snake Eyes") and **12** ("Boxcars") so rare?
*   Increase the number of rolls to see the "pyramid" shape of the probability distribution emerge.
"""

def inject_widgets(notebook_path, output_path):
    print(f"Reading {notebook_path}...")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Insert after "Formal Probability - Notation" (Cell 3)
    idx = -1
    for i, cell in enumerate(nb.cells):
        if "**<u>Formal Probability - Notation</u>**" in cell.source:
            idx = i + 1
            break
            
    if idx != -1:
        print(f"Injecting Dice Widget after cell {idx-1}...")
        nb.cells.insert(idx, new_markdown_cell(create_intro_markdown()))
        nb.cells.insert(idx + 1, new_code_cell(create_dice_code()))
    else:
        print("Warning: Target cell 'Notation' not found. Appending to end.")
        nb.cells.insert(4, new_markdown_cell(create_intro_markdown()))
        nb.cells.insert(5, new_code_cell(create_dice_code()))

    print(f"Saving to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Done!")

if __name__ == "__main__":
    inject_widgets("Chapter_13.ipynb", "Chapter_13.ipynb")
