import nbformat
import os
import textwrap

def fix_indentation():
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

    print(f"Found cell at index {target_idx}. fixing indentation...")
    
    # Get current source
    source = nb.cells[target_idx].source
    
    # Dedent the source
    # textwrap.dedent removes common leading whitespace
    new_source = textwrap.dedent(source)
    
    # Also manual check: if dedent didn't work because of first line difference
    # split lines, strip common prefix manually if needed, but dedent covers most cases.
    # Given the previous dump showed explicit 4 spaces on mostly every line, let's just strip lines.
    
    # Robust approach: Split, strip 4 spaces if present, join.
    lines = source.splitlines()
    cleaned_lines = []
    
    # If the first line is empty (it was in the dump "\n"), skip it or keep it.
    # The dump showed:
    # 515:     "\n",
    # 516:     "    <div style...
    
    for line in lines:
        if line.startswith("    "):
            cleaned_lines.append(line[4:])
        else:
            cleaned_lines.append(line)
            
    nb.cells[target_idx].source = "\n".join(cleaned_lines)

    print(f"Saving to {nb_path}...")
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Done!")

if __name__ == "__main__":
    fix_indentation()
