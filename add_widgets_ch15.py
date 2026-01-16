
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell
import os

def create_widget_code():
    return """
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from IPython.display import display, clear_output

def plot_binomial_normal(n, p):
    # Binomial Data
    k = np.arange(0, n + 1)
    binomial_probs = stats.binom.pmf(k, n, p)
    
    # Normal Approximation
    mean = n * p
    std_dev = np.sqrt(n * p * (1 - p))
    x = np.linspace(0, n, 1000)
    normal_curve = stats.norm.pdf(x, mean, std_dev)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(k, binomial_probs, color='skyblue', label=f'Binomial({n}, {p})', alpha=0.7)
    plt.plot(x, normal_curve, color='red', linewidth=2, label=f'Normal Approx ($\\mu$={mean:.1f}, $\\sigma$={std_dev:.1f})')
    
    plt.title(f'Binomial Model vs. Normal Approximation (n={n}, p={p})')
    plt.xlabel('Number of Successes (k)')
    plt.ylabel('Probability')
    plt.legend()
    plt.grid(alpha=0.3)
    
    # Rule of Thumb Check
    np_val = n * p
    nq_val = n * (1 - p)
    is_good = np_val >= 10 and nq_val >= 10
    
    status_color = 'green' if is_good else 'orange'
    status_text = f"np = {np_val:.1f}, nq = {nq_val:.1f} -> {'Approximation is Good (>=10)' if is_good else 'Approximation may be Poor (<10)'}"
    
    plt.text(0.5, -0.15, status_text, ha='center', transform=plt.gca().transAxes, fontsize=12, color='black', 
             bbox=dict(facecolor=status_color, alpha=0.2))
    
    plt.show()

# Controls
style = {'description_width': 'initial'}
n_slider = widgets.IntSlider(value=20, min=5, max=500, step=5, description='Trials (n):', style=style)
p_slider = widgets.FloatSlider(value=0.5, min=0.01, max=0.99, step=0.01, description='Probability (p):', style=style)

ui = widgets.VBox([n_slider, p_slider])
out = widgets.interactive_output(plot_binomial_normal, {'n': n_slider, 'p': p_slider})

display(ui, out)
"""

def create_intro_markdown():
    return """
### Interactive Experiment: Normal Approximation of the Binomial

Binomial calculations can be tedious for large $n$. Fortunately, as the number of trials ($n$) increases, the Binomial distribution often starts to look like a **Normal Distribution**.

**Rule of Thumb:**
The Normal model is a good approximation if we expect at least 10 successes ($np \ge 10$) and at least 10 failures ($nq \ge 10$).

**Explore:**
*   Increase **$n$** and watch the blue bars fit the red curve better.
*   Change **$p$** to extreme values (near 0 or 1) and see how you need a much larger $n$ for the approximation to work.
"""

def inject_widgets(notebook_path, output_path):
    print(f"Reading {notebook_path}...")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Find insertion point: Before "Normal Approximation for the Binomial Model:" (Cell 6 or similar)
    insert_idx = -1
    for i, cell in enumerate(nb.cells):
        if "**<u>Normal Approximation" in cell.source:
            insert_idx = i # Insert BEFORE this header
            break
    
    if insert_idx == -1:
        print("Warning: Target cell 'Normal Approximation' not found. Appending to end.")
        insert_idx = len(nb.cells)
    else:
        print(f"Inserting widgets before cell {insert_idx}...")

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
    inject_widgets("Chapter_15.ipynb", "Chapter_15.ipynb")
