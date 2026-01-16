import nbformat
import os

def fix_perm_comb_widget():
    nb_path = 'Chapter_12.ipynb'
    if not os.path.exists(nb_path):
        print(f"Error: {nb_path} not found.")
        return

    print(f"Reading {nb_path}...")
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Find the cell with the Permutations vs Combinations widget
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code' and 'calculate_counts' in cell.source:
            print(f"Found widget at cell {i}, updating...")
            
            # New improved widget code
            new_code = """# @title Permutations vs. Combinations Explorer - Click 'Play' to Start

import ipywidgets as widgets
import math
from IPython.display import display, HTML, clear_output

# Output widget for results
output = widgets.Output()

def update_display(change):
    n = n_slider.value
    r = r_slider.value
    
    with output:
        clear_output(wait=True)
        
        # Validations
        if r > n:
            display(HTML("<div style='color:red; padding:10px; border:1px solid red; border-radius:5px;'><b>Error:</b> You cannot choose more items (r) than available options (n).</div>"))
            return
        
        # Calculations
        perm = math.perm(n, r)
        comb = math.comb(n, r)
        
        # Formatting output with HTML for clarity
        html_output = f\"\"\"
        <div style="border: 2px solid #4CAF50; padding: 15px; border-radius: 8px; background-color: #f9f9f9; margin-top:10px;">
            <h3 style="color: #4CAF50; margin-top:0;">Results for n={n}, r={r}</h3>
            
            <div style="background-color: #e8f5e9; padding: 10px; border-radius: 5px; margin: 10px 0;">
                <p style="margin:5px 0;"><b>🎯 Permutations (Order Matters):</b></p>
                <p style="margin:5px 0; padding-left:20px;"><i>Formula:</i> P(n, r) = n! / (n-r)!</p>
                <p style="margin:5px 0; padding-left:20px;"><i>Result:</i> <b style="color:#2e7d32; font-size:1.2em;">{perm:,}</b> different arrangements</p>
            </div>
            
            <div style="background-color: #fff3e0; padding: 10px; border-radius: 5px; margin: 10px 0;">
                <p style="margin:5px 0;"><b>🎲 Combinations (Order Doesn't Matter):</b></p>
                <p style="margin:5px 0; padding-left:20px;"><i>Formula:</i> C(n, r) = n! / (r!(n-r)!)</p>
                <p style="margin:5px 0; padding-left:20px;"><i>Result:</i> <b style="color:#e65100; font-size:1.2em;">{comb:,}</b> different selections</p>
            </div>
            
            <div style="background-color: #e3f2fd; padding: 10px; border-radius: 5px; margin: 10px 0;">
                <p style="margin:5px 0;"><b>💡 Key Insight:</b></p>
                <p style="margin:5px 0; padding-left:20px;">Permutations ≥ Combinations because "AB" and "BA" count as two different permutations but only one combination.</p>
                <p style="margin:5px 0; padding-left:20px;">Ratio: {perm/comb if comb > 0 else 0:.1f}x more permutations than combinations</p>
            </div>
        </div>
        \"\"\"
        display(HTML(html_output))

# Interactive controls
style = {'description_width': '150px'}
n_slider = widgets.IntSlider(
    value=5, 
    min=1, 
    max=20, 
    step=1, 
    description='Total Items (n):', 
    style=style,
    continuous_update=False
)
r_slider = widgets.IntSlider(
    value=3, 
    min=1, 
    max=20, 
    step=1, 
    description='Items to Choose (r):', 
    style=style,
    continuous_update=False
)

# Attach observers
n_slider.observe(update_display, names='value')
r_slider.observe(update_display, names='value')

# Display
display(widgets.VBox([
    widgets.HTML("<h4>Adjust the sliders to explore:</h4>"),
    n_slider, 
    r_slider,
    output
]))

# Initial display
update_display(None)
"""
            
            cell.source = new_code
            print("Widget code updated!")
            break

    print(f"Saving {nb_path}...")
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Done!")

if __name__ == "__main__":
    fix_perm_comb_widget()
