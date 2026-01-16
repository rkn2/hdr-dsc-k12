
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell
import os

def create_widget_code():
    return """
import ipywidgets as widgets
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from IPython.display import display, clear_output

def draw_venn(p_a, p_b, p_and):
    # Sanity checks
    if p_and > p_a or p_and > p_b:
        print("Error: Intersection P(A and B) cannot be greater than P(A) or P(B).")
        return
    if (p_a + p_b - p_and) > 1.0:
        print("Error: Union P(A or B) cannot be greater than 1.")
        return

    # Calculations
    p_only_a = p_a - p_and
    p_only_b = p_b - p_and
    p_neither = 1.0 - (p_only_a + p_only_b + p_and)
    p_or = p_a + p_b - p_and
    
    # Conditional Probabilities
    p_a_given_b = p_and / p_b if p_b > 0 else 0
    p_b_given_a = p_and / p_a if p_a > 0 else 0
    
    # Independence Check
    independent = abs(p_a_given_b - p_a) < 0.01

    # Visualizing
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Draw Circles
    circle_a = patches.Circle((3.5, 3), 2, edgecolor='blue', facecolor='blue', alpha=0.3, label='A')
    circle_b = patches.Circle((6.5, 3), 2, edgecolor='red', facecolor='red', alpha=0.3, label='B')
    ax.add_patch(circle_a)
    ax.add_patch(circle_b)
    
    # Labels
    ax.text(2.5, 3, f"Only A\\n{p_only_a:.2f}", ha='center', va='center', weight='bold')
    ax.text(7.5, 3, f"Only B\\n{p_only_b:.2f}", ha='center', va='center', weight='bold')
    ax.text(5, 3, f"A & B\\n{p_and:.2f}", ha='center', va='center', weight='bold')
    ax.text(5, 0.5, f"Neither: {p_neither:.2f}", ha='center')
    
    # Text Report
    report = (
        f"P(A) = {p_a:.2f}, P(B) = {p_b:.2f}\\n"
        f"P(A or B) = {p_or:.2f}\\n"
        f"P(A | B) = {p_a_given_b:.2f}\\n"
        f"Independence Check: P(A|B) vs P(A)? {p_a_given_b:.2f} vs {p_a:.2f} -> {'Independent' if independent else 'Dependent'}"
    )
    ax.text(0, 5.5, report, fontsize=10, va='top', bbox=dict(facecolor='white', alpha=0.8))
    
    plt.title('Venn Diagram Visualization')
    plt.show()

# Controls
style = {'description_width': 'initial'}
p_a_slider = widgets.FloatSlider(value=0.5, min=0, max=1.0, step=0.01, description='P(A):', style=style)
p_b_slider = widgets.FloatSlider(value=0.4, min=0, max=1.0, step=0.01, description='P(B):', style=style)
p_and_slider = widgets.FloatSlider(value=0.2, min=0, max=1.0, step=0.01, description='P(A and B):', style=style)

ui = widgets.VBox([p_a_slider, p_b_slider, p_and_slider])
out = widgets.interactive_output(draw_venn, {'p_a': p_a_slider, 'p_b': p_b_slider, 'p_and': p_and_slider})

display(ui, out)
"""

def create_intro_markdown():
    return """
### Interactive Experiment: Visualizing Probability Rules

Use the tool below to explore how two events, **A** and **B**, interact.
*   **P(A)**: Probability of Event A happening.
*   **P(B)**: Probability of Event B happening.
*   **P(A and B)**: Probability of BOTH happening at the same time (Intersection).

The diagram helps you visualize:
*   **Union P(A or B):** Everything inside the circles.
*   **Intersection P(A and B):** The overlap.
*   **Conditional Probability P(A|B):** If we know we are in circle B, what portion of B is also A?
"""

def inject_widgets(notebook_path, output_path):
    print(f"Reading {notebook_path}...")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Find insertion point: After "Tables vs Venn Diagrams:" (Cell 7)
    insert_idx = -1
    for i, cell in enumerate(nb.cells):
        if "**<u>Tables vs Venn Diagrams:</u>**" in cell.source:
            insert_idx = i + 1
            break
    
    if insert_idx == -1:
        print("Warning: Target cell 'Tables vs Venn Diagrams' not found. Appending to end.")
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
    inject_widgets("Chapter_14.ipynb", "Chapter_14.ipynb")
