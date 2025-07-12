import pygame
from settings import *

class SurfaceMaker:
    def get_surf(self, block_type, size):
        image = pygame.Surface(size)
        image.fill("red")
        return image