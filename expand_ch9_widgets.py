
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell
import os

# --- Widget 1: Sample Size Explorer ---
def create_sample_size_code():
    return """
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display

def plot_sample_size_demo(n):
    # True Population: Mean=50, Std=15
    pop_mean = 50
    pop_std = 15
    
    # Generate one sample of size n
    sample = np.random.normal(pop_mean, pop_std, n)
    sample_mean = np.mean(sample)
    
    # Generate history of means for plot (to show "settling")
    # We'll simulate increasing sample sizes up to n
    ns = np.arange(1, n + 1)
    # For speed, just plot the cumulative mean of this one large sample sequence
    # This mimics "adding more people to the sample"
    cumulative_means = np.cumsum(sample) / ns
    
    plt.figure(figsize=(10, 5))
    plt.plot(ns, cumulative_means, label='Sample Mean', color='blue')
    plt.axhline(pop_mean, color='red', linestyle='--', label=f'True Mean ({pop_mean})')
    
    plt.xlim(1, 1000)
    plt.ylim(30, 70)
    plt.xlabel('Sample Size (n)')
    plt.ylabel('Average Value')
    plt.title(f'Effect of Sample Size: Current Mean = {sample_mean:.2f} (n={n})')
    plt.legend()
    plt.grid(alpha=0.3)
    
    plt.show()

display(widgets.interactive(plot_sample_size_demo, 
                            n=widgets.IntSlider(value=10, min=2, max=1000, step=10, description='Sample Size:')))
"""

def create_sample_size_intro():
    return """
### Interactive Experiment: The Power of Sample Size

One of the key ideas in sampling is that **size matters**.
*   A small sample (e.g., asking 5 people) can yield results very far from the truth just by random chance.
*   A large sample (e.g., asking 500 people) tends to be much closer to the truth.

**Try it:**
Move the slider to increase the **Sample Size ($n$)**.
Notice how the blue line (your sample average) swings wildly at the beginning but "settles down" near the red line (the true population average) as $n$ gets larger.
"""

# --- Widget 2: Sampling Methods Visualizer ---
def create_method_viz_code():
    return """
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

def plot_sampling_method(method):
    # Population: 10x10 Grid
    # Setup Strata: Left half (Red), Right half (Blue)
    # Setup Clusters: 4 quadrants (Top-Left, Top-Right, Bot-Left, Bot-Right)
    
    n_points = 100
    cols = 10
    rows = 10
    
    x = np.tile(np.arange(cols), rows)
    y = np.repeat(np.arange(rows), cols)
    colors = ['red' if c < 5 else 'blue' for c in x] # Strata colors
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Base Plot: All points faded
    ax.scatter(x, y, c=colors, s=50, alpha=0.2)
    
    start_idx = 0 # For systematic
    
    selected_indices = []
    
    if method == 'Simple Random Sample (SRS)':
        # Pick 20 random points
        selected_indices = np.random.choice(range(n_points), 20, replace=False)
        title = "SRS: Every individual has equal chance."
        
    elif method == 'Stratified':
        # Pick 10 from Red (Left), 10 from Blue (Right)
        red_indices = [i for i, c in enumerate(x) if c < 5]
        blue_indices = [i for i, c in enumerate(x) if c >= 5]
        sel_red = np.random.choice(red_indices, 10, replace=False)
        sel_blue = np.random.choice(blue_indices, 10, replace=False)
        selected_indices = np.concatenate([sel_red, sel_blue])
        title = "Stratified: Slice population into groups (Strata), sample from EACH group."
        
        # Draw Divider
        ax.axvline(4.5, color='black', linestyle='--')
        ax.text(2, -1, "Stratum 1", ha='center')
        ax.text(7, -1, "Stratum 2", ha='center')

    elif method == 'Cluster':
        # Clusters: 0:TL, 1:TR, 2:BL, 3:BR. Pick 1 random cluster.
        # TL: x<5, y>=5. TR: x>=5, y>=5. BL: x<5, y<5. BR: x>=5, y<5
        clusters = {0: [], 1: [], 2: [], 3: []}
        for i in range(n_points):
            if x[i]<5 and y[i]>=5: clusters[0].append(i)
            elif x[i]>=5 and y[i]>=5: clusters[1].append(i)
            elif x[i]<5 and y[i]<5: clusters[2].append(i)
            elif x[i]>=5 and y[i]<5: clusters[3].append(i)
            
        chosen_cluster = np.random.choice([0, 1, 2, 3])
        selected_indices = clusters[chosen_cluster]
        title = "Cluster: Split into groups, pick the WHOLE group."
        
        # Draw Cluster boxes
        rects = [
            patches.Rectangle((-0.5, 4.5), 5, 5, fill=False, edgecolor='green', lw=2), # TL
            patches.Rectangle((4.5, 4.5), 5, 5, fill=False, edgecolor='green', lw=2),  # TR
            patches.Rectangle((-0.5, -0.5), 5, 5, fill=False, edgecolor='green', lw=2),# BL
            patches.Rectangle((4.5, -0.5), 5, 5, fill=False, edgecolor='green', lw=2)  # BR
        ]
        # Highlight chosen
        rects[chosen_cluster].set_edgecolor('black')
        rects[chosen_cluster].set_linewidth(4)
        for r in rects: ax.add_patch(r)

    elif method == 'Systematic':
        # Pick every 5th person
        start = np.random.randint(0, 5)
        selected_indices = np.arange(start, n_points, 5)
        title = f"Systematic: Start at {start}, pick every 5th person."
        
        # Draw path
        # Connect dots to show order? Maybe too messy.
        
    # Plot Selected (Dark Mode)
    if len(selected_indices) > 0:
        sel_x = x[selected_indices]
        sel_y = y[selected_indices]
        sel_c = np.array(colors)[selected_indices]
        ax.scatter(sel_x, sel_y, c=sel_c, s=150, edgecolor='black', zorder=10)
    
    ax.set_title(title, fontsize=12)
    ax.axis('off')
    plt.show()

# Dropdown
style = {'description_width': 'initial'}
method_dropdown = widgets.Dropdown(
    options=['Simple Random Sample (SRS)', 'Stratified', 'Cluster', 'Systematic'],
    value='Simple Random Sample (SRS)',
    description='Method:',
    style=style,
    layout={'width': '400px'}
)

display(widgets.interactive(plot_sampling_method, method=method_dropdown))
"""

