from pygame import sprite, Rect, event, quit
from pygame.locals import *
from apple import Apple
from constants import BLOCKSIZE

class Snake(sprite.Sprite):
    """Uses a list of rects to represent segments."""
    def __init__(self, coords, start_length=5):
        super(Snake, self).__init__()
        self.segments = []
        for seg in range(start_length):
            rect = Rect((coords[0] // BLOCKSIZE), (coords[1] // BLOCKSIZE) + seg, BLOCKSIZE, BLOCKSIZE)
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
            quit()
            exit(0)
        grid[head.x][head.y] = head

    def __collision(self, grid, active_apl, events):
        future_point = [self.segments[0].x + self.dir[0], self.segments[0].y + self.dir[1]]
        if grid[future_point[0]][future_point[1]] in self.segments:
            quit()
            exit(0)
            return True
        elif type(grid[future_point[0]][future_point[1]]) == Apple:
            rect = Rect(future_point[0], future_point[1], BLOCKSIZE, BLOCKSIZE)
            self.segments.insert(0, rect)
            grid[future_point[0]][future_point[1]] = rect
            active_apl.kill()
            event.post(events)
            return True
        return False