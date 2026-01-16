import nbformat
import os

def hide_all_code_cells():
    # List of notebooks to update
    notebooks = [
        "Chapter_9.ipynb",
        "Chapter_10.ipynb",
        "Chapter_11.ipynb",
        "Chapter_12.ipynb",
        "Chapter_13.ipynb",
        "Chapter_14.ipynb",
        "Chapter_15.ipynb",
        "Chapter_16.ipynb"
    ]
    
    # Also check for updated versions if they exist
    if os.path.exists("Chapter_10_updated.ipynb"):
        notebooks.append("Chapter_10_updated.ipynb")

    for nb_path in notebooks:
        if not os.path.exists(nb_path):
            print(f"Skipping {nb_path} (not found)")
            continue

        print(f"Processing {nb_path}...")
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        updates = 0
        for cell in nb.cells:
            if cell.cell_type == 'code':
                # Force 'form' view (hidden code)
                if 'metadata' not in cell:
                    cell.metadata = {}
                
                # We update it to form view to hide code
                if 'cellView' not in cell.metadata or cell.metadata['cellView'] != 'form':
                    cell.metadata['cellView'] = 'form'
                    updates += 1
                
                # Optional: Ensure it's not ID'd as 'collapsed' which is the old way, use the form view
                if 'collapsed' in cell.metadata:
                    del cell.metadata['collapsed']

        if updates > 0:
            print(f"  Hiding {updates} code cells in {nb_path}...")
            with open(nb_path, 'w', encoding='utf-8') as f:
                nbformat.write(nb, f)
        else:
            print(f"  No changes needed for {nb_path}.")

    print("All notebooks processed!")

if __name__ == "__main__":
    hide_all_code_cells()
