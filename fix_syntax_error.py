import nbformat

def fix_syntax():
    nb_path = 'Chapter_10_updated.ipynb'
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    target_code = "plot_simpson"
    
    fixed_count = 0
    for cell in nb.cells:
        if cell.cell_type == 'code' and target_code in cell.source:
            # Fix 1: The definition with the space error
            if "x_ substantial" in cell.source:
                cell.source = cell.source.replace("x_ substantial", "x_subset")
                fixed_count += 1
                
            # Fix 2: The usages of the weird variable name to standardized "x_subset"
            if "x_substantial" in cell.source:
                cell.source = cell.source.replace("x_substantial", "x_subset")
                fixed_count += 1

    if fixed_count > 0:
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print(f"Fixed {fixed_count} syntax errors in notebook.")
    else:
        print("No syntax errors found or already fixed.")

if __name__ == "__main__":
    fix_syntax()
