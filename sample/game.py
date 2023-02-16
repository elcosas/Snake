import pygame
from pygame.locals import *
from random import choice

BLOCKSIZE = 40

def main():
    pygame.init()
    clock = pygame.time.Clock()
    grid = [[None for y in range(0, 600 // BLOCKSIZE)] for x in range(0, 800 // BLOCKSIZE)]

    SPAWNAPPLE = pygame.USEREVENT + 1
    spawnapple_evt = pygame.event.Event(SPAWNAPPLE)
    pygame.event.post(spawnapple_evt)

    window = pygame.display.set_mode((800, 600))
    player = Snake((400, 300))

    running = True
    while running:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == SPAWNAPPLE:
                new_x = choice(range(0, 800 // BLOCKSIZE))
                new_y = choice(range(0, 600 // BLOCKSIZE))
                while grid[new_x][new_y] in player.segments:
                    new_x = choice(range(0, 800 // BLOCKSIZE))
                    new_y = choice(range(0, 600 // BLOCKSIZE))
                apple = Apple((new_x, new_y))
                grid[new_x][new_y] = apple

        player.get_input(pygame.key.get_pressed())
        window.fill((0, 0, 0))
        player.move_snake(grid, apple, spawnapple_evt)
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
            elif type(row) == Apple:
                window.blit(row.surface, row.rect)
            else:
                pygame.draw.rect(window, (255, 255, 255), pygame.Rect(i*BLOCKSIZE, j*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE), 1)

class Snake(pygame.sprite.Sprite):
    """Uses a list of rects to represent segments."""
    def __init__(self, coords, start_length=5):
        super(Snake, self).__init__()
        self.segments = []
        for seg in range(start_length):
            rect = pygame.Rect((coords[0] // BLOCKSIZE), (coords[1] // BLOCKSIZE) + seg, BLOCKSIZE, BLOCKSIZE)
            self.segments.append(rect)
        self.dir = [0, -1]

    def get_input(self, pressed_keys):
        if pressed_keys[K_UP] and self.dir[1] != 1:
            self.dir = [0, -1]
        elif pressed_keys[K_DOWN] and self.dir[1] != -1:
            self.dir = [0, 1]
        elif pressed_keys[K_LEFT] and self.dir[0] != 1:
            self.dir = [-1, 0]
        elif pressed_keys[K_RIGHT] and self.dir[0] != -1:
            self.dir = [1, 0]

    def move_snake(self, grid, active_apl, events):
        for i in range(len(self.segments)-1, 0, -1):
            if i == len(self.segments)-1:
                grid[self.segments[i].x][self.segments[i].y] = None
            new_x = self.segments[i-1].x - self.segments[i].x
            new_y = self.segments[i-1].y - self.segments[i].y
            self.segments[i].move_ip(new_x, new_y)
            grid[self.segments[i].x][self.segments[i].y] = self.segments[i]
        head = self.segments[0]
        if not self.__collision(grid, active_apl, events):
            head.move_ip(self.dir[0], self.dir[1])
        if head.x < 0 or head.y < 0:
            # TODO: Call Game Over
            pygame.quit()
        grid[head.x][head.y] = head

    def __collision(self, grid, active_apl, events):
        future_point = [self.segments[0].x + self.dir[0], self.segments[0].y + self.dir[1]]
        if grid[future_point[0]][future_point[1]] in self.segments:
            # TODO: Call Game Over
            pygame.quit()
            return True
        elif type(grid[future_point[0]][future_point[1]]) == Apple:
            rect = pygame.Rect(future_point[0], future_point[1], BLOCKSIZE, BLOCKSIZE)
            self.segments.insert(0, rect)
            grid[future_point[0]][future_point[1]] = rect
            active_apl.kill()
            pygame.event.post(events)
            return True
        return False

class Apple(pygame.sprite.Sprite):
    """Apple that can be consumed by snake, spawns
    randomly on the grid"""
    def __init__(self, coords):
        super(Apple, self).__init__()
        self.surface = pygame.Surface((BLOCKSIZE, BLOCKSIZE))
        self.surface.fill((255, 0, 0))
        self.rect = self.surface.get_rect(topleft=(coords[0]*BLOCKSIZE, coords[1]*BLOCKSIZE))

if __name__ == '__main__':
    main()
