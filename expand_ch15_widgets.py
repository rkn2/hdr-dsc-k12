
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell
import os

def create_geometric_code():
    return """
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from IPython.display import display

def plot_geometric(p=0.2):
    # Geometric: P(X=k) = (1-p)^(k-1) * p
    # Waiting until the k-th trial for the first success
    
    k_values = np.arange(1, 21)
    probs = stats.geom.pmf(k_values, p)
    
    mean_wait = 1/p
    
    plt.figure(figsize=(10, 5))
    bars = plt.bar(k_values, probs, color='orange', alpha=0.7)
    
    plt.title(f'Geometric Distribution (p={p})\\nExpected Wait Time E(X) = 1/p = {mean_wait:.1f} trials')
    plt.xlabel('Number of Trials to get First Success')
    plt.ylabel('Probability')
    plt.xticks(k_values)
    plt.grid(axis='y', alpha=0.3)
    
    plt.axvline(mean_wait, color='blue', linestyle='--', label=f'Expected Wait ({mean_wait:.1f})')
    plt.legend()
    
    plt.show()

display(widgets.interactive(plot_geometric, 
                            p=widgets.FloatSlider(value=0.2, min=0.05, max=0.9, step=0.05, description='Prob of Success (p):')))
"""

def create_intro_markdown():
    return """
### Interactive Experiment: The Waiting Game (Geometric Model)

While the **Binomial** model counts successes in a fixed number of trials, the **Geometric** model counts how many trials it takes to get **one** success.

*   **Example:** How many times do I have to roll a die until I get a 6? (p = 1/6 $\\approx$ 0.17)
*   **Explore:** Change $p$ and see how the "Wait Time" changes. If $p$ is small, you might wait a long time!
"""

def inject_widgets(notebook_path, output_path):
    print(f"Reading {notebook_path}...")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Insert after "Bernoulli Trials:" (Cell 3)
    idx = -1
    for i, cell in enumerate(nb.cells):
        if "**<u>Bernoulli Trials:</u>**" in cell.source:
            idx = i + 1
            break
            
    if idx != -1:
        print(f"Injecting Geometric Widget after cell {idx-1}...")
        nb.cells.insert(idx, new_markdown_cell(create_intro_markdown()))
        nb.cells.insert(idx + 1, new_code_cell(create_geometric_code()))
    else:
        print("Warning: Target cell 'Bernoulli' not found. Appending before Binomial.")
        for i, cell in enumerate(nb.cells):
            if "Binomial Model" in cell.source:
                idx = i
                break
        if idx != -1:
             nb.cells.insert(idx, new_markdown_cell(create_intro_markdown()))
             nb.cells.insert(idx+1, new_code_cell(create_geometric_code()))
        else:
             idx = 3 # Guess
             nb.cells.insert(idx, new_markdown_cell(create_intro_markdown()))
             nb.cells.insert(idx+1, new_code_cell(create_geometric_code()))

    print(f"Saving to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Done!")

if __name__ == "__main__":
    inject_widgets("Chapter_15.ipynb", "Chapter_15.ipynb")
