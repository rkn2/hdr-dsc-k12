
import nbformat
from nbformat.v4 import new_markdown_cell
import re

def create_styled_cereal_content():
    # Based on standard stats curriculum (e.g. TPS/BVD), the Cereal box problem usually is:
    # 20% Tiger (0,1), 30% Serena (2,3,4), 50% Danica (5,6,7,8,9)
    # The string seen "89064| 2730|8 64568 1|41"
    # Let's verify typical mapping.
    # 8(D), 9(D), 0(T), 6(D), 4(S) -> D, D, T, D, S (Collected all 3?)
    
    # Let's create a visual mapping key first.
    key_html = """
    <div style="background-color: #f9f9f9; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
        <strong>Component Model (Key):</strong>
        <ul>
            <li><span style="background-color: #ffcccc; padding: 2px 5px; border-radius: 3px;"><strong>0, 1</strong></span> = <span style="color: #d9534f; font-weight: bold;">Simone Biles</span> (20%)</li>
            <li><span style="background-color: #ccffcc; padding: 2px 5px; border-radius: 3px;"><strong>2, 3, 4</strong></span> = <span style="color: #5cb85c; font-weight: bold;">Caitlin Clark</span> (30%)</li>
            <li><span style="background-color: #cce5ff; padding: 2px 5px; border-radius: 3px;"><strong>5, 6, 7, 8, 9</strong></span> = <span style="color: #0275d8; font-weight: bold;">Serena Williams</span> (50%)</li>
        </ul>
        <p><strong>Goal:</strong> Get all three pictures!</p>
    </div>
    """

    # The simulation string: "89064| 2730|8 64568 1|41..."
    # Trial 1: 8(S.W) 9(S.W) 0(Simone) 6(S.W) 4(Caitlin). Collected S.W, Simone, Caitlin. Success!
    # Trial 2: 2(Caitlin) 7(S.W) 3(Caitlin) 0(Simone). Collected Caitlin, S.W, Simone. Success!
    # Trial 3: 8645681 -> 8(S.W) 6(S.W) 4(Caitlin) 5(S.W) 6(S.W) 8(S.W) 1(Simone). Success!
    
    table_rows = ""
    trials = [
        ("89064", "Serena, Serena, Simone, Serena, Caitlin", "Yes (5 boxes)"),
        ("2730", "Caitlin, Serena, Caitlin, Simone", "Yes (4 boxes)"),
        ("8645681", "Serena, Serena, Caitlin, Serena, Serena, Serena, Simone", "Yes (7 boxes)"),
        ("41...", "Caitlin, Simone...", "Incomplete")
    ]
    
    for digits, outcomes, result in trials:
        formatted_digits = ""
        for d in digits:
            if d in ['0', '1']: color = "#d9534f" # Red/Simone
            elif d in ['2', '3', '4']: color = "#5cb85c" # Green/Caitlin
            else: color = "#0275d8" # Blue/Serena
            
            if d in "0123456789":
                formatted_digits += f'<span style="color: {color}; font-weight: bold; font-size: 1.2em; margin-right: 2px;">{d}</span>'
            else:
                formatted_digits += d
                
        table_rows += f"<tr><td style='letter-spacing: 2px;'>{formatted_digits}</td><td>{outcomes}</td><td>{result}</td></tr>"

    viz_html = f"""
    <table class="table" style="width: 100%; border: 1px solid #ddd;">
        <thead style="background-color: #eee;">
            <tr>
                <th>Random Digits</th>
                <th>Outcomes</th>
                <th>Result (Success?)</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
    """
    
    title_md = "**Put it all together to run the simulation:**\n\n5. Run several trials."
    
    return title_md + "\n\n" + key_html + "\n" + viz_html

def stylize_chapter_11(notebook_path, output_path):
    print(f"Reading {notebook_path}...")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Find Cell 15 (Simulation Table)
    target_idx = -1
    for i, cell in enumerate(nb.cells):
        if "89064" in cell.source or "Component Model" in cell.source:
            target_idx = i
            break
            
    if target_idx != -1:
        print(f"Refining Cell {target_idx} (Simulation Table) with styled content...")
        nb.cells[target_idx] = new_markdown_cell(create_styled_cereal_content())
    else:
        print("Warning: Could not find '89064' in notebook.")

    # Find the earlier cell "Specify how to model" containing the plain text key
    # Text: "**0, 1 Simone 2, 3, 4 Caitlin 5, 6, 7, 8, 9 Serena.**"
    model_idx = -1
    for i, cell in enumerate(nb.cells):
        if "0, 1 Simone" in cell.source and "Specify how to model" in cell.source:
            model_idx = i
            break
            
    if model_idx != -1:
        print(f"Refining Cell {model_idx} (Component Definition) with styled content...")
        # We want to keep the text before the key, and replace the key line with the HTML key.
        # The key_html variable in create_styled_cereal_content() is what we want.
        # Let's extract just the key from that function or redefine it here.
        
        # Redefine key purely for this replacement to be safe/clean
        key_html = """
<div style="background-color: #f9f9f9; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
    <strong>Component Model (Key):</strong>
    <ul>
        <li><span style="background-color: #ffcccc; padding: 2px 5px; border-radius: 3px;"><strong>0, 1</strong></span> = <span style="color: #d9534f; font-weight: bold;">Simone Biles</span> (20%)</li>
        <li><span style="background-color: #ccffcc; padding: 2px 5px; border-radius: 3px;"><strong>2, 3, 4</strong></span> = <span style="color: #5cb85c; font-weight: bold;">Caitlin Clark</span> (30%)</li>
        <li><span style="background-color: #cce5ff; padding: 2px 5px; border-radius: 3px;"><strong>5, 6, 7, 8, 9</strong></span> = <span style="color: #0275d8; font-weight: bold;">Serena Williams</span> (50%)</li>
    </ul>
</div>
"""
        # Current cell content usually ends with the bold text. We will replace that bold line.
        # Original: "...One possible assignment of the digits, then, is\n\n> **0, 1 Simone 2..."
        # We can just replace the whole cell content with a cleaner logic + the HTML key.
        
        new_source = """**Specify how to model a component outcome using equally likely random digits:**

1. Identify the component to be repeated.

> In this case, our component is the opening of a box of cereal.

2. Explain how you will model the component’s outcome.

> The digits from 0 to 9 are equally likely to occur. Because 20% of the boxes contain Simone’s picture, we’ll use 2 of the 10 digits to represent that outcome. Three of the 10 digits can model the 30% of boxes with Caitlin’s cards, and the remaining 5 digits can represent the 50% of boxes with Serena.
>
> One possible assignment of the digits, then, is:

""" + key_html
        
        nb.cells[model_idx] = new_markdown_cell(new_source)

    print(f"Saving to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Done!")

if __name__ == "__main__":
    stylize_chapter_11("Chapter_11.ipynb", "Chapter_11.ipynb")
