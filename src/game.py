import pygame
import pygame.font
from pygame.locals import *
from sys import exit
from random import choice
from snake import Snake
from apple import Apple
from constants import *

def main():
    pygame.init()
    pygame.display.set_caption('Snake')

    COUNTDOWN = pygame.USEREVENT + 1
    pygame.time.set_timer(COUNTDOWN, 1000)

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    font = pygame.font.Font(None, 16)

    count = 5
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit(0)
            elif event.type == COUNTDOWN:
                count -= 1
        
        window.fill((0, 0, 0))
        text = str(count)
        text_surface = font.render(text, False, (0, 255, 25))
        window.blit(text_surface, text_surface.get_rect(center=window.get_rect().center))

        if count <= 0:
            running = False

    game(window)

    pygame.quit()
    exit(0)

def game(window):
    clock = pygame.time.Clock()
    grid = [[None for y in range(0, WINDOW_HEIGHT // BLOCKSIZE)] for x in range(0, WINDOW_WIDTH // BLOCKSIZE)]

    SPAWNAPPLE = pygame.USEREVENT + 2
    spawnapple_evt = pygame.event.Event(SPAWNAPPLE)
    pygame.event.post(spawnapple_evt)

    player = Snake((400, 300))

    running = True
    while running:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == SPAWNAPPLE:
                new_x = choice(range(0, WINDOW_WIDTH // BLOCKSIZE))
                new_y = choice(range(0, WINDOW_HEIGHT // BLOCKSIZE))
                while grid[new_x][new_y] in player.segments:
                    new_x = choice(range(0, WINDOW_WIDTH // BLOCKSIZE))
                    new_y = choice(range(0, WINDOW_HEIGHT // BLOCKSIZE))
                apple = Apple((new_x, new_y))
                grid[new_x][new_y] = apple

        player.get_input(pygame.key.get_pressed())
        window.fill((0, 0, 0))
        player.move_snake(grid, apple, spawnapple_evt)
        draw_grid(grid, window)
        pygame.display.flip()

def draw_grid(grid, window):
    """Iterates through grid, drawing rects for blank spaces and the cooresponding
    object in the cell for each cell"""
    for i, col in enumerate(grid):
        for j, row in enumerate(col):
            if type(row) == pygame.Rect:
                seg = row.copy().move(row.x*BLOCKSIZE - row.x, row.y*BLOCKSIZE - row.y)
                pygame.draw.rect(window, (0, 255, 0), seg)
            elif type(row) == Apple:
                window.blit(row.surface, row.rect)
            else:
                pygame.draw.rect(window, (255, 255, 255), pygame.Rect(i*BLOCKSIZE, j*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE), 1)

if __name__ == '__main__':
    main()
