import nbformat
import random

def add_widgets():
    nb_path = 'Chapter_9.ipynb'
    try:
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
    except FileNotFoundError:
        print(f"Error: Could not find {nb_path}")
        return

    # 1. Define the Widget Code
    widget_code = """import matplotlib.pyplot as plt
import numpy as np
import ipywidgets as widgets
from IPython.display import display

# Generate Population Data (once)
np.random.seed(42)
population_size = 1000
# True Population: Average height 170cm, std dev 10cm
true_mean = 170
population = np.random.normal(true_mean, 10, population_size)

# Create a "Biased" sub-group (e.g., Basketball team members are taller)
# Let's say people > 185cm are more likely to be in the "Convenience" location
bias_weight = (population - 150) / 50 
bias_probs = np.exp(bias_weight) / np.sum(np.exp(bias_weight))

def run_sampling_sim(sample_method, sample_size):
    plt.figure(figsize=(10, 6))
    
    # 1. Plot Population Distribution (Grey background)
    plt.hist(population, bins=30, alpha=0.3, color='grey', label='Full Population (Ground Truth)', density=True)
    plt.axvline(true_mean, color='black', linestyle='--', linewidth=2, label=f'True Mean ({true_mean:.1f} cm)')
    
    # 2. Draw Sample
    if sample_method == 'Simple Random Sample (SRS)':
        # Every individual has equal chance
        sample_data = np.random.choice(population, size=sample_size, replace=False)
        color = 'blue'
        title_extra = "unbiased"
    else: # Convenience Sample (Biased)
        # Taller people are more likely to be selected
        sample_data = np.random.choice(population, size=sample_size, replace=False, p=bias_probs)
        color = 'red'
        title_extra = "BIASED towards tall people"

    # 3. Plot Sample Distribution
    sample_mean = np.mean(sample_data)
    plt.hist(sample_data, bins=15, alpha=0.7, color=color, label=f'Your Sample (n={sample_size})', density=True)
    plt.axvline(sample_mean, color=color, linestyle='-', linewidth=3, label=f'Sample Mean ({sample_mean:.1f} cm)')
    
    plt.title(f"Sampling Method: {sample_method}\\nSample Average: {sample_mean:.1f} cm (True: {true_mean:.1f} cm)", fontsize=14)
    plt.xlabel("Height (cm)")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Educational Note
    if sample_method != 'Simple Random Sample (SRS)' and abs(sample_mean - true_mean) > 5:
        plt.text(140, 0.04, "Notice: Bias pushes the\\nresult away from truth!", 
                 color='red', fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
        if sample_size > 200:
             plt.text(140, 0.02, "Even a LARGE biased sample\\nis still WRONG!", 
                 color='darkred', fontsize=12, fontweight='bold', bbox=dict(facecolor='white', alpha=0.8))

    plt.show()

# UI Elements
style = {'description_width': 'initial'}
method_dropdown = widgets.Dropdown(
    options=['Simple Random Sample (SRS)', 'Convenience Sample (Basketball Court)'],
    value='Simple Random Sample (SRS)',
    description='Sampling Method:',
    style=style,
    layout=widgets.Layout(width='400px')
)

size_slider = widgets.IntSlider(
    value=50,
    min=10,
    max=500,
    step=10,
    description='Sample Size (n):',
    style=style
)

ui = widgets.VBox([method_dropdown, size_slider])
out = widgets.interactive_output(run_sampling_sim, {'sample_method': method_dropdown, 'sample_size': size_slider})

display(widgets.HTML("<h3>Experiment: Random vs. Biased Sampling</h3>"))
display(widgets.HTML("<b>Goal:</b> Estimate the average height of the population."))
display(ui, out)
"""

    # 2. Define the Markdown Context (Instruction)
    markdown_intro = """### 🧪 Interactive Experiment: The Danger of Bias

**Bias** is a systematic error. It's not just "bad luck" — it's like a scale that is always 5 pounds off. 

In this simulation, we know the **True Population Mean** height is **170 cm**.
Try the two different sampling methods:

1.  **Simple Random Sample (SRS):** Everyone has an equal chance. 
    *   *Try changing the sample size.* Does the Sample Mean stay close to the True Mean?
2.  **Convenience Sample:** Imagine you only measure people currently playing basketball.
    *   *What happens to the Sample Mean?*
    *   *Does increasing the sample size fix the error?* (Hint: NO!)
"""

    # 3. Insert into Notebook
    # We look for the cell discussing "Bias occurs when"
    target_text = "Bias** occurs when"
    
    new_cells = [
        nbformat.v4.new_markdown_cell(markdown_intro),
        nbformat.v4.new_code_cell(widget_code)
    ]
    
    insert_idx = -1
    for idx, cell in enumerate(nb.cells):
        if cell.cell_type == 'markdown' and target_text in cell.source:
            insert_idx = idx + 1 # Insert AFTER this cell
            break
            
    if insert_idx != -1:
        # Check if we already inserted it to avoid duplicates
        if insert_idx < len(nb.cells) and "Interactive Experiment: The Danger of Bias" in nb.cells[insert_idx].source:
            print("Widget already appears to be present.")
        else:
            nb.cells[insert_idx:insert_idx] = new_cells
            print(f"Inserted widget at index {insert_idx}")
            
            # Save
            with open(nb_path, 'w', encoding='utf-8') as f:
                nbformat.write(nb, f)
            print("Notebook saved.")
    else:
        print("Target text not found. Appending to end (fallback).")
        nb.cells.extend(new_cells)
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)

if __name__ == "__main__":
    add_widgets()
