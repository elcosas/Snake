import pygame
from pygame.locals import *

BLOCKSIZE = 40

def main():
    pygame.init()
    clock = pygame.time.Clock()
    grid = [[None for y in range(0, 600 // BLOCKSIZE)] for x in range(0, 800 // BLOCKSIZE)]

    window = pygame.display.set_mode((800, 600)) 
    player = Snake((400, 300))

    running = True
    while running:
        clock.tick(5)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        player.get_input(pygame.key.get_pressed())
        window.fill((0, 0, 0))
        player.move_snake(grid)
        draw_grid(grid, window)
        pygame.display.flip()

    pygame.quit()

def draw_grid(grid, window):
    """draws all rect objects in grid taken as arg."""
    for i, col in enumerate(grid):
        for j, row in enumerate(col):
            if type(row) == pygame.Rect:
                seg = row.copy().move(row.x*BLOCKSIZE - row.x, row.y*BLOCKSIZE - row.y)
                pygame.draw.rect(window, (0, 255, 0), seg)
            else:
                pygame.draw.rect(window, (255, 255, 255), pygame.Rect(i*BLOCKSIZE, j*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE), 1)

class Snake(pygame.sprite.Sprite):
    """Uses a list of rects to represent segments."""
    def __init__(self, coords, start_length=3):
        super(Snake, self).__init__()
        self.segments = []
        for seg in range(start_length):
            rect = pygame.Rect((coords[0] // BLOCKSIZE), (coords[1] // BLOCKSIZE) + seg, BLOCKSIZE, BLOCKSIZE)
            self.segments.append(rect)
        self.dir = [0, -1]

    def get_input(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.dir = [0, -1]
        elif pressed_keys[K_DOWN]:
            self.dir = [0, 1]
        elif pressed_keys[K_LEFT]:
            self.dir = [-1, 0]
        elif pressed_keys[K_RIGHT]:
            self.dir = [1, 0]

    def move_snake(self, grid):
        for index, seg in enumerate(self.segments):
            if index == 0:
                pos = [seg.x, seg.y]
                seg.move_ip(self.dir[0], self.dir[1])
                grid[seg.x][seg.y] = seg
                grid[pos[0]][pos[1]] = None
            else:
                old_pos = [seg.x, seg.y]
                seg.move(pos[0] - seg.x, pos[1] - seg.y)
                grid[pos[0]][pos[1]] = seg
                grid[old_pos[0]][old_pos[1]] = None
                old_pos = pos

if __name__ == '__main__':
    main()
