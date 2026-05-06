import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Constantes
ANCHO = 600
ALTO = 600
TAMANO_CELDA = 20
VELOCIDAD = 10

# Colores (RGB)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (50, 150, 255)
GRIS = (100, 100, 100)
NARANJA = (255, 165, 0)

# Configuración de la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Snake Game")
reloj = pygame.time.Clock()

# Fuentes
fuente = pygame.font.Font(None, 36)
fuente_grande = pygame.font.Font(None, 72)

def mostrar_texto(texto, color, x, y, tamano="normal"):
    """Muestra texto en la pantalla"""
    if tamano == "grande":
        superficie = fuente_grande.render(texto, True, color)
    else:
        superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect(center=(x, y))
    pantalla.blit(superficie, rect)

def dibujar_cuadricula():
    """Dibuja la cuadrícula de fondo"""
    for x in range(0, ANCHO, TAMANO_CELDA):
        pygame.draw.line(pantalla, GRIS, (x, 0), (x, ALTO), 1)
    for y in range(0, ALTO, TAMANO_CELDA):
        pygame.draw.line(pantalla, GRIS, (0, y), (ANCHO, y), 1)

def generar_comida(serpiente):
    """Genera comida en una posición aleatoria que no sea la serpiente"""
    while True:
        x = random.randint(0, (ANCHO - TAMANO_CELDA) // TAMANO_CELDA) * TAMANO_CELDA
        y = random.randint(0, (ALTO - TAMANO_CELDA) // TAMANO_CELDA) * TAMANO_CELDA
        if [x, y] not in serpiente:
            return [x, y]

def mostrar_puntuacion(puntuacion):
    """Muestra la puntuación actual"""
    mostrar_texto(f"Puntuación: {puntuacion}", BLANCO, ANCHO - 80, 20)

def pantalla_inicio():
    """Pantalla de inicio del juego"""
    pantalla.fill(NEGRO)
    mostrar_texto("SNAKE GAME", VERDE, ANCHO // 2, ALTO // 3, "grande")
    mostrar_texto("Presiona ESPACIO para comenzar", BLANCO, ANCHO // 2, ALTO // 2)
    mostrar_texto("Usa las flechas para moverte", AZUL, ANCHO // 2, ALTO // 2 + 40)
    mostrar_texto("Presiona ESC para salir", ROJO, ANCHO // 2, ALTO // 2 + 80)
    pygame.display.flip()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return True
                if evento.key == pygame.K_ESCAPE:
                    return False
    return False

def pantalla_game_over(puntuacion):
    """Pantalla de fin del juego"""
    pantalla.fill(NEGRO)
    mostrar_texto("GAME OVER", ROJO, ANCHO // 2, ALTO // 3, "grande")
    mostrar_texto(f"Puntuación final: {puntuacion}", BLANCO, ANCHO // 2, ALTO // 2)
    mostrar_texto("Presiona ESPACIO para jugar de nuevo", VERDE, ANCHO // 2, ALTO // 2 + 50)
    mostrar_texto("Presiona ESC para salir", ROJO, ANCHO // 2, ALTO // 2 + 100)
    pygame.display.flip()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return True
                if evento.key == pygame.K_ESCAPE:
                    return False
    return False

def juego_principal():
    """Función principal del juego"""
    
    # Posición inicial de la serpiente
    serpiente = [[ANCHO // 2, ALTO // 2]]
    direccion = "DERECHA"
    proxima_direccion = "DERECHA"
    
    # Generar comida inicial
    comida = generar_comida(serpiente)
    
    puntuacion = 0
    juego_terminado = False
    pausa = False
    
    while not juego_terminado:
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False
                
                if evento.key == pygame.K_p:
                    pausa = not pausa
                    continue
                
                if not pausa and not juego_terminado:
                    if evento.key == pygame.K_UP and direccion != "ABAJO":
                        proxima_direccion = "ARRIBA"
                    elif evento.key == pygame.K_DOWN and direccion != "ARRIBA":
                        proxima_direccion = "ABAJO"
                    elif evento.key == pygame.K_LEFT and direccion != "DERECHA":
                        proxima_direccion = "IZQUIERDA"
                    elif evento.key == pygame.K_RIGHT and direccion != "IZQUIERDA":
                        proxima_direccion = "DERECHA"
        
        if pausa:
            pantalla.fill(NEGRO)
            mostrar_texto("PAUSA", BLANCO, ANCHO // 2, ALTO // 2, "grande")
            mostrar_texto("Presiona P para continuar", AZUL, ANCHO // 2, ALTO // 2 + 50)
            pygame.display.flip()
            reloj.tick(VELOCIDAD)
            continue
        
        direccion = proxima_direccion
        
        # Mover la serpiente
        cabeza = serpiente[0].copy()
        if direccion == "ARRIBA":
            cabeza[1] -= TAMANO_CELDA
        elif direccion == "ABAJO":
            cabeza[1] += TAMANO_CELDA
        elif direccion == "IZQUIERDA":
            cabeza[0] -= TAMANO_CELDA
        elif direccion == "DERECHA":
            cabeza[0] += TAMANO_CELDA
        
        serpiente.insert(0, cabeza)
        
        # Verificar si comió la comida
        if cabeza == comida:
            puntuacion += 10
            comida = generar_comida(serpiente)
        else:
            serpiente.pop()
        
        # Verificar colisiones
        # Colisión con bordes
        if (cabeza[0] < 0 or cabeza[0] >= ANCHO or 
            cabeza[1] < 0 or cabeza[1] >= ALTO):
            juego_terminado = True
            break
        
        # Colisión con sí misma
        if cabeza in serpiente[1:]:
            juego_terminado = True
            break
        
        # Dibujar todo
        pantalla.fill(NEGRO)
        dibujar_cuadricula()
        
        # Dibujar comida
        pygame.draw.rect(pantalla, ROJO, (comida[0], comida[1], TAMANO_CELDA, TAMANO_CELDA))
        pygame.draw.rect(pantalla, NARANJA, (comida[0] + 2, comida[1] + 2, TAMANO_CELDA - 4, TAMANO_CELDA - 4))
        
        # Dibujar serpiente
        for i, segmento in enumerate(serpiente):
            color = VERDE if i == 0 else (0, 200, 0)
            pygame.draw.rect(pantalla, color, (segmento[0], segmento[1], TAMANO_CELDA, TAMANO_CELDA))
            pygame.draw.rect(pantalla, (0, 150, 0), (segmento[0] + 2, segmento[1] + 2, TAMANO_CELDA - 4, TAMANO_CELDA - 4))
        
        # Ojos de la serpiente (solo en la cabeza)
        if len(serpiente) > 0:
            cabeza_pos = serpiente[0]
            ojo_tamano = TAMANO_CELDA // 5
            if direccion in ["DERECHA", "IZQUIERDA"]:
                ojo_y = cabeza_pos[1] + TAMANO_CELDA // 3
                if direccion == "DERECHA":
                    ojo1_x = cabeza_pos[0] + TAMANO_CELDA - ojo_tamano * 2
                    ojo2_x = cabeza_pos[0] + TAMANO_CELDA - ojo_tamano * 2
                else:
                    ojo1_x = cabeza_pos[0] + ojo_tamano
                    ojo2_x = cabeza_pos[0] + ojo_tamano
                ojo1_y = ojo_y
                ojo2_y = ojo_y + TAMANO_CELDA // 3
            else:
                ojo_x = cabeza_pos[0] + TAMANO_CELDA // 3
                if direccion == "ABAJO":
                    ojo1_y = cabeza_pos[1] + TAMANO_CELDA - ojo_tamano * 2
                    ojo2_y = cabeza_pos[1] + TAMANO_CELDA - ojo_tamano * 2
                else:
                    ojo1_y = cabeza_pos[1] + ojo_tamano
                    ojo2_y = cabeza_pos[1] + ojo_tamano
                ojo1_x = ojo_x
                ojo2_x = ojo_x + TAMANO_CELDA // 3
            
            pygame.draw.circle(pantalla, BLANCO, (ojo1_x, ojo1_y), ojo_tamano)
            pygame.draw.circle(pantalla, BLANCO, (ojo2_x, ojo2_y), ojo_tamano)
            pygame.draw.circle(pantalla, NEGRO, (ojo1_x, ojo1_y), ojo_tamano // 2)
            pygame.draw.circle(pantalla, NEGRO, (ojo2_x, ojo2_y), ojo_tamano // 2)
        
        mostrar_puntuacion(puntuacion)
        
        # Mostrar controles
        mostrar_texto("P: Pausa", AZUL, 70, 20)
        mostrar_texto("ESC: Salir", ROJO, 70, 50)
        
        pygame.display.flip()
        reloj.tick(VELOCIDAD + (puntuacion // 100))  # Aumenta velocidad con la puntuación
    
    return pantalla_game_over(puntuacion)

def main():
    """Función principal del programa"""
    ejecutando = True
    
    while ejecutando:
        iniciar = pantalla_inicio()
        if not iniciar:
            break
        
        jugar_de_nuevo = juego_principal()
        if not jugar_de_nuevo:
            break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()