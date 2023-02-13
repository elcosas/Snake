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
        clock.tick(10)
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
        for i in range(len(self.segments)-1, 0, -1):
            if i == len(self.segments)-1:
                grid[self.segments[i].x][self.segments[i].y] = None
            new_x = self.segments[i-1].x - self.segments[i].x
            new_y = self.segments[i-1].y - self.segments[i].y
            self.segments[i].move_ip(new_x, new_y)
            grid[self.segments[i].x][self.segments[i].y] = self.segments[i]
        head = self.segments[0]
        head.move_ip(self.dir[0], self.dir[1])
        grid[head.x][head.y] = head

if __name__ == '__main__':
    main()
