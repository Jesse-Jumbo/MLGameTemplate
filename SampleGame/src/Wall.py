import random

import pygame
from mlgame.view.view_model import create_rect_view_data


class Wall(pygame.sprite.Sprite):
    def __init__(self, init_pos: tuple, init_size: tuple):
        super().__init__()
        self.rect = pygame.Rect(*init_pos, *init_size)
        self.color = "#ff0000"
        self._shield = 100

    def update(self, *args, **kwargs) -> None:
        if self._shield <= 0:
            self.kill()

    def collide_with_bullet(self):
        self._shield -= random.randrange(100)

    @property
    def shield(self):
        return self._shield

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