def create_method_intro():
    return """
### Interactive Experiment: Visualizing Sampling Methods

It's easy to confuse the definitions of different sampling strategies. Use the tool below to **visualize** the difference.
*   **SRS:** Pure chaos (random).
*   **Stratified:** We force fairness (e.g., ensure we get some Red and some Blue points).
*   **Cluster:** We save money/time by grabbing a whole "clump" (e.g., surveying everyone in one randomly selected classroom).
*   **Systematic:** We follow a rule (e.g., every 5th person).
"""

def inject_widgets(notebook_path, output_path):
    print(f"Reading {notebook_path}...")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # --- Injection 1: Sample Size (After 'Idea 3') ---
    idx1 = -1
    for i, cell in enumerate(nb.cells):
        if "**<span class=\"mark\">Idea 3: It's the Sample Size</span>**" in cell.source or "Idea 3" in cell.source:
            idx1 = i + 1
            break
            
    if idx1 != -1:
        print(f"Injecting Sample Size Widget after cell {idx1-1}...")
        nb.cells.insert(idx1, new_markdown_cell(create_sample_size_intro()))
        nb.cells.insert(idx1 + 1, new_code_cell(create_sample_size_code()))
    else:
        print("Warning: Could not find 'Idea 3' location.")

    # --- Injection 2: Sampling Methods (After 'Systematic Sample') ---
    # Since we modified the list by inserting 2 cells, we must re-search or offset.
    # Re-searching is safer.
    idx2 = -1
    for i, cell in enumerate(nb.cells):
        if "Systematic Sample" in cell.source and "Selected systematically" not in cell.source: 
            # Header usually has bold or mark
            idx2 = i + 1
            break
    
    # If not found, look for "Sampling Methods - Videos" to insert BEFORE it
    if idx2 == -1:
         for i, cell in enumerate(nb.cells):
            if "Sampling Methods - Videos" in cell.source:
                idx2 = i
                break
                
    if idx2 != -1:
        print(f"Injecting Sampling Methods Widget at cell {idx2}...")
        nb.cells.insert(idx2, new_markdown_cell(create_method_intro()))
        nb.cells.insert(idx2 + 1, new_code_cell(create_method_viz_code()))
    else:
        print("Warning: Could not find 'Systematic Sample' location.")

    print(f"Saving to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Done!")

if __name__ == "__main__":
    inject_widgets("Chapter_9.ipynb", "Chapter_9.ipynb")
