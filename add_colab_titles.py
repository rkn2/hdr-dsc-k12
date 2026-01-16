import nbformat
import os

def add_titles():
    nb_path = 'Chapter_11.ipynb'
    if not os.path.exists(nb_path):
        print(f"Error: {nb_path} not found.")
        return

    print(f"Reading {nb_path}...")
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    updates = 0
    
    # Mapping of class names to titles
    class_to_title = {
        "class CerealBoxSimulator": "# @title 🥣 Cereal Box Simulator - Click 'Play' to Start",
        "class WorldSeriesSimulator": "# @title ⚾ World Series Simulator - Click 'Play' to Start",
        "class DormLotterySimulator": "# @title 🎫 Dorm Room Lottery Simulator - Click 'Play' to Start",
        "class FreeThrowSimulator": "# @title 🏀 Free Throw Simulator - Click 'Play' to Start"
    }

    for cell in nb.cells:
        if cell.cell_type == 'code':
            lines = cell.source.splitlines()
            # Check if any line defines one of our classes
            for class_name, title in class_to_title.items():
                if any(class_name in line for line in lines):
                    # Check if title already exists
                    if lines[0].strip() == title:
                        print(f"Title already exists for {class_name}")
                        break
                    
                    # Update cell source
                    print(f"Adding title for {class_name}...")
                    new_source = title + "\n" + cell.source
                    cell.source = new_source
                    updates += 1
                    break

    if updates > 0:
        print(f"Saving {updates} updates to {nb_path}...")
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print("Done!")
    else:
        print("No updates needed.")

if __name__ == "__main__":
    add_titles()
