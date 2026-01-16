import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell
import os

def create_styled_phillies_content():
    # Explanation HTML
    explanation_html = """
    <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin-bottom: 20px; border-left: 5px solid #d9534f;">
        <h4 style="margin-top:0; color: #d9534f;">⚾ World Series Model (2-3-2 Format)</h4>
        <p><strong>Scenario:</strong> Phillies (Home) vs. Red Sox (Away). Best of 7 games. First to 4 wins.</p>
        <p><strong>Home Field Advantage:</strong> The home team has a <strong>55%</strong> chance of winning any game.</p>
        <hr>
        <strong>Digit Assignment (00-99):</strong>
        <ul>
            <li><span style="background-color: #dff0d8; padding: 2px 5px; border-radius: 3px;"><strong>00 - 54</strong></span> = <strong>Home Team Wins</strong> (55%)</li>
            <li><span style="background-color: #f2dede; padding: 2px 5px; border-radius: 3px;"><strong>55 - 99</strong></span> = <strong>Away Team Wins</strong> (45%)</li>
        </ul>
        <br>
        <strong>Schedule:</strong>
        <table style="width: 80%; font-size: 0.9em; margin-bottom: 0;">
            <tr style="background-color: #eee;">
                <th>Game</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th>
            </tr>
            <tr>
                <td><strong>Location</strong></td>
                <td>Philly</td><td>Philly</td><td>Boston</td><td>Boston</td><td>Boston</td><td>Philly</td><td>Philly</td>
            </tr>
            <tr>
                <td><strong>Home Team</strong></td>
                <td>Phillies</td><td>Phillies</td><td>Red Sox</td><td>Red Sox</td><td>Red Sox</td><td>Phillies</td><td>Phillies</td>
            </tr>
        </table>
    </div>
    """

    # Static Simulation Table with Sample Data
    # 89059 -> 89 (Away Win), 05 (Home Win), 9...
    # Let's use the provided string "89059 43528..."
    # 89059 -> 89, 05, 9... (The string is grouped by 5, need pairs for 00-99)
    # Let's re-interpret standard parsing: "89" "05" "94" "35" "28"
    
    # Trial 1: 89059 43528
    # G1 (Philly Home): 89 (>54) -> Away Win (Red Sox leads 1-0)
    # G2 (Philly Home): 05 (<=54) -> Home Win (Tied 1-1)
    # G3 (Boston Home): 94 (>54) -> Away Win (Phillies win! 1-2 Philly lead) -> WAIT. 
    # Logic check: "Away Team Wins". If Boston is Home, and digit is "Away Win", then PHILLY wins.
    # Correct Logic: 
    #   If Location = Philly: 00-54=Philly, 55-99=Boston
    #   If Location = Boston: 00-54=Boston, 55-99=Philly
    
    # Let's apply this to "89 05 94 35 28 10 54"
    # 1. @Philly: 89 (Away) -> Bos Win. (Series: Bos 1-0)
    # 2. @Philly: 05 (Home) -> Phi Win. (Series: Tied 1-1)
    # 3. @Boston: 94 (Away) -> Phi Win. (Series: Phi 2-1)
    # 4. @Boston: 35 (Home) -> Bos Win. (Series: Tied 2-2)
    # 5. @Boston: 28 (Home) -> Bos Win. (Series: Bos 3-2)
    # 6. @Philly: 10 (Home) -> Phi Win. (Series: Tied 3-3)
    # 7. @Philly: 54 (Home) -> Phi Win. (Series: Phi 4-3) -> PHILLIES WIN!
    
    viz_html = """
    <p><strong>Sample Trial:</strong> Using random digits <code>89 05 94 35 28 10 54</code></p>
    <table class="table" style="width: 100%; border: 1px solid #ddd;">
        <thead style="background-color: #eee;">
            <tr>
                <th>Game</th>
                <th>Location</th>
                <th>Random Digit</th>
                <th>Winner</th>
                <th>Series Score (Phi-Bos)</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>1</td><td>Philly</td><td><span style="color:red">89</span> (Away)</td><td>Red Sox</td><td>0 - 1</td></tr>
            <tr><td>2</td><td>Philly</td><td><span style="color:green">05</span> (Home)</td><td><strong>Phillies</strong></td><td>1 - 1</td></tr>
            <tr><td>3</td><td>Boston</td><td><span style="color:green">94</span> (Away)</td><td><strong>Phillies</strong></td><td>2 - 1</td></tr>
            <tr><td>4</td><td>Boston</td><td><span style="color:red">35</span> (Home)</td><td>Red Sox</td><td>2 - 2</td></tr>
            <tr><td>5</td><td>Boston</td><td><span style="color:red">28</span> (Home)</td><td>Red Sox</td><td>2 - 3</td></tr>
            <tr><td>6</td><td>Philly</td><td><span style="color:green">10</span> (Home)</td><td><strong>Phillies</strong></td><td>3 - 3</td></tr>
            <tr><td>7</td><td>Philly</td><td><span style="color:green">54</span> (Home)</td><td><strong>Phillies</strong></td><td><strong>4 - 3</strong></td></tr>
        </tbody>
    </table>
    <p><strong>Result:</strong> Phillies win the series in 7 games.</p>
    """
    
    return explanation_html + viz_html

