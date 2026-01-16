import nbformat
import os

def inject_counting_widgets():
    nb_path = 'Chapter_12.ipynb'
    if not os.path.exists(nb_path):
        print(f"Error: {nb_path} not found.")
        return

    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Widget 1: OR Rule (Addition)
    or_widget_code = """# @title 🥗 The Lunch Special: Addition Rule (OR)
import ipywidgets as widgets
from IPython.display import display, HTML

def update_or_rule(salads, sandwiches):
    total = salads + sandwiches
    display(HTML(f\"\"\"
    <div style="border: 2px solid #2E7D32; padding: 15px; border-radius: 10px; background-color: #f1f8e9;">
        <h4 style="color: #2E7D32; margin-top:0;">Rule of Addition (OR)</h4>
        <p>If you choose <b>1</b> item from <b>Set A</b> ({salads} options) <b>OR</b> <b>1</b> item from <b>Set B</b> ({sandwiches} options):</p>
        <p style="font-size: 1.2em; font-weight: bold;">{salads} + {sandwiches} = <span style="color: #c62828;">{total} Total Options</span></p>
    </div>
    \"\"\"))

salads_slider = widgets.IntSlider(value=4, min=1, max=10, description='Salads:')
sands_slider = widgets.IntSlider(value=5, min=1, max=10, description='Sandwiches:')

ui = widgets.HBox([salads_slider, sands_slider])
out = widgets.interactive_output(update_or_rule, {'salads': salads_slider, 'sandwiches': sands_slider})

display(ui, out)
"""

    # Widget 2: AND Rule (Multiplication)
    and_widget_code = """# @title 🍔 The Hungry Special & License Plates: Multiplication Rule (AND)
import ipywidgets as widgets
from IPython.display import display, HTML

def update_and_rule(salads, sandwiches):
    total = salads * sandwiches
    display(HTML(f\"\"\"
    <div style="border: 2px solid #1565C0; padding: 15px; border-radius: 10px; background-color: #e3f2fd; margin-bottom: 20px;">
        <h4 style="color: #1565C0; margin-top:0;">Rule of Multiplication (AND)</h4>
        <p>If you choose <b>1</b> item from <b>Set A</b> ({salads} options) <b>AND</b> <b>1</b> item from <b>Set B</b> ({sandwiches} options):</p>
        <p style="font-size: 1.25em; font-weight: bold;">{salads} × {sandwiches} = <span style="color: #c62828;">{total} Possible Combinations</span></p>
    </div>
    \"\"\"))

def plate_calc(letters, numbers):
    # Standard CT: 2 letters, 5 numbers
    total = (26**letters) * (10**numbers)
    display(HTML(f\"\"\"
    <div style="border: 1px dashed #555; padding: 10px; border-radius: 5px; background-color: #fff;">
        <b>License Plate Calculator:</b><br>
        Pattern: {letters} Letters and {numbers} Numbers<br>
        Calculation: 26<sup>{letters}</sup> × 10<sup>{numbers}</sup> = <span style="color: blue;">{total:,}</span> unique plates.
    </div>
    \"\"\"))

# Hungry Special Controls
salads_s = widgets.IntSlider(value=4, min=1, max=10, description='Salads:')
sands_s = widgets.IntSlider(value=5, min=1, max=10, description='Sandwiches:')

# License Plate Controls
let_s = widgets.Dropdown(options=[1,2,3], value=2, description='Letters:')
num_s = widgets.Dropdown(options=[1,2,3,4,5,6], value=5, description='Numbers:')

ui_hungry = widgets.VBox([widgets.Label("<b>Hungry Special (Salad AND Sandwich):</b>"), widgets.HBox([salads_s, sands_s])])
out_hungry = widgets.interactive_output(update_and_rule, {'salads': salads_s, 'sandwiches': sands_s})

ui_plate = widgets.VBox([widgets.Label("<b>License Plate Explorer:</b>"), widgets.HBox([let_s, num_s])])
out_plate = widgets.interactive_output(plate_calc, {'letters': let_s, 'numbers': num_s})

display(ui_hungry, out_hungry, ui_plate, out_plate)
"""

    # Insertion logic
    found_idx_or = -1
    found_idx_and = -1
    
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'markdown':
            if "Fundamental Counting Principle (Part 1: OR)" in cell.source:
                found_idx_or = i
            if "Fundamental Counting Principle (Part 2: AND)" in cell.source:
                found_idx_and = i

    if found_idx_and != -1:
        # Check if the next cell is the image/text block to replace
        # We replace the text that comes AFTER the plate example if it includes the image.
        # However, it's safer to just insert the widget after the markdown cell.
        
        # Insert AND widget first (to not shift indices before we use them correctly)
        # We insert at idx + 1
        widget_and = nbformat.v4.new_code_cell(source=and_widget_code)
        widget_and.metadata = {"cellView": "form"}
        
        # Remove the base64 image from the markdown if it's there
        if "img src=\"data:image/png;base64" in nb.cells[found_idx_and].source:
             import re
             nb.cells[found_idx_and].source = re.sub(r'<img src="data:image/png;base64.*?>', '', nb.cells[found_idx_and].source, flags=re.DOTALL)

        nb.cells.insert(found_idx_and + 1, widget_and)
        
    if found_idx_or != -1:
        widget_or = nbformat.v4.new_code_cell(source=or_widget_code)
        widget_or.metadata = {"cellView": "form"}
        nb.cells.insert(found_idx_or + 1, widget_or)

    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Counting widgets injected.")

if __name__ == "__main__":
    inject_counting_widgets()
