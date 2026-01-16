import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell
import os

def create_cereal_widget_code():
    return """import ipywidgets as widgets
from IPython.display import display, clear_output
import numpy as np
import matplotlib.pyplot as plt

class CerealBoxSimulator:
    def __init__(self):
        # Configuration
        self.athletes = ['Simone Biles', 'Caitlin Clark', 'Serena Williams']
        self.probs = [0.2, 0.3, 0.5]
        self.colors = ['#d9534f', '#5cb85c', '#0275d8'] # Red, Green, Blue matching the text
        
        # State associated with single trial
        self.collection = {name: 0 for name in self.athletes}
        self.boxes_opened = 0
        self.history = [] # List of cards found in order
        
        # Simulation State
        self.sim_results = []
        
        # UI Elements
        self.out_display = widgets.Output()
        self.out_plot = widgets.Output()
        
        self.btn_buy_one = widgets.Button(description="Buy 1 Box", button_style='info', icon='shopping-cart')
        self.btn_buy_all = widgets.Button(description="Buy Until Full Set", button_style='warning', icon='fast-forward')
        self.btn_reset = widgets.Button(description="Reset Collection", button_style='danger', icon='refresh')
        
        self.btn_sim_100 = widgets.Button(description="Simulate 100 Classes", button_style='success', icon='area-chart')
        
        # Layout
        self.btn_buy_one.on_click(self.on_buy_one)
        self.btn_buy_all.on_click(self.on_buy_all)
        self.btn_reset.on_click(self.on_reset)
        self.btn_sim_100.on_click(self.on_sim_100)
        
        self.controls = widgets.HBox([self.btn_buy_one, self.btn_buy_all, self.btn_reset])
        self.sim_controls = widgets.HBox([self.btn_sim_100])
        
        self.dashboard = widgets.VBox([
            widgets.HTML("<h3>Cereal Box Simulation</h3>"),
            widgets.HTML("<p><strong>Goal:</strong> Collect all 3 pictures (Simone 20%, Caitlin 30%, Serena 50%)</p>"),
            self.controls,
            self.out_display,
            widgets.HTML("<hr>"),
            widgets.HTML("<h4>Class Simulation (Group Mode)</h4>"),
            self.sim_controls,
            self.out_plot
        ])
        
        self.update_display()

    def get_card(self):
        return np.random.choice(self.athletes, p=self.probs)

    def on_buy_one(self, b):
        card = self.get_card()
        self.collection[card] += 1
        self.boxes_opened += 1
        self.history.append(card)
        self.update_display()
        
    def on_buy_all(self, b):
        # Limit to prevent infinite loops in weird cases, though unlikely here
        limit = 100
        while not all(self.collection.values()) and self.boxes_opened < limit:
            self.on_buy_one(None)
            
    def on_reset(self, b):
        self.collection = {name: 0 for name in self.athletes}
        self.boxes_opened = 0
        self.history = []
        self.update_display()
        
    def run_full_trial(self):
        # Helper for simulation: run until done and return count
        coll = {name: 0 for name in self.athletes}
        count = 0
        while not all(coll.values()):
            card = np.random.choice(self.athletes, p=self.probs)
            coll[card] += 1
            count += 1
        return count

    def on_sim_100(self, b):
        self.sim_results = [self.run_full_trial() for _ in range(100)]
        self.update_plot()

    def update_display(self):
        with self.out_display:
            clear_output(wait=True)
            
            # Status Banner
            is_complete = all(self.collection.values())
            status_color = "#dff0d8" if is_complete else "#f2dede"
            status_text = "COLLECTION COMPLETE!" if is_complete else "Collection Incomplete"
            
            html = f'''
            <div style="background-color: {status_color}; padding: 10px; border-radius: 5px; margin-top: 10px;">
                <h4 style="margin-top:0;">Boxes Opened: {self.boxes_opened} | Status: {status_text}</h4>
                <div style="display: flex; gap: 10px;">
            '''
            
            for i, name in enumerate(self.athletes):
                count = self.collection[name]
                # visual style
                opacity = "1.0" if count > 0 else "0.3"
                border = f"3px solid {self.colors[i]}" if count > 0 else "1px dashed #ccc"
                
                html += f'''
                <div style="opacity: {opacity}; border: {border}; padding: 10px; border-radius: 8px; width: 120px; text-align: center; background-color: white;">
                    <div style="font-size: 24px; color: {self.colors[i]}; font-weight: bold;">{count}</div>
                    <div style="font-size: 14px;">{name}</div>
                    <div style="font-size: 10px; color: #777;">{int(self.probs[i]*100)}%</div>
                </div>
                '''
            
            html += "</div></div>"
            display(widgets.HTML(html))
            
            # Show last few cards
            if self.history:
                recent = self.history[-10:]
                history_html = "<div style='margin-top: 5px; color: #666;'>Recent: " + " &rarr; ".join([f"<span style='color:{self.get_color(c)}'>{c.split()[0]}</span>" for c in recent]) + "</div>"
                display(widgets.HTML(history_html))

    def get_color(self, name):
        if name == 'Simone Biles': return self.colors[0]
        if name == 'Caitlin Clark': return self.colors[1]
        return self.colors[2]

    def update_plot(self):
        with self.out_plot:
            clear_output(wait=True)
            if not self.sim_results:
                return
            
            avg = np.mean(self.sim_results)
            med = np.median(self.sim_results)
            
            plt.figure(figsize=(10, 4))
            plt.hist(self.sim_results, bins=range(min(self.sim_results), max(self.sim_results)+2), 
                     color='skyblue', edgecolor='white', align='left')
            plt.axvline(avg, color='red', linestyle='dashed', linewidth=1, label=f'Mean: {avg:.1f}')
            plt.axvline(med, color='green', linestyle='dashed', linewidth=1, label=f'Median: {med:.1f}')
            plt.title('Distribution of Boxes Needed (100 Trials)')
            plt.xlabel('Number of Boxes')
            plt.ylabel('Frequency')
            plt.legend()
            plt.grid(axis='y', alpha=0.3)
            plt.show()

# Run the widget
sim = CerealBoxSimulator()
display(sim.dashboard)
"""

def add_widget_to_notebook():
    nb_path = 'Chapter_11.ipynb'
    if not os.path.exists(nb_path):
        print(f"Error: {nb_path} not found.")
        return

    print(f"Reading {nb_path}...")
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Find the 'Put it all together' section or 'Analyze the response variable' section
    # The formatted table is likely in a cell with "89064" or "Component Model"
    
    target_idx = -1
    for i, cell in enumerate(nb.cells):
        if "Analyze the response variable" in cell.source:
            target_idx = i
            break
            
    if target_idx == -1:
        # Fallback: look for the table we just styled
        for i, cell in enumerate(nb.cells):
            if "Component Model (Key)" in cell.source and "table" in cell.source:
                target_idx = i + 1 # Insert after the table
                break
                
    if target_idx == -1:
        print("Could not find suitable insertion point. Appending to end.")
        target_idx = len(nb.cells)

    print(f"Inserting widget at index {target_idx}...")
    
    # Create the cells
    header_cell = new_markdown_cell("### Interactive Cereal Box Simulator\n\nNow it's your turn! Instead of using a random number table, use this simulator to 'buy' boxes and see how long it takes to complete your collection.")
    code_cell = new_code_cell(create_cereal_widget_code())
    
    # Insert
    nb.cells.insert(target_idx, header_cell)
    nb.cells.insert(target_idx + 1, code_cell)

    print(f"Saving to {nb_path}...")
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Done!")

if __name__ == "__main__":
    add_widget_to_notebook()
