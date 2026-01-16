import nbformat
import os

def force_title_on_all_cells():
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
    
    if os.path.exists("Chapter_10_updated.ipynb"):
        notebooks.append("Chapter_10_updated.ipynb")

    for nb_path in notebooks:
        if not os.path.exists(nb_path):
            continue

        print(f"Processing {nb_path}...")
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        updates = 0
        for i, cell in enumerate(nb.cells):
            if cell.cell_type == 'code':
                # If "@title" is not in the source, add it
                if "# @title" not in cell.source:
                    # Create a generic title
                    title_line = "# @title Click 'Play' to Run Code"
                    
                    # If it's a specific known widget, try to be smarter (optional, but good for UX)
                    if "class " in cell.source:
                        first_line = cell.source.splitlines()[0]
                        if "class" in first_line:
                            cls_name = first_line.split("class")[1].split(":")[0].strip()
                            title_line = f"# @title {cls_name} - Click 'Play'"
                    
                    cell.source = title_line + "\n" + cell.source
                    updates += 1
                
                # Double force the metadata
                if 'metadata' not in cell:
                    cell.metadata = {}
                cell.metadata['cellView'] = 'form'

        if updates > 0:
            print(f"  Added @title to {updates} cells in {nb_path}...")
            with open(nb_path, 'w', encoding='utf-8') as f:
                nbformat.write(nb, f)
        else:
            print(f"  No source changes (just metadata check) for {nb_path}.")

    print("All notebooks processed!")

if __name__ == "__main__":
    force_title_on_all_cells()
