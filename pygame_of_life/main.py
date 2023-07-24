import pygame
import sys
from pygame_of_life.engine import GameEngine, Color
# Inicializar Pygame
pygame.init()
pygame.font.init()

# Definir el tamaño de la pantalla
WIDTH = 800
HEIGHT = 800

NUM_ROWS = 40
NUM_COLS = 40

# Crear la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyGame of Life")

pygame.time.set_timer(pygame.USEREVENT, 1000)

def main():
    # Dibujar los elementos en la pantalla
    screen.fill((0, 0, 0))  # Limpiar la pantalla con color negro

    # Score
    games = 0

    # Init game
    engine = GameEngine(screen=screen, height=HEIGHT, width=WIDTH, rows=NUM_ROWS, cols=NUM_COLS)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the mouse click coordinates
                click = pygame.mouse.get_pos()
                engine.handle(click)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    engine.toggle_run()
                    engine.paint_border()
            if event.type == pygame.USEREVENT:
                # Call the function every second
                engine.execute()
        pygame.display.flip()

if __name__ == "__main__":
    main()