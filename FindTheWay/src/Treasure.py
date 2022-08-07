from enum import auto
from os import path
import math

import pygame
from mlgame.utils.enum import StringEnum
from mlgame.view.view_model import create_asset_init_data, create_image_view_data

TREASURE_PATH = path.join(path.dirname(__file__), "..", "asset", "image", "treasure.png")


class Treasure(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, size: tuple):
        super().__init__()
        # self._play_area_rect = play_area_rect
        self._init_pos = pos
        self.rect = pygame.Rect(*pos, 50, 50)
        self._score = 0

    @property
    def xy(self):
        return self.rect.topleft

    def reset(self):
        self.rect.topleft = self._init_pos

    def collide_with_player(self):
        pass

    @property
    def game_object_data(self):
        return create_image_view_data(image_id="treasure", x=self.rect.x, y=self.rect.y,
                                      width=self.rect.width, height=self.rect.height)

    @property
    def game_init_object_data(self):
        return create_asset_init_data(image_id="treasure",
                                      width=self.rect.width, height=self.rect.height,
                                      file_path=TREASURE_PATH,
                                      github_raw_url="https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/MyGame/asset/image/player.png")
