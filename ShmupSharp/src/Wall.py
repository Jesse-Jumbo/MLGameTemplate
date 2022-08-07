import pygame
import random
from mlgame.view.view_model import create_rect_view_data

Colarlist = ["#000000", "#ff0000", "#ffff00", "#00ff00", "#8c8c8c", "#0000ff", "#00FFFF", "#FF00FF", "#282828",
             "#22390A"]


class Wall(pygame.sprite.Sprite):
    def __init__(self, init_pos: tuple, init_size: tuple):
        super().__init__()
        self.rect = pygame.Rect(*init_pos, *init_size)
        self.hit_rect = pygame.Rect(0, 0, self.rect.width - 2, self.rect.height - 2)
        self.hit_rect.center = self.rect.center
        self.color = Colarlist[random.randint(0, 9)]

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

    def collide_with_bullets(self):
        self.kill()
