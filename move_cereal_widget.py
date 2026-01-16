import nbformat
import os

def move_widget():
    nb_path = 'Chapter_11.ipynb'
    if not os.path.exists(nb_path):
        print(f"Error: {nb_path} not found.")
        return

    print(f"Reading {nb_path}...")
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # 1. Find and remove the misplaced widget cells
    # They are likely defined by the markdown header "Interactive Cereal Box Simulator" 
    # and the code cell containing "class CerealBoxSimulator"
    
    cells_to_move = []
    indices_to_remove = []
    
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'markdown' and "Interactive Cereal Box Simulator" in cell.source:
            indices_to_remove.append(i)
            cells_to_move.append(cell)
        elif cell.cell_type == 'code' and "class CerealBoxSimulator" in cell.source:
            indices_to_remove.append(i)
            cells_to_move.append(cell)
            
    if not cells_to_move:
        print("Could not find widget cells to move. They might not exist or title changed.")
        return

    # Remove in reverse order to maintain indices during deletion
    for i in sorted(indices_to_remove, reverse=True):
        del nb.cells[i]
        
    print(f"Removed {len(cells_to_move)} cells.")

    # 2. Find the correct insertion point
    # We want to insert AFTER the cell that contains the Cereal Example table.
    # We identified this cell has "Component Model (Key)" AND "<table"
    
    target_idx = -1
    for i, cell in enumerate(nb.cells):
        if "Component Model (Key)" in cell.source and "<table" in cell.source:
            target_idx = i + 1
            break
            
    if target_idx == -1:
        print("Could not find Cereal Example table cell. Appending to end.")
        target_idx = len(nb.cells)
    
    print(f"Inserting widget at new index {target_idx}...")
    
    # Insert the cells (header first, then code)
    # Assuming cells_to_move[0] is header and [1] is code based on previous script order
    # But let's be safe and check types if needed, though sequential append is fine if they were sequential
    
    # Verify order: Markdown Header should be first
    if cells_to_move[0].cell_type != 'markdown':
        cells_to_move.reverse()
        
    for cell in reversed(cells_to_move): # Insert in reverse order at same index to push down
        nb.cells.insert(target_idx, cell)

    print(f"Saving to {nb_path}...")
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Done!")

if __name__ == "__main__":
    move_widget()
