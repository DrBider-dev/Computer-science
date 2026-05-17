# game/algorithms/greedy.py
import json
import os

def run_greedy():
    if not os.path.exists("data/state.json"):
        return None
        
    with open("data/state.json", "r") as f:
        state = json.load(f)
        
    grid = {(d['row'], d['col']): d for d in state['grid']}
    infected = [d for d in state['grid'] if d['state'] == 'infected']
    
    candidates = set()
    for inf in infected:
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = inf['row'] + dr, inf['col'] + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if grid[(nr, nc)]['state'] == 'healthy':
                    candidates.add((nr, nc))
                    
    if not candidates:
        return None
        
    best = max(candidates, key=lambda pos: grid[pos]['risk'])
    return {"row": best[0], "col": best[1], "risk": grid[best]['risk']}

if __name__ == "__main__":
    # Puede ser llamado independientemente para pruebas
    print(run_greedy())