def create_widget_code():
    return """import ipywidgets as widgets
from IPython.display import display, clear_output
import numpy as np
import matplotlib.pyplot as plt

class WorldSeriesSimulator:
    def __init__(self):
        # Config
        self.home_win_prob = 0.55
        self.schedule = ['Philly', 'Philly', 'Boston', 'Boston', 'Boston', 'Philly', 'Philly']
        
        # State
        self.wins_phi = 0
        self.wins_bos = 0
        self.current_game = 0
        self.game_log = []
        self.sim_results = [] # Store 'Phi' or 'Bos' for mass sim
        
        # UI
        self.out_display = widgets.Output()
        self.out_plot = widgets.Output()
        
        self.btn_play = widgets.Button(description="Play Next Game", button_style='info', icon='play')
        self.btn_reset = widgets.Button(description="Reset Series", button_style='warning', icon='refresh')
        self.btn_sim_1000 = widgets.Button(description="Simulate 1000 Series", button_style='success', icon='fast-forward')
        
        self.btn_play.on_click(self.on_play_game)
        self.btn_reset.on_click(self.on_reset)
        self.btn_sim_1000.on_click(self.on_sim_1000)
        
        self.controls = widgets.HBox([self.btn_play, self.btn_reset])
        
        self.dashboard = widgets.VBox([
            widgets.HTML("<h3>⚾ Interactive World Series Simulator</h3>"),
            widgets.HTML(f"<p><strong>Rules:</strong> Best of 7. Home team has {int(self.home_win_prob*100)}% win chance.</p>"),
            self.controls,
            self.out_display,
            widgets.HTML("<hr>"),
            self.btn_sim_1000,
            self.out_plot
        ])
        
        self.update_display()

    def play_game_logic(self):
        if self.wins_phi >= 4 or self.wins_bos >= 4:
            return None
            
        loc = self.schedule[self.current_game]
        home_team = 'Phillies' if loc == 'Philly' else 'Red Sox'
        
        # Random roll
        roll = np.random.rand()
        
        if roll < self.home_win_prob:
            winner = home_team
        else:
            winner = 'Red Sox' if home_team == 'Phillies' else 'Phillies'
            
        return {'game': self.current_game + 1, 'loc': loc, 'winner': winner}

    def on_play_game(self, b):
        res = self.play_game_logic()
        if res:
            self.current_game += 1
            if res['winner'] == 'Phillies': self.wins_phi += 1
            else: self.wins_bos += 1
            self.game_log.append(res)
            self.update_display()

    def on_reset(self, b):
        self.wins_phi = 0
        self.wins_bos = 0
        self.current_game = 0
        self.game_log = []
        self.update_display()

    def run_full_series(self):
        phi = 0
        bos = 0
        for i in range(7):
            if phi == 4: return 'Phillies'
            if bos == 4: return 'Red Sox'
            
            loc = self.schedule[i]
            home_team = 'Phillies' if loc == 'Philly' else 'Red Sox'
            if np.random.rand() < self.home_win_prob:
                winner = home_team
            else:
                winner = 'Red Sox' if home_team == 'Phillies' else 'Phillies'
                
            if winner == 'Phillies': phi += 1
            else: bos += 1
            
        return 'Phillies' if phi == 4 else 'Red Sox'

    def on_sim_1000(self, b):
        results = [self.run_full_series() for _ in range(1000)]
        phi_wins = results.count('Phillies')
        self.sim_results = results
        
        with self.out_plot:
            clear_output(wait=True)
            plt.figure(figsize=(8, 4))
            plt.bar(['Phillies', 'Red Sox'], [phi_wins, 1000-phi_wins], color=['#d9534f', '#002f6c'])
            plt.title(f"1000 Simulated Series Results (Phi Wins: {phi_wins/10}%)")
            plt.ylabel("Series Won")
            plt.grid(axis='y', alpha=0.3)
            plt.show()

    def update_display(self):
        with self.out_display:
            clear_output(wait=True)
            
            # Series Scoreboard
            html = f'''
            <div style="display: flex; gap: 20px; align-items: center; margin: 10px 0;">
                <div style="text-align: center;">
                    <h2 style="margin:0; color: #d9534f;">{self.wins_phi}</h2>
                    <div>Phillies</div>
                </div>
                <div style="font-size: 1.5em; color: #777;">-</div>
                <div style="text-align: center;">
                    <h2 style="margin:0; color: #002f6c;">{self.wins_bos}</h2>
                    <div>Red Sox</div>
                </div>
            </div>
            '''
            
            # Game Log Table
            if self.game_log:
                rows = ""
                for g in self.game_log:
                     winner_style = "font-weight:bold; color: #d9534f" if g['winner'] == 'Phillies' else "font-weight:bold; color: #002f6c"
                     rows += f"<tr><td>{g['game']}</td><td>{g['loc']}</td><td style='{winner_style}'>{g['winner']}</td></tr>"
                
                html += f'''
                <table class="table" style="width: 50%; border: 1px solid #ddd; margin-top: 10px;">
                    <thead style="background-color: #f5f5f5;"><tr><th>Game</th><th>Location</th><th>Winner</th></tr></thead>
                    <tbody>{rows}</tbody>
                </table>
                '''
                
            if self.wins_phi == 4:
                html += "<div style='color: #d9534f; font-weight: bold; margin-top: 10px;'>🏆 PHILLIES WIN THE WORLD SERIES!</div>"
            elif self.wins_bos == 4:
                html += "<div style='color: #002f6c; font-weight: bold; margin-top: 10px;'>🏆 RED SOX WIN THE WORLD SERIES!</div>"
                
            display(widgets.HTML(html))

# Run
ws_sim = WorldSeriesSimulator()
display(ws_sim.dashboard)
"""

