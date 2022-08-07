import pygame
from mlgame.view.view_model import create_rect_view_data
from os import path

BOMB_PATH = path.join(path.dirname(__file__), "..", "asset", "image", "bomb.png")

class Bullet(pygame.sprite.Sprite):
    def __init__(self, init_pos: tuple, size: tuple):
        super().__init__()
        self.rect = pygame.Rect(*init_pos, 50, 50)

    def xy(self):
        return self.rect.topleft

    @property
    def game_object_data(self):
        return create_rect_view_data(
            name="bullet"
            , x=self.rect.x
            , y=self.rect.y
            , width=self.rect.width
            , height=self.rect.height
            , angle=0)

    def update(self, *args, **kwargs):
        pass