import pygame
from settings import *
from os import walk

class SurfaceMaker:
    def __init__(self):
        for index, info in enumerate(walk("graphics/blocks")):
            if index == 0:
                self.assets = {color:{} for color in info[1]}
            else:
                for image_name in info[2]:
                    color_type = list(self.assets.keys())[index - 1]
                    full_path = "graphics/blocks" + f"{color_type}/" + image_name
                    print(full_path)

    def get_surf(self, block_type, size):
        image = pygame.Surface(size)
        image.fill("red")
        return image