
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

def simulate_ci(n, p, confidence_level):
    n_sims = 100
    
    # Generate simulations
    # X ~ Binomial(n, p)
    x = np.random.binomial(n, p, n_sims)
    p_hats = x / n
    
    # Calculate intervals
    z_score = stats.norm.ppf(1 - (1 - confidence_level)/2)
    std_errors = np.sqrt(p_hats * (1 - p_hats) / n)
    margins_of_error = z_score * std_errors
    
    lower_bounds = p_hats - margins_of_error
    upper_bounds = p_hats + margins_of_error
    
    # Check capture
    captured = (lower_bounds <= p) & (upper_bounds >= p)
    capture_rate = np.mean(captured)
    
    # Plotting
    plt.figure(figsize=(12, 6))
    
    # Plot intervals
    for i in range(n_sims):
        color = 'green' if captured[i] else 'red'
        plt.plot([i, i], [lower_bounds[i], upper_bounds[i]], color=color, alpha=0.6)
        plt.plot(i, p_hats[i], 'o', color=color, markersize=3)
        
    plt.axhline(p, color='black', linestyle='--', linewidth=2, label=f'True p = {p}')
    
    plt.title(f'Confidence Interval Simulation (n={n}, p={p}, Confidence={confidence_level:.0%})\\nCapture Rate: {capture_rate:.0%}')
    plt.xlabel('Simulation Number (1-100)')
    plt.ylabel('Proportion')
    plt.ylim(max(0, p - 0.2), min(1, p + 0.2))
    plt.legend()
    plt.grid(alpha=0.2)
    
    # Highlighting 'Red' intervals
    if not all(captured):
        plt.text(0.5, 0.05, f"Red lines missed the true parameter!", ha='center', transform=plt.gca().transAxes, color='red')
        
    plt.show()

# Controls
style = {'description_width': 'initial'}
n_slider = widgets.IntSlider(value=50, min=10, max=500, step=10, description='Sample Size (n):', style=style)
p_slider = widgets.FloatSlider(value=0.5, min=0.1, max=0.9, step=0.05, description='True Prop (p):', style=style)
conf_dropdown = widgets.Dropdown(options=[0.90, 0.95, 0.99], value=0.95, description='Confidence Level:', style=style)

ui = widgets.VBox([widgets.HBox([n_slider, p_slider]), conf_dropdown])
out = widgets.interactive_output(simulate_ci, {'n': n_slider, 'p': p_slider, 'confidence_level': conf_dropdown})

display(ui, out)
"""

def create_intro_markdown():
    return """
### Interactive Experiment: What does "95% Confidence" Mean?

A Confidence Interval (CI) is a range of values calculated from sample data that is likely to cover the true population parameter.
But what does "95% confident" actually mean?

It means that if we took many, many samples and calculated a CI for each one, about **95% of those intervals would capture the true parameter**.

**Explore:**
*   The **Black Dashed Line** is the **True Parameter ($p$)**. We (the simulators) know it, but the intervals don't!
*   **Green Lines**: Intervals that successfully "captured" the true $p$.
*   **Red Lines**: Intervals that missed.
*   Change the **Confidence Level** to 90% or 99% and see how the width of the intervals changes, and how many red lines appear.
"""

def inject_widgets(notebook_path, output_path):
    print(f"Reading {notebook_path}...")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Find insertion point: At the end, since the file seems heavily summarized or the topic is the finale.
    # Or try to find "Confidence Interval" definition.
    insert_idx = -1
    for i, cell in enumerate(nb.cells):
        if "Confidence Interval" in cell.source or "interval" in cell.source.lower():
            insert_idx = i + 1 
            # Keep searching for the LAST occurrence or best spot? 
            # Actually, insert at the end is safest for a "Review/Explore" widget if structure is unclear.
    
    if insert_idx == -1:
        print("Warning: Content unclear. Appending to end.")
        insert_idx = len(nb.cells)
    else:
        # If we found it, insert after. But if there are multiple, maybe the last one?
        # Let's just append to end for this one to ensure it doesn't break flow mid-sentence.
        pass

    # For Ch 16, appending to end is a good strategy as it summarizes the chapter.
    insert_idx = len(nb.cells)
    
    print(f"Inserting widgets at cell {insert_idx} (End of notebook)...")

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
    inject_widgets("Chapter_16.ipynb", "Chapter_16.ipynb")
