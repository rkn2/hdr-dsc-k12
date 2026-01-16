import nbformat
import sys

def inspect_notebook(notebook_path):
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        print(f"Inspecting: {notebook_path}")
        print(f"Total Cells: {len(nb.cells)}")
        
        for i, cell in enumerate(nb.cells):
            cell_type = cell.cell_type
            source = cell.source.strip()
            # truncate source for display
            display_source = source[:100].replace('\n', ' ') + "..." if len(source) > 100 else source.replace('\n', ' ')
            
            print(f"Cell {i} [{cell_type}]: {display_source}")
            
    except Exception as e:
        print(f"Error reading notebook: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        inspect_notebook(sys.argv[1])
    else:
        print("Usage: python3 inspect_nb.py <notebook_path>")