def update_notebook():
    nb_path = 'Chapter_11.ipynb'
    if not os.path.exists(nb_path):
        print(f"Error: {nb_path} not found.")
        return

    print(f"Reading {nb_path}...")
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Search for "Suppose the Philadelphia Phillies" to identify the cell
    target_idx = -1
    for i, cell in enumerate(nb.cells):
        if "Suppose the Philadelphia Phillies" in cell.source:
            target_idx = i
            break
            
    if target_idx == -1:
        print("Could not find Phillies example cell.")
        return

    print(f"Found static example at cell {target_idx}. Updating content...")
    
    # 1. Update the static markdown cell with our styled HTML
    nb.cells[target_idx].source = create_styled_phillies_content()
    
    # 2. Inject the widget immediately after
    # Check if widget is already there to avoid duplicates
    if target_idx + 1 < len(nb.cells) and "class WorldSeriesSimulator" in nb.cells[target_idx+1].source:
        print("Widget code already exists. Updating it...")
        nb.cells[target_idx+1].source = create_widget_code()
    else:
        print("Injecting new widget code...")
        code_cell = new_code_cell(create_widget_code())
        nb.cells.insert(target_idx + 1, code_cell)

    print(f"Saving to {nb_path}...")
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Done!")

if __name__ == "__main__":
    update_notebook()
