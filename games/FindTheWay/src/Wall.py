from os import path

import pygame
import random
from mlgame.view.view_model import create_rect_view_data, create_asset_init_data, create_image_view_data

EXPLOTION_PATH = path.join(path.dirname(__file__), "asset", "image", "explosion.png")


class Wall(pygame.sprite.Sprite):
    def __init__(self, construction: dict, **kwargs):
        super().__init__()
        init_pos = (construction["x"], construction["y"])
        init_size = (construction["width"], construction["height"])
        self.rect = pygame.Rect(*init_pos, *init_size)
        self.color = "#ffff00"

    @property
    def xy(self):
        return self.rect.topleft

    @property
    def game_object_data(self):
        return create_rect_view_data(
            name="wall"
            , x=self.rect.x
            , y=self.rect.y
            , width=self.rect.width
            , height=self.rect.height
            , color=self.color
            , angle=0)
