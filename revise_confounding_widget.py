import nbformat
import random

def revise_widget():
    nb_path = 'Chapter_10_updated.ipynb'
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Signatures to identify cells
    # We look for the cell containing the old function name
    old_widget_signature = "def plot_exercise_paradox(show_confounder=False):"
    
    # We also want to update the markdown instructions above it
    old_markdown_signature = "### 🧩 Advanced Topic: Confounding Variables & Simpson's Paradox"

    # New Markdown Content
    new_markdown_source = """### 🧩 Advanced Topic: Confounding Variables & Simpson's Paradox

Sometimes, a lurking variable doesn't just explain a relationship—it can completely **reverse** it! This is known as **Simpson's Paradox**.

**Scenario:**
Imagine a dataset showing that **People who exercise MORE have HIGHER health risks.**
That sounds impossible, right?

*   **The Mystery:** Look at the chart below. The trend line goes UP (meaning exercise seems *bad* for you).
*   **The Mission:** Only one "hidden variable" explains this strange result. 
*   **Your Task:** Use the dropdown menu to **stratify** (group) the data by different factors. Can you find the variable that reveals the *true* relationship (where exercise lowers health risk)?
"""

    # New Widget Code
    new_widget_source = """import matplotlib.pyplot as plt
import numpy as np
import ipywidgets as widgets
from IPython.display import display

# Generate data once to keep it consistent
np.random.seed(42)
n = 300

# 1. Confounder: Age Group (Young, Mid, Senior)
# Seniors exercise MORE (retired) but have HIGHER baseline risk
# Youths exercise LESS (busy) but have LOWER baseline risk
groups = ['20s', '40s', '60s']
n_g = n // 3

ages = []
exercise = []
risk = []
gender = []
coffee = []

# Generate data for each group
for g in groups:
    if g == '20s':
        base_ex, base_risk = 2, 20
    elif g == '40s':
        base_ex, base_risk = 5, 45
    else: # 60s
        base_ex, base_risk = 8, 70
        
    # Generate variance
    ex_vals = np.random.normal(base_ex, 1.2, n_g)
    # The TRUTH: Within any group, -4 risk per hour of exercise
    risk_vals = base_risk - 4 * (ex_vals - base_ex) + np.random.normal(0, 5, n_g)
    
    ages.extend([g] * n_g)
    exercise.extend(ex_vals)
    risk.extend(risk_vals)
    
    # Generate irrelevant variables (randomly distributed)
    gender.extend(np.random.choice(['Male', 'Female'], n_g))
    coffee.extend(np.random.choice(['Drinker', 'Non-Drinker'], n_g))

exercise = np.array(exercise)
risk = np.array(risk)
ages = np.array(ages)
gender = np.array(gender)
coffee = np.array(coffee)

def plot_simpson(group_by):
    plt.figure(figsize=(10, 6))
    
    # 1. Define grouping
    if group_by == 'None (Aggregated)':
        labels = ['All Data']
        # Just one group of indices
        groups_indices = [np.arange(len(exercise))]
        colors = ['gray']
    
    elif group_by == 'Gender':
        labels = ['Female', 'Male']
        groups_indices = [np.where(gender == 'Female')[0], np.where(gender == 'Male')[0]]
        colors = ['magenta', 'blue']
        
    elif group_by == 'Coffee Preference':
        labels = ['Drinker', 'Non-Drinker']
        groups_indices = [np.where(coffee == 'Drinker')[0], np.where(coffee == 'Non-Drinker')[0]]
        colors = ['brown', 'green']
        
    elif group_by == 'Age Group (Confounder)':
        labels = ['20s', '40s', '60s']
        groups_indices = [np.where(ages == '20s')[0], np.where(ages == '40s')[0], np.where(ages == '60s')[0]]
        colors = ['blue', 'green', 'orange']

    # 2. Plotting Loop
    for idx, indices in enumerate(groups_indices):
        if len(indices) == 0: continue
        
        x_ substantial = exercise[indices]
        y_subset = risk[indices]
        
        # Scatter
        plt.scatter(x_substantial, y_subset, alpha=0.6, s=50, color=colors[idx], label=labels[idx])
        
        # Trend Line for this group
        if len(x_substantial) > 1:
            m, b = np.polyfit(x_substantial, y_subset, 1)
            # Determine style based on slope (Positive = Bad/Misleading, Negative = Good/True)
            style = '-' if m > 0 else '--' 
            width = 2 if m > 0 else 4
            plt.plot(x_substantial, m*x_substantial + b, color=colors[idx], linestyle=style, linewidth=width)

    plt.title(f"Health Risk vs. Exercise | Grouped by: {group_by}", fontsize=14)
    plt.ylabel("Health Risk Score")
    plt.xlabel("Weekly Exercise Hours")
    plt.legend(title=group_by if group_by != 'None (Aggregated)' else "Legend")
    plt.grid(True, alpha=0.3)
    
    # Hint text
    if group_by == 'Age Group (Confounder)':
        plt.annotate("Paradox Resolved!\\nWithin each age group,\\nexpected trend returns.", 
                     xy=(5, 40), xycoords='data', 
                     xytext=(200, 50), textcoords='offset points',
                     arrowprops=dict(facecolor='black', shrink=0.05),
                     fontsize=11, backgroundcolor='white')
    elif group_by == 'None (Aggregated)':
        plt.annotate("Misleading Trend:\\nLooks like exercise\\nINCREASES risk!", 
                     xy=(8, 75), xycoords='data', 
                     xytext=(-180, -50), textcoords='offset points',
                     arrowprops=dict(facecolor='red', shrink=0.05),
                     fontsize=11, color='red', backgroundcolor='white')

    plt.show()

# UI Setup
dropdown = widgets.Dropdown(
    options=['None (Aggregated)', 'Gender', 'Coffee Preference', 'Age Group (Confounder)'],
    value='None (Aggregated)',
    description='Color By:',
)

display(widgets.HTML("<b>Explore the Data:</b> Try grouping the points to find the hidden variable."))
output = widgets.interactive_output(plot_simpson, {'group_by': dropdown})
display(widgets.VBox([dropdown, output]))
"""

    markdown_replaced = False
    code_replaced = False

    for cell in nb.cells:
        if cell.cell_type == 'markdown' and old_markdown_signature in cell.source:
            cell.source = new_markdown_source
            markdown_replaced = True
            print("Markdown instruction cell updated.")
        
        if cell.cell_type == 'code' and old_widget_signature in cell.source:
            cell.source = new_widget_source
            code_replaced = True
            print("Widget code cell updated.")

    if not markdown_replaced:
        print("Warning: Markdown instruction cell not found/updated.")
    if not code_replaced:
        print("Warning: Widget code cell not found/updated.")

    if markdown_replaced or code_replaced:
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print("Notebook saved with revisions.")
    else:
        print("No changes made.")

if __name__ == "__main__":
    revise_widget()
