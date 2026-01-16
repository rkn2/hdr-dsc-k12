
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell
import os

def create_birthday_code():
    return """
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display

def birthday_paradox_sim(k_people=23):
    # Theoretical Calculation
    # P(No Match) = 365/365 * 364/365 * ... * (365-k+1)/365
    prob_no_match = 1.0
    for i in range(k_people):
        prob_no_match *= (365 - i) / 365
    prob_match = 1 - prob_no_match
    
    # Simulation (Run 1000 times)
    n_sims = 1000
    matches = 0
    for _ in range(n_sims):
        birthdays = np.random.randint(1, 366, size=k_people)
        if len(birthdays) != len(set(birthdays)):
            matches += 1
    sim_prob = matches / n_sims
    
    # Visualization
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Bar Chart comparison
    bars = ax.bar(['Theoretical P(Match)', f'Simulated P(Match)\\n(n={n_sims})'], 
           [prob_match, sim_prob], color=['skyblue', 'lightgreen'])
    
    ax.set_ylim(0, 1.0)
    ax.set_ylabel('Probability')
    ax.set_title(f"The Birthday Problem (Group Size: {k_people})")
    
    # Add labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1%}', ha='center', va='bottom', fontsize=12, weight='bold')
                
    # Threshold Line at 50%
    ax.axhline(0.5, color='red', linestyle='--', alpha=0.5)
    ax.text(0.5, 0.52, '50% Chance Threshold', color='red', ha='center')
    
    plt.show()

display(widgets.interactive(birthday_paradox_sim, 
                            k_people=widgets.IntSlider(value=23, min=2, max=100, step=1, description='People in Room:')))
"""

def create_intro_markdown():
    return """
### Interactive Experiment: The Birthday Problem

A famous counter-intuitive result in probability (using Combinations!) is the **Birthday Problem**.

**Question:** How many people do you need in a room so that there is a **50% chance** that at least two of them allow share the same birthday?

*   Most people guess a high number (like 180).
*   **Move the slider** to find out the real answer.
*   (Hint: It has to do with how many *pairs* of people you can form. With 23 people, there are ${23 \\choose 2} = 253$ possible pairs!)
"""

def inject_widgets(notebook_path, output_path):
    print(f"Reading {notebook_path}...")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Insert at the end (after "Combinations and Probability")
    idx = len(nb.cells)
    
    print(f"Injecting Birthday Widget at end (cell {idx})...")
    nb.cells.append(new_markdown_cell(create_intro_markdown()))
    nb.cells.append(new_code_cell(create_birthday_code()))

    print(f"Saving to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Done!")

if __name__ == "__main__":
    inject_widgets("Chapter_12.ipynb", "Chapter_12.ipynb")
