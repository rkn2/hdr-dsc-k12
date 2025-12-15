import nbformat

def place_widget():
    nb_path = 'Chapter_10_updated.ipynb'
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Content signatures
    def_signature = "**Confounding:**"
    examples_signature = "**What could be the confounding factor?**"
    advanced_topic_signature = "### 🧩 Advanced Topic: Confounding Variables & Simpson's Paradox"
    widget_code_signature = "plot_exercise_paradox" # Distinctive string in the widget code

    # 1. Identify indices of key cells
    def_idx = -1
    examples_idx = -1
    advanced_topic_indices = []
    widget_indices = []

    for idx, cell in enumerate(nb.cells):
        if cell.cell_type == 'markdown':
            if def_signature in cell.source:
                def_idx = idx
            elif examples_signature in cell.source:
                examples_idx = idx
            elif advanced_topic_signature in cell.source:
                advanced_topic_indices.append(idx)
        elif cell.cell_type == 'code':
            if widget_code_signature in cell.source:
                widget_indices.append(idx)

    print(f"Definition found at: {def_idx}")
    print(f"Examples found at: {examples_idx}")
    print(f"Advanced Topic found at: {advanced_topic_indices}")
    print(f"Widget Code found at: {widget_indices}")

    # 2. Extract specific cells we want to keep and move
    # We take the first found valid instance of each if multiple exist, or create if missing (though they should exist)
    
    advanced_topic_cell = None
    if advanced_topic_indices:
        advanced_topic_cell = nb.cells[advanced_topic_indices[0]]
    else:
        print("Error: Advanced Topic cell not found.")
        return

    widget_cell = None
    if widget_indices:
        widget_cell = nb.cells[widget_indices[0]]
    else:
        print("Error: Widget code cell not found.")
        return

    # 3. Create a new list of cells excluding the ones we are moving (to avoid duplicates)
    indices_to_remove = set(advanced_topic_indices + widget_indices)
    new_cells = [cell for i, cell in enumerate(nb.cells) if i not in indices_to_remove]

    # 4. Find the insertion point in the NEW list
    # We want to insert AFTER the examples cell.
    # Note: indices change after removal, so we extraction-logic or re-find.
    # Re-finding in 'new_cells' is safer.
    
    insert_idx = -1
    for idx, cell in enumerate(new_cells):
        if cell.cell_type == 'markdown' and examples_signature in cell.source:
            insert_idx = idx
            break
    
    if insert_idx != -1:
        # Insert AFTER the examples cell
        target_idx = insert_idx + 1
        print(f"Inserting at new index: {target_idx}")
        new_cells.insert(target_idx, widget_cell) # Box/Widget 2nd
        new_cells.insert(target_idx, advanced_topic_cell) # Header 1st
    else:
        print("Error: Target insertion point ('What could be the confounding factor?') not found.")
        # Fallback: After definition
        for idx, cell in enumerate(new_cells):
            if cell.cell_type == 'markdown' and def_signature in cell.source:
                insert_idx = idx
                break
        if insert_idx != -1:
             print(f"Fallback: Inserting after definition at new index: {insert_idx + 1}")
             new_cells.insert(insert_idx + 1, widget_cell)
             new_cells.insert(insert_idx + 1, advanced_topic_cell)
        else:
            print("Error: Fallback definition cell not found. Appending to end.")
            new_cells.append(advanced_topic_cell)
            new_cells.append(widget_cell)

    nb.cells = new_cells

    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Notebook updated successfully.")

if __name__ == "__main__":
    place_widget()
