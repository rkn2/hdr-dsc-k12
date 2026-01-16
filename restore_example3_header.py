import nbformat
from nbformat.v4 import new_markdown_cell
import os

def restore_example3_header():
    nb_path = 'Chapter_11.ipynb'
    if not os.path.exists(nb_path):
        print(f"Error: {nb_path} not found.")
        return

    print(f"Reading {nb_path}...")
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Find the Free Throw Model HTML cell
    target_idx = -1
    for i, cell in enumerate(nb.cells):
        if "Free Throw Model" in cell.source:
            target_idx = i
            break
            
    if target_idx == -1:
        print("Could not find Free Throw Model cell.")
        return

    # Check if header already exists above it
    if target_idx > 0 and "Example 3" in nb.cells[target_idx-1].source:
        print("Header already exists.")
        return

    print(f"Inserting Example 3 header at index {target_idx}...")
    
    header_cell = new_markdown_cell("### Example 3: Sean's Free Throws")
    nb.cells.insert(target_idx, header_cell)

    print(f"Saving to {nb_path}...")
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Done!")

if __name__ == "__main__":
    restore_example3_header()
