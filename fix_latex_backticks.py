import nbformat
import os
import re

def fix_latex_backticks():
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

    # Patterns to match: $`...`$ or just removing ` inside $...$ 
    # But specifically the user mentioned: $`P(A)...`$ should be $P(A)...$
    # So we replace "$`" with "$" and "`$" with "$"
    
    for nb_path in notebooks:
        if not os.path.exists(nb_path):
            continue

        print(f"Scanning {nb_path}...")
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        updates = 0
        for cell in nb.cells:
            if cell.cell_type == 'markdown':
                original_source = cell.source
                
                # Replace $` with $
                new_source = original_source.replace("$`", "$")
                # Replace `$ with $
                new_source = new_source.replace("`$", "$")
                
                # Also handle potentially weird spacing like $ ` or ` $ if necessary, 
                # but let's stick to the specific issue first.
                
                if new_source != original_source:
                    cell.source = new_source
                    updates += 1

        if updates > 0:
            print(f"  Fixed {updates} cells in {nb_path}...")
            with open(nb_path, 'w', encoding='utf-8') as f:
                nbformat.write(nb, f)
        else:
            print(f"  No issues found in {nb_path}.")

    print("All notebooks processed!")

if __name__ == "__main__":
    fix_latex_backticks()
