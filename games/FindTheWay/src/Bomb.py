from enum import auto
from os import path
import math

import pygame
# from mlgame.utils.enum import StringEnum
from mlgame.view.view_model import create_asset_init_data, create_image_view_data

# from Bomb import Bomb

BOMB_PATH = path.join(path.dirname(__file__), "..", "asset", "image", "bomb.png")


class Bomb(pygame.sprite.Sprite):
    def __init__(self, construction: dict):
        super().__init__()
        self.image_id = "bomb"
        init_pos = (construction["x"], construction["y"])
        init_size = (50, 50)
        self.rect = pygame.Rect(*init_pos, *init_size)
        self.cooldown = False
        self.used_frame = 0

    def update(self):
        self.used_frame += 1
        if self.used_frame % 6 == 0:
            self.cooldown = True
        else:
            self.cooldown = False

    def collide_with_walls(self, used_frame):
        self.image_id = "explosion"
        # print(self.used_frame, used_frame)

    @property
    def xy(self):
        return self.rect.topleft

    @property
    def game_object_data(self):
        return create_image_view_data(image_id=self.image_id, x=self.rect.x, y=self.rect.y,
                                       width=self.rect.width, height=self.rect.height, angle=0)

    @property
    def game_init_object_data(self):
        return create_asset_init_data(image_id="bomb",
                                       width=self.rect.width, height=self.rect.height,
                                       file_path=BOMB_PATH,
                                       github_raw_url="https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/MyGame/asset/image/bomb.png")
