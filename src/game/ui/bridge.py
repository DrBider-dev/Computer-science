# game/ui/bridge.py
import subprocess
import json
import os
from game.algorithms.greedy import run_greedy
from game.algorithms.backtracking import run_backtracking

def execute_system_tick(action=None):
    # 1. Registrar acción si el usuario interactuó
    if action:
        with open("data/action.json", "w") as f:
            json.dump(action, f, indent=2)
            
    # 2. Ejecutar el Motor en C++
    if os.path.exists("./engine_bin"):
        subprocess.run(["./engine_bin"])
    else:
        # Auto-compilación de respaldo si no existe el binario ejecutable
        subprocess.run(["g++", "engine/main.cpp", "-o", "engine_bin"])
        subprocess.run(["./engine_bin"])
        
    # 3. Correr algoritmos y fusionar sus salidas en result.json
    greedy_res = run_greedy()
    backtrack_res = run_backtracking()
    
    result_data = {
        "greedy_recommendation": greedy_res,
        "quarantine_plan": backtrack_res
    }
    
    with open("data/result.json", "w") as f:
        json.dump(result_data, f, indent=2)