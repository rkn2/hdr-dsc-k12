
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
            <li><span style="background-color: #ffcccc; padding: 2px 5px; border-radius: 3px;"><strong>0, 1</strong></span> = <span style="color: #d9534f; font-weight: bold;">Tiger Woods</span> (20%)</li>
            <li><span style="background-color: #ccffcc; padding: 2px 5px; border-radius: 3px;"><strong>2, 3, 4</strong></span> = <span style="color: #5cb85c; font-weight: bold;">Serena Williams</span> (30%)</li>
            <li><span style="background-color: #cce5ff; padding: 2px 5px; border-radius: 3px;"><strong>5, 6, 7, 8, 9</strong></span> = <span style="color: #0275d8; font-weight: bold;">Danica Patrick</span> (50%)</li>
        </ul>
        <p><strong>Goal:</strong> Get all three pictures!</p>
    </div>
    """

    # The simulation string: "89064| 2730|8 64568 1|41..."
    # We will format this into distinct "Trials".
    
    # Trial 1: 89064 -> 8(D) 9(D) 0(T) 6(D) 4(S). Collected D, T, S. Success! (Length 5)
    # Trial 2: 2730 -> 2(S) 7(D) 3(S) 0(T). Collected S, D, T. Success! (Length 4)
    # Trial 3: 8645681 -> 8(D) 6(D) 4(S) 5(D) 6(D) 8(D) 1(T). Collected D, S, T. Success! (Length 7)
    # Trial 4: 41 -> (Truncated?)
    
    # Let's build a nice visual for the trials found in the text.
    # I'll construct a table.
    
    table_rows = ""
    trials = [
        ("89064", "D, D, T, D, S", "Yes (5 boxes)"),
        ("2730", "S, D, S, T", "Yes (4 boxes)"),
        ("8645681", "D, D, S, D, D, D, T", "Yes (7 boxes)"),
        ("41...", "S, T...", "Incomplete")
    ]
    
    for digits, outcomes, result in trials:
        formatted_digits = ""
        for d in digits:
            if d in ['0', '1']: color = "#d9534f" # Red/Tiger
            elif d in ['2', '3', '4']: color = "#5cb85c" # Green/Serena
            else: color = "#0275d8" # Blue/Danica
            
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

    # Find Cell 15 (Index 15? or search for "89064")
    target_idx = -1
    for i, cell in enumerate(nb.cells):
        if "89064" in cell.source:
            target_idx = i
            break
            
    if target_idx != -1:
        print(f"Refining Cell {target_idx} with styled content...")
        nb.cells[target_idx] = new_markdown_cell(create_styled_cereal_content())
    else:
        print("Warning: Could not find '89064' in notebook.")

    print(f"Saving to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Done!")

if __name__ == "__main__":
    stylize_chapter_11("Chapter_11.ipynb", "Chapter_11.ipynb")
