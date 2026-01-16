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
        if cell.cell_type == 'code' and 'Permutations vs. Combinations Explorer' in cell.source:
            print(f"Found widget at cell {i}, updating...")
            
            # Simpler, more reliable widget code
            new_code = """# @title Permutations vs. Combinations Explorer - Click 'Play' to Start

import ipywidgets as widgets
import math
from IPython.display import display, HTML

def show_results(n, r):
    # Validations
    if r > n:
        return HTML("<div style='color:red; padding:10px; border:1px solid red; border-radius:5px;'><b>Error:</b> You cannot choose more items (r) than available options (n).</div>")
    
    # Calculations
    perm = math.perm(n, r)
    comb = math.comb(n, r)
    ratio = perm / comb if comb > 0 else 0
    
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
            <p style="margin:5px 0; padding-left:20px;">Ratio: {ratio:.1f}x more permutations than combinations</p>
        </div>
    </div>
    \"\"\"
    return HTML(html_output)

# Interactive controls
style = {'description_width': '150px'}
n_slider = widgets.IntSlider(
    value=5, 
    min=1, 
    max=20, 
    step=1, 
    description='Total Items (n):', 
    style=style
)
r_slider = widgets.IntSlider(
    value=3, 
    min=1, 
    max=20, 
    step=1, 
    description='Items to Choose (r):', 
    style=style
)

# Use interact for automatic display
widgets.interact(show_results, n=n_slider, r=r_slider)
"""
            
            cell.source = new_code
            print("Widget code updated to simpler version!")
            break

    print(f"Saving {nb_path}...")
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Done!")

if __name__ == "__main__":
    fix_perm_comb_widget()
