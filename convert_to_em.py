import json
import glob
import re
import os

# Order from most specific to least specific
replacements = [
    # Complex Phrasings
    ("cards in boxes of cereal", "compliance certificates in shipments"),
    ("New Jersey’s Pick-6", "ASTM A36 Testing"),
    ("Convenience Sample (Basketball Court)", "Convenience Sample (High-Performance Site)"),
    ("Basketball team members are taller", "Samples from high-performance concrete are stronger"),
    ("pain severity", "corrosion extent"),
    ("gender, income level", "material grade, fabrication method"),
    ("age, gender, income level", "exposure level, material grade, project scale"),
    ("three different fertilizers", "three different steel alloys"),
    ("medication, acupuncture, and physical therapy", "galvanization, epoxy coating, and cathodic protection"),
    ("sandy, loamy, and clayey", "Simple, Warren, and Pratt"),
    ("20-30 years", "Category I exposure"),
    ("31-40 years", "Category II exposure"),
    ("41-50 years", "Category III exposure"),
    ("demographic differences", "environmental variances"),
    
    # Chapter 10 Contexts (Agricultural/Medical/Consumer)
    ("Fertilizers", "Steel Composites"),
    ("Fertilizer", "Steel Composite"),
    ("Crop Yield", "Stress Handling"),
    ("crop yield", "structural strength"),
    ("soil type", "truss configuration"),
    ("soil", "material"),
    ("Pain Relief Therapies", "Corrosion Protections"),
    ("pain relief therapies", "corrosion protection methods"),
    ("chronic back pain", "surface oxidation"),
    ("age groups", "environment types"),
    ("age group", "environment type"),
    ("age", "environmental exposure"),
    ("Packaging Designs", "Connection Methods"),
    ("packaging designs", "fastening techniques"),
    ("packaging design", "connection type"),
    ("minimalist, colorful, and eco-friendly", "bolted, welded, and riveted"),
    ("consumer preferences", "structural reliability"),
    ("Consumer Preferences", "Structural Reliability"),
    ("product", "component"),
    ("consumers", "inspectors"),
    ("demographic groups", "project scales"),
    ("demographic group", "project scale"),
    ("participant", "technician"),
    ("participants", "technicians"),
    
    # Chapter 14/15/16 Contexts (Student/Health/Voting)
    ("student", "structural element"),
    ("students", "structural elements"),
    ("exam scores", "yield strengths"),
    ("test scores", "load capacities"),
    ("scores", "readings"),
    ("score", "reading"),
    ("grade", "rating"),
    ("grades", "ratings"),
    ("GPA", "Safety Factor"),
    ("voter", "load point"),
    ("voters", "load points"),
    ("Democrats", "Structural Engineers"),
    ("Republicans", "Geotechnical Engineers"),
    ("polling", "sensor monitoring"),
    ("survey", "inspection report"),
    ("surveys", "inspection reports"),
    ("drug", "additive"),
    ("drugs", "additives"),
    ("patient", "structure"),
    ("patients", "structures"),
    ("disease", "deflection"),
    ("healthy", "stable"),
    ("treatment", "reinforcement"),
    ("treatments", "reinforcements"),
    
    # General (Sports/Food/Games)
    ("DVD Grab Bag", "Materials Testing Bag"),
    ("basketball player", "concrete beam"),
    ("basketball star", "steel grade"),
    ("basketball", "reinforced concrete"),
    ("height 170cm", "compressive strength 3000 psi"),
    ("std dev 10cm", "std dev 400 psi"),
    ("cereal manufacturer", "standards board"),
    ("Lunch Special", "Base Design"),
    ("Hungry Special", "Advanced Design"),
    ("Hungry", "Advanced"),
    ("Simone Biles", "Carbon Fiber"),
    ("Caitlin Clark", "High-Strength Steel"),
    ("Serena Williams", "Prestressed Concrete"),
    ("athletes", "advanced materials"),
    ("gymnast", "bridges"),
    ("tennis pro", "dams"),
    ("batting orders", "construction staging sequences"),
    ("baseball manager", "structural lead"),
    ("volleyball squads", "inspection teams"),
    ("county legislature", "planning commission"),
    ("committee", "review panel"),
    ("representatives", "engineers"),
    ("password", "access code"),
    ("ATM", "safety lock"),
    ("pizza", "steel truss"),
    ("toppings", "joints"),
    ("ice cream", "aggregate mix"),
    ("scoop", "batch"),
    ("flavors", "grades"),
    ("cone", "pour"),
    ("salads", "girder profiles"),
    ("sandwiches", "deck slabs"),
    ("lunch", "design iteration"),
    ("café", "engineering firm"),
    ("lottery", "batch sample"),
    ("lotto", "randomized quality check"),
    ("bettor", "inspector"),
    ("grand prize", "passing grade"),
    ("prize", "passing grade"),
    ("height", "compressive strength"),
    ("playing basketball", "measuring concrete samples"),
    ("athlete", "material"),
    ("DVD", "steel sample")
]

def apply_replacements(text):
    for k, v in replacements:
        pattern = re.compile(re.escape(k), re.IGNORECASE)
        
        def replace_with_case(match):
            original = match.group(0)
            if original.isupper():
                return v.upper()
            if original.istitle():
                return v.title()
            return v
            
        text = pattern.sub(replace_with_case, text)
    return text

def process_notebooks():
    files = [f for f in glob.glob("Chapter_*.ipynb") if "_EM" not in f and "updated" not in f]
    for file in files:
        new_file = file.replace(".ipynb", "_EM.ipynb")
        print(f"Refining {new_file} from {file}...")

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
