import pygame
import sys
import random

# Inicializar pygame
pygame.init()

# Configuración pantalla
ANCHO = 800
ALTO = 600
TAMANO_BLOQUE = 20

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Snake 🐍")

clock = pygame.time.Clock()

# Colores
NEGRO = (15, 15, 15)
VERDE = (0, 200, 0)
ROJO = (220, 50, 50)
BLANCO = (255, 255, 255)

# Fuente
fuente = pygame.font.SysFont("Arial", 32)

# Snake inicial
snake = [(100, 100)]
direccion = (TAMANO_BLOQUE, 0)

# Comida
comida = (
    random.randrange(0, ANCHO, TAMANO_BLOQUE),
    random.randrange(0, ALTO, TAMANO_BLOQUE)
)

# Puntaje
puntaje = 0

def dibujar_texto(texto, x, y):
    superficie = fuente.render(texto, True, BLANCO)
    pantalla.blit(superficie, (x, y))

def reiniciar_juego():
    global snake, direccion, comida, puntaje

    snake = [(100, 100)]
    direccion = (TAMANO_BLOQUE, 0)

    comida = (
        random.randrange(0, ANCHO, TAMANO_BLOQUE),
        random.randrange(0, ALTO, TAMANO_BLOQUE)
    )

    puntaje = 0

# Bucle principal
while True:

    # Eventos
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_w and direccion != (0, TAMANO_BLOQUE):
                direccion = (0, -TAMANO_BLOQUE)

            if evento.key == pygame.K_s and direccion != (0, -TAMANO_BLOQUE):
                direccion = (0, TAMANO_BLOQUE)

            if evento.key == pygame.K_a and direccion != (TAMANO_BLOQUE, 0):
                direccion = (-TAMANO_BLOQUE, 0)

            if evento.key == pygame.K_d and direccion != (-TAMANO_BLOQUE, 0):
                direccion = (TAMANO_BLOQUE, 0)

    # Nueva cabeza
    cabeza_x = snake[0][0] + direccion[0]
    cabeza_y = snake[0][1] + direccion[1]

    nueva_cabeza = (cabeza_x, cabeza_y)

    # Colisiones con bordes
    if (
        cabeza_x < 0
        or cabeza_x >= ANCHO
        or cabeza_y < 0
        or cabeza_y >= ALTO
    ):
        reiniciar_juego()

    # Colisión consigo misma
    if nueva_cabeza in snake:
        reiniciar_juego()

    # Mover snake
    snake.insert(0, nueva_cabeza)

    # Comer comida
    if nueva_cabeza == comida:

        puntaje += 1

        comida = (
            random.randrange(0, ANCHO, TAMANO_BLOQUE),
            random.randrange(0, ALTO, TAMANO_BLOQUE)
        )

    else:
        snake.pop()

    # Dibujar fondo
    pantalla.fill(NEGRO)

    # Dibujar comida
    pygame.draw.rect(
        pantalla,
        ROJO,
        (comida[0], comida[1], TAMANO_BLOQUE, TAMANO_BLOQUE)
    )

    # Dibujar snake
    for segmento in snake:

        pygame.draw.rect(
            pantalla,
            VERDE,
            (
                segmento[0],
                segmento[1],
                TAMANO_BLOQUE,
                TAMANO_BLOQUE
            )
        )

    # Mostrar puntaje
    dibujar_texto(f"Puntaje: {puntaje}", 10, 10)

    # Actualizar pantalla
    pygame.display.flip()

    # FPS
    clock.tick(10)