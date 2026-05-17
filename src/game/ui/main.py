# game/ui/main.py
import pygame
import json
import os
import sys

# Asegurar que el path incluya la raíz para las importaciones de módulos hermanos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from game.ui.bridge import execute_system_tick

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plague Containment - Grupo 16")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 16)

# Colors
COLOR_HEALTHY = (140, 190, 70)
COLOR_INFECTED = (230, 60, 60)
COLOR_VACCINATED = (40, 150, 90)
COLOR_QUARANTINED = (40, 90, 170)
COLOR_BG = (30, 30, 30)
COLOR_TEXT = (240, 240, 240)
COLOR_HINT = (255, 235, 50)

CELL_SIZE = 55
OFFSET_X, OFFSET_Y = 40, 60

if not os.path.exists("data"):
    os.makedirs("data")

# Inicialización primaria del sistema
execute_system_tick()

running = True
while running:
    screen.fill(COLOR_BG)
    
    # Cargar datos de los puentes JSON
    state, result = None, None
    if os.path.exists("data/state.json"):
        with open("data/state.json", "r") as f: state = json.load(f)
    if os.path.exists("data/result.json"):
        with open("data/result.json", "r") as f: result = json.load(f)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and state:
            mx, my = pygame.mouse.get_pos()
            c = (mx - OFFSET_X) // CELL_SIZE
            r = (my - OFFSET_Y) // CELL_SIZE
            if 0 <= r < 8 and 0 <= c < 8:
                execute_system_tick({"action_type": "vaccinate", "row": r, "col": c})

    # Renderizar componentes
    if state:
        greedy_hint = result.get("greedy_recommendation") if result else None
        
        for district in state["grid"]:
            r, c = district["row"], district["col"]
            risk, status = district["risk"], district["state"]
            
            rect = pygame.Rect(OFFSET_X + c * CELL_SIZE, OFFSET_Y + r * CELL_SIZE, CELL_SIZE - 3, CELL_SIZE - 3)
            
            if status == "healthy": color = COLOR_HEALTHY
            elif status == "infected": color = COLOR_INFECTED
            elif status == "vaccinated": color = COLOR_VACCINATED
            else: color = COLOR_QUARANTINED
                
            pygame.draw.rect(screen, color, rect)
            
            # Dibujar indicador numérico de riesgo de la celda
            val_txt = font.render(str(risk), True, (255,255,255) if status != "healthy" else (45,45,45))
            screen.blit(val_txt, (rect.x + 20, rect.y + 18))
            
            # Dibujar borde si es la recomendación del Greedy Advisor
            if greedy_hint and greedy_hint["row"] == r and greedy_hint["col"] == c:
                pygame.draw.rect(screen, COLOR_HINT, rect, 3)
                
        # HUD derecho
        screen.blit(font.render(f"TURN: {state['turn']}", True, COLOR_TEXT), (520, 60))
        screen.blit(font.render(f"Infections: {len(state['infection_chain'])}", True, COLOR_TEXT), (520, 100))
        
        pygame.draw.rect(screen, COLOR_HINT, (520, 180, 20, 20))
        screen.blit(font.render("Greedy Recommendation", True, COLOR_TEXT), (550, 180))
        
        screen.blit(font.render("Click on a Healthy district", True, COLOR_TEXT), (520, 480))
        screen.blit(font.render("to deploy Vaccination.", True, COLOR_TEXT), (520, 500))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()