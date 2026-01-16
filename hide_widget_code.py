import nbformat
import os

def hide_widget_code():
    nb_path = 'Chapter_11.ipynb'
    if not os.path.exists(nb_path):
        print(f"Error: {nb_path} not found.")
        return

    print(f"Reading {nb_path}...")
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    updates = 0
    
    # Cells that have the @title annotation
    for cell in nb.cells:
        if cell.cell_type == 'code' and "# @title" in cell.source:
            # Check/Update metadata
            if 'cellView' not in cell.metadata or cell.metadata['cellView'] != 'form':
                print(f"Hiding code for cell with title: {cell.source.splitlines()[0]}...")
                cell.metadata['cellView'] = 'form'
                updates += 1

    if updates > 0:
        print(f"Saving {updates} metadata updates to {nb_path}...")
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print("Done!")
    else:
        print("No metadata updates needed.")

if __name__ == "__main__":
    hide_widget_code()
