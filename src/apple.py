from pygame import sprite, Surface
from constants import BLOCKSIZE

class Apple(sprite.Sprite):
    """Apple that can be consumed by snake, spawns
    randomly on the grid"""
    def __init__(self, coords):
        super(Apple, self).__init__()
        self.surface = Surface((BLOCKSIZE, BLOCKSIZE))
        self.surface.fill((255, 0, 0))
        self.rect = self.surface.get_rect(topleft=(coords[0]*BLOCKSIZE, coords[1]*BLOCKSIZE))