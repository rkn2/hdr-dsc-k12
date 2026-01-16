import nbformat
import os

def sanitize_indentation():
    nb_path = 'Chapter_11.ipynb'
    if not os.path.exists(nb_path):
        print(f"Error: {nb_path} not found.")
        return

    print(f"Reading {nb_path}...")
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Find the cell with the Phillies HTML content
    target_idx = -1
    for i, cell in enumerate(nb.cells):
        if "World Series Model (2-3-2 Format)" in cell.source and cell.cell_type == 'markdown':
            target_idx = i
            break
            
    if target_idx == -1:
        print("Could not find Phillies HTML cell.")
        return

    print(f"Found cell at index {target_idx}. Aggressively stripping indentation...")
    
    # Get current source
    source = nb.cells[target_idx].source
    
    # Slit into lines and strip leading whitespace from EACH line
    lines = source.splitlines()
    cleaned_lines = [line.lstrip() for line in lines]
    
    # Reassemble
    nb.cells[target_idx].source = "\n".join(cleaned_lines)

    print(f"Saving to {nb_path}...")
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Done!")

if __name__ == "__main__":
    sanitize_indentation()
