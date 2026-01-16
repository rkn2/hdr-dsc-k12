
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell
import os

def create_me_code():
    return """
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from IPython.display import display

def plot_margin_of_error(n, conf_level):
    # Calculate Z score
    alpha = 1 - conf_level
    z_score = stats.norm.ppf(1 - alpha/2)
    
    # Assume p_hat = 0.5 (worst case / most conservative)
    p_hat = 0.5
    
    # ME Formula: ME = z * sqrt(p(1-p)/n)
    me = z_score * np.sqrt((p_hat * (1 - p_hat)) / n)
    
    # Create Tug of War Plot
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Plot ME as a horizontal bar centered at 0
    ax.barh(0, 2*me, height=0.5, left=-me, color='purple', alpha=0.6, label='Confidence Interval Width')
    ax.barh(0, 0.005, height=0.6, left=-0.0025, color='black') # Center point
    
    ax.set_xlim(-0.2, 0.2)
    ax.set_ylim(-1, 1)
    ax.set_yticks([])
    ax.set_xlabel('Error from True Proportion')
    ax.set_title(f"Margin of Error (ME) = ±{me:.3f} ({me:.1%})\\nSample Size n={n}, Confidence={conf_level:.0%}")
    
    # Add Text Annotations
    ax.text(0, -0.6, f"Interval Width: {2*me:.3f}", ha='center')
    ax.text(-me, 0.3, f"-{me:.3f}", ha='center')
    ax.text(me, 0.3, f"+{me:.3f}", ha='center')
    
    ax.grid(axis='x', alpha=0.3)
    plt.show()

# Controls
style = {'description_width': 'initial'}
n_slider = widgets.IntSlider(value=100, min=10, max=2000, step=10, description='Sample Size (n):', style=style)
conf_slider = widgets.FloatSlider(value=0.95, min=0.80, max=0.999, step=0.005, description='Confidence Level:', style=style)

display(widgets.interactive(plot_margin_of_error, n=n_slider, conf_level=conf_slider))
"""

def create_intro_markdown():
    return """
### Interactive Experiment: The Margin of Error Tug-of-War

Constructing a Confidence Interval is a trade-off.
*   We want to be **Confident** (High Confidence Level) $\\rightarrow$ This makes the interval **Wider** (Larger ME).
*   We want to be **Precise** (Small Margin of Error) $\\rightarrow$ This requires a **Larger Sample Size ($n$)**.

**Explore:**
*   Increase $n$ and watch the purple bar shrink (more precise).
*   Increase Confidence (e.g., to 99.9%) and watch the bar grow (less precise, but "safer").
"""

def inject_widgets(notebook_path, output_path):
    print(f"Reading {notebook_path}...")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Insert after "Key Vocabulary" (Cell 4)
    idx = -1
    for i, cell in enumerate(nb.cells):
        if "**Key Vocabulary:**" in cell.source:
            idx = i + 1
            break
            
    if idx != -1:
        print(f"Injecting ME Widget after cell {idx-1}...")
        nb.cells.insert(idx, new_markdown_cell(create_intro_markdown()))
        nb.cells.insert(idx + 1, new_code_cell(create_me_code()))
    else:
        print("Warning: Target cell 'Vocabulary' not found. Appending to end.")
        idx = len(nb.cells)
        nb.cells.insert(idx, new_markdown_cell(create_intro_markdown()))
        nb.cells.insert(idx + 1, new_code_cell(create_me_code()))

    print(f"Saving to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Done!")

if __name__ == "__main__":
    inject_widgets("Chapter_16.ipynb", "Chapter_16.ipynb")
