import pygame
from pygame.locals import *

def main():
    pygame.init()
    BLOCKSIZE = 40
    grid = [[pygame.Rect(x*BLOCKSIZE, y*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE) for y in range(0, 600 // BLOCKSIZE)] for x in range(0, 800 // BLOCKSIZE)]
    print(grid)

    window = pygame.display.set_mode((800, 600)) 

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        window.fill((0, 0, 0))
        draw_grid(grid, window)
        pygame.display.flip()

    pygame.quit()

def draw_grid(grid, window):
    """draws all rect objects in grid taken as arg"""
    for col in grid:
        for row in col:
            pygame.draw.rect(window, (255, 255, 255), row, 1)

if __name__ == '__main__':
    main()
