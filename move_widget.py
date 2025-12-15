
import nbformat

def main():
    nb_path = "Chapter_10_updated.ipynb"
    
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
        
    confounding_cells = []
    other_cells = []
    
    # Identify and extract Confounding cells
    # We look for the specific header we added
    header_text = "### 🧩 Advanced Topic: Confounding Variables & Simpson's Paradox"
    
    capture_mode = False
    
    for cell in nb.cells:
        if cell.cell_type == 'markdown' and header_text in cell.source:
            capture_mode = True
            confounding_cells.append(cell)
            continue
            
        if capture_mode:
            # The next cell should be the code cell for the plot
            if cell.cell_type == 'code' and "plot_exercise_paradox" in cell.source:
                confounding_cells.append(cell)
                capture_mode = False # Stop identifying after capturing the code
            else:
                # If there was some intervening text (unlikely given my previous script), 
                # keep capturing or reset if it looks like a new section.
                # But for safety, let's assume the strict pair we inserted.
                # If we encounter something else, we might be drifting.
                # Actually, my previous script inserted them strictly adjacent.
                confounding_cells.append(cell)
                if cell.cell_type == 'code': # End of widget usually
                     capture_mode = False
        else:
            other_cells.append(cell)
            
    # Now append the confounding cells to the end
    final_cells = other_cells + confounding_cells
    
    nb.cells = final_cells
    
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
        
    print(f"Moved {len(confounding_cells)} Confounding Variable cells to the end of the notebook.")

if __name__ == "__main__":
    main()
