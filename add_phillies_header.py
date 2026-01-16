import nbformat
from nbformat.v4 import new_markdown_cell
import os

def add_header():
    nb_path = 'Chapter_11.ipynb'
    if not os.path.exists(nb_path):
        print(f"Error: {nb_path} not found.")
        return

    print(f"Reading {nb_path}...")
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Find the widget code cell
    target_idx = -1
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code' and "class WorldSeriesSimulator" in cell.source:
            target_idx = i
            break
            
    if target_idx == -1:
        print("Could not find widget code cell.")
        return

    # Check if header already exists
    if target_idx > 0 and "Interactive World Series Simulator" in nb.cells[target_idx-1].source:
        print("Header already exists.")
        return

    print(f"Inserting header at index {target_idx}...")
    
    header_text = "### ⚾ Interactive World Series Simulator\n\n**Run the cell below** to load the simulator. You can play game-by-game or simulate the entire series 1000 times."
    header_cell = new_markdown_cell(header_text)
    
    nb.cells.insert(target_idx, header_cell)

    print(f"Saving to {nb_path}...")
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Done!")

if __name__ == "__main__":
    add_header()
