from enum import auto
from os import path
import math

import pygame
# from mlgame.utils.enum import StringEnum
from mlgame.view.view_model import create_asset_init_data, create_image_view_data
# from Bomb import Bomb

BOMB_PATH = path.join(path.dirname(__file__), "..", "asset", "image", "bomb.png")

class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, size: tuple):
        super().__init__()
        self._init_pos = pos
        self.rect = pygame.Rect(*pos, 50, 50)

    def update(self):
        pass

    @property
    def xy(self):
        return self.rect.topleft

    @property
    def game_object_data(self):
        return create_image_view_data(image_id="bomb", x=self.rect.x, y=self.rect.y,
                                      width=self.rect.width, height=self.rect.height, angle=0)

    @property
    def game_init_object_data(self):
        return create_asset_init_data(image_id="bomb",
                                      width=self.rect.width, height=self.rect.height,
                                      file_path=BOMB_PATH,
                                      github_raw_url="https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/MyGame/asset/image/bomb.png")
