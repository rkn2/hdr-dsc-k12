import json
import glob
import re
import os

replacements = {
    # Food & Leisure
    "pizza": "steel truss",
    "Pizza": "Steel Truss",
    "Pepperoni": "Bolts",
    "Mushroom": "Rivets",
    "Onions": "Welds",
    "toppings": "joints",
    "ice cream": "aggregate mix",
    "scoop": "batch",
    "flavors": "grades",
    "cone": "pour",
    "DVD Grab Bag": "Materials Testing Bag",
    "DVD": "steel sample",
    "Lunch Special": "Base Design",
    "Hungry Special": "Advanced Design",
    "salads": "girder profiles",
    "sandwiches": "deck slabs",
    "lunch": "design iteration",
    "café": "engineering firm",

    # Sports
    "basketball player": "concrete beam",
    "basketball star": "steel grade",
    "basketball": "reinforced concrete",
    "Caitlin Clark": "High-Strength Steel",
    "Simone Biles": "Carbon Fiber",
    "Serena Williams": "Prestressed Concrete",
    "athletes": "advanced materials",
    "gymnast": "bridges",
    "tennis pro": "dams",
    "batting orders": "construction staging sequences",
    "baseball manager": "structural lead",
    "players": "crane operators",
    "volleyball squads": "inspection teams",
    "coach": "chief engineer",

    # Lottery and Games
    "cards in boxes of cereal": "compliance certificates in shipments",
    "cards": "certificates",
    "cereal manufacturer": "standards board",
    "lottery": "batch sample",
    "lotto": "randomized quality check",
    "New Jersey’s Pick-6": "ASTM A36 Testing",
    "bettor": "inspector",
    "bettors": "inspectors",
    "betting": "testing",
    "grand prize": "passing grade",
    "prize": "passing grade",

    # Government / Other
    "county legislature": "planning commission",
    "Democrats": "Structural Engineers",
    "Republicans": "Geotechnical Engineers",
    "committee": "review panel",
    "representatives": "engineers",
    "password": "access code",
    "ATM": "safety lock"
}

def apply_replacements(text):
    for k, v in replacements.items():
        # simplistic replacement for demonstration; for case preservation we can do a re.sub
        text = re.sub(r"\b" + re.escape(k) + r"\b", v, text)
    return text

def process_notebooks():
    files = glob.glob("Chapter_*.ipynb")
    for file in files:
        if "_EM" in file or "updated" in file:
            continue
        
        new_file = file.replace(".ipynb", "_EM.ipynb")
        print(f"Creating {new_file}")

        with open(file, "r") as f:
            nb = json.load(f)
            
        for cell in nb.get("cells", []):
            if "source" in cell:
                if isinstance(cell["source"], list):
                    for i, line in enumerate(cell["source"]):
                        cell["source"][i] = apply_replacements(line)
                elif isinstance(cell["source"], str):
                    cell["source"] = apply_replacements(cell["source"])
                    
        with open(new_file, "w") as f:
            json.dump(nb, f, indent=1)

if __name__ == "__main__":
    process_notebooks()
