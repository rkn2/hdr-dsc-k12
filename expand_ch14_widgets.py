
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell
import os

def create_tree_code():
    return """
import ipywidgets as widgets
import matplotlib.pyplot as plt
from IPython.display import display

def plot_tree_diagram(p_disease, p_pos_given_disease, p_pos_given_healthy):
    # Complement probabilities
    p_healthy = 1 - p_disease
    p_neg_given_disease = 1 - p_pos_given_disease
    p_neg_given_healthy = 1 - p_pos_given_healthy
    
    # Path Probabilities
    p_d_pos = p_disease * p_pos_given_disease
    p_d_neg = p_disease * p_neg_given_disease
    p_h_pos = p_healthy * p_pos_given_healthy
    p_h_neg = p_healthy * p_neg_given_healthy
    
    # Total Positive
    p_positive = p_d_pos + p_h_pos
    
    # Bayes Theorem: P(Disease | Positive)
    p_disease_given_pos = p_d_pos / p_positive if p_positive > 0 else 0
    
    # Visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    
    # Coordinates
    root = (1, 5)
    d_node = (4, 7)
    h_node = (4, 3)
    dp_node = (7, 8)
    dn_node = (7, 6)
    hp_node = (7, 4)
    hn_node = (7, 2)
    
    # Draw Lines
    ax.plot([root[0], d_node[0]], [root[1], d_node[1]], 'k-', lw=1)
    ax.plot([root[0], h_node[0]], [root[1], h_node[1]], 'k-', lw=1)
    
    ax.plot([d_node[0], dp_node[0]], [d_node[1], dp_node[1]], 'k-', lw=1)
    ax.plot([d_node[0], dn_node[0]], [d_node[1], dn_node[1]], 'k-', lw=1)
    
    ax.plot([h_node[0], hp_node[0]], [h_node[1], hp_node[1]], 'k-', lw=1)
    ax.plot([h_node[0], hn_node[0]], [h_node[1], hn_node[1]], 'k-', lw=1)
    
    # Nodes
    ax.plot(*root, 'ko') 
    
    # Labels
    # Stage 1
    ax.text(2.5, 6.2, f"Disease\\n{p_disease:.2%}", ha='right')
    ax.text(2.5, 3.8, f"Healthy\\n{p_healthy:.2%}", ha='right')
    
    # Stage 2
    ax.text(5.5, 7.8, f"+ Test\\n{p_pos_given_disease:.2%}", ha='right', color='green')
    ax.text(5.5, 6.2, f"- Test\\n{p_neg_given_disease:.2%}", ha='right', color='red')
    ax.text(5.5, 3.8, f"+ Test\\n{p_pos_given_healthy:.2%}", ha='right', color='green')
    ax.text(5.5, 2.2, f"- Test\\n{p_neg_given_healthy:.2%}", ha='right', color='red')
    
    # Outcomes
    ax.text(7.2, 8, f"True Positive\\nP={p_d_pos:.4f}", va='center')
    ax.text(7.2, 6, f"False Negative\\nP={p_d_neg:.4f}", va='center')
    ax.text(7.2, 4, f"False Positive\\nP={p_h_pos:.4f}", va='center')
    ax.text(7.2, 2, f"True Negative\\nP={p_h_neg:.4f}", va='center')
    
    plt.title(f"Conditional Probability Tree Diagram\\nP(Disease | Positive Test) = {p_disease_given_pos:.2%}", fontsize=14)
    plt.show()

# Controls
style = {'description_width': 'initial'}
p_disease = widgets.FloatLogSlider(value=0.01, base=10, min=-4, max=-1, step=0.1, description='Prevalence P(D):', style=style)
p_sens = widgets.FloatSlider(value=0.95, min=0.5, max=1.0, step=0.01, description='Sensitivity P(+|D):', style=style)
p_false_pos = widgets.FloatSlider(value=0.05, min=0.0, max=0.2, step=0.01, description='False Pos Rate P(+|H):', style=style)

ui = widgets.VBox([p_disease, p_sens, p_false_pos])
out = widgets.interactive_output(plot_tree_diagram, 
                                 {'p_disease': p_disease, 
                                  'p_pos_given_disease': p_sens, 
                                  'p_pos_given_healthy': p_false_pos})

display(ui, out)
"""

def create_intro_markdown():
    return """
### Interactive Experiment: Conditional Probability Tree

Conditional probability can be counter-intuitive. 
**Scenario:** You test positive for a rare disease. The test is 95% accurate. Do you have the disease?
Maybe not! If the disease is rare enough, the **False Positives** (healthy people testing positive) might outnumber the **True Positives** (sick people testing positive).

**Explore:**
*   Adjust the prevalence (how common the disease is).
*   See how the final probability **P(Disease | Positive)** changes.
*   This visualizes **Bayes' Theorem** without needing to memorize the formula!
"""

def inject_widgets(notebook_path, output_path):
    print(f"Reading {notebook_path}...")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Insert after "Drawing Without Replacement" (Cell 13, the last one likely)
    # Or after General Multiplication Rule.
    idx = len(nb.cells) 
    
    print(f"Injecting Tree Widget at end (cell {idx})...")
    nb.cells.append(new_markdown_cell(create_intro_markdown()))
    nb.cells.append(new_code_cell(create_tree_code()))

    print(f"Saving to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Done!")

if __name__ == "__main__":
    inject_widgets("Chapter_14.ipynb", "Chapter_14.ipynb")
