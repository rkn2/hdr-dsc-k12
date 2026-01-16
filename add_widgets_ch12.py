
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell
import os

def create_widget_code():
    return """
import ipywidgets as widgets
import math
from IPython.display import display, HTML

def calculate_counts(n, r):
    # Validations
    if r > n:
        return "<div style='color:red;'><b>Error:</b> You cannot choose more items (r) than valid options (n).</div>"
    
    # Calculations
    perm = math.perm(n, r)
    comb = math.comb(n, r)
    
    # Formatting output with HTML for clarity
    html_output = f\"\"\"
    <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; background-color: #f9f9f9;">
        <h3>Results for n={n}, r={r}</h3>
        <p><b>1. Fundamental Counting Principle (Permutations) - Order Matters:</b><br>
        <i>Equation:</i> $P(n, r) = \\frac{{n!}}{{(n-r)!}}$<br>
        <i>Calculation:</i> {perm:,} different ways.</p>
        <hr>
        <p><b>2. Combinations - Order Does NOT Matter:</b><br>
        <i>Equation:</i> $C(n, r) = \\frac{{n!}}{{r!(n-r)!}}$<br>
        <i>Calculation:</i> {comb:,} different ways.</p>
        <hr>
        <p><b>Key Insight:</b><br>
        Permutations are always greater than or equal to Combinations because "AB" and "BA" count as two different permutations but only one combination.</p>
    </div>
    \"\"\"
    return HTML(html_output)

# Interactive controls
style = {'description_width': 'initial'}
n_slider = widgets.IntSlider(value=5, min=1, max=20, step=1, description='Total Items (n):', style=style)
r_slider = widgets.IntSlider(value=3, min=1, max=20, step=1, description='Items to Choose (r):', style=style)

ui = widgets.VBox([n_slider, r_slider])
out = widgets.interactive_output(calculate_counts, {'n': n_slider, 'r': r_slider})

display(ui, out)
"""

def create_intro_markdown():
    return """
### Interactive Experiments: Permutations vs. Combinations

Understanding the difference between **Order Matters** (Permutations) and **Order Doesn't Matter** (Combinations) is crucial.

**Scenario: The Pizza Shop**
Imagine you are ordering a pizza.
*   **n (Total Items):** The number of toppings available at the shop (e.g., Pepperoni, Mushrooms, Onions, etc.).
*   **r (Items to Choose):** The number of toppings you want on your pizza.

**Explore:**
*   Does the order of toppings matter? (Is a "Pepperoni & Mushroom" pizza different from a "Mushroom & Pepperoni" pizza?) -> **Combination**.
*   What if we were assigning specific awards (1st place, 2nd place, 3rd place) to people? -> **Permutation**.

Use the tool below to see how the number of possibilities grows as you add more items.
"""

def inject_widgets(notebook_path, output_path):
    print(f"Reading {notebook_path}...")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Find insertion point: After "Combinations" section (Cell 8)
    # We look for the cell containing "**Combinations** are the number"
    insert_idx = -1
    for i, cell in enumerate(nb.cells):
        if "**Combinations** are the number" in cell.source:
            insert_idx = i + 1
            break
    
    if insert_idx == -1:
        print("Warning: Target cell 'Combinations' not found. Appending to end.")
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
    inject_widgets("Chapter_12.ipynb", "Chapter_12.ipynb")
