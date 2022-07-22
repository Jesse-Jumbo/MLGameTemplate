import pygame
from mlgame.view.view_model import create_rect_view_data


class Wall(pygame.sprite.Sprite):
    def __init__(self, init_pos: tuple, init_size: tuple):
        super().__init__()
        self.rect = pygame.Rect(*init_pos, *init_size)

    def get_xy(self):
        return self.rect.topleft

    @property
    def get_object_data(self):
        return create_rect_view_data(name="wall", x=self.rect.x, y=self.rect.y, width=self.rect.width, height=self.rect.height, color="#ff0000", angle=0)
