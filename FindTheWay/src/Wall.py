import pygame
import random
from mlgame.view.view_model import create_rect_view_data

ColorList = ["#000000", "#ff0000", "#ffff00", "#00ff00", "#0000ff", "#FF00FF"]
class Wall(pygame.sprite.Sprite):
    def __init__(self, init_pos: tuple, init_size: tuple):
        super().__init__()
        self.rect = pygame.Rect(*init_pos, *init_size)
        self.color = ColorList[random.randint(0, 5)]

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








