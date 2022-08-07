from enum import auto
from os import path
import math

import pygame
# from mlgame.utils.enum import StringEnum
from mlgame.view.view_model import create_asset_init_data, create_image_view_data
# from Bomb import Bomb
from .Wall import Wall

PLAYER_PATH = path.join(path.dirname(__file__), "..", "asset", "image", "player.png")

class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, size: tuple, play_area_rect: pygame.Rect):
        super().__init__()
        self._play_area_rect = play_area_rect
        self._speed = 4
        self._init_pos = pos
        self.rect = pygame.Rect(*pos, 50, 50)
        self._score = 0
        self.live = 100
        self.angle = 0
        self.last_x = self.rect.x
        self.last_y = self.rect.y
        # self.bombs = pygame.sprite.Group()
    def update(self, action: list) -> None:
        self.last_x = self.rect.x
        self.last_y = self.rect.y
        while(self.angle < 0):
            self.angle += 360
        if "LEFT" in action:
            self.angle += 90
        if "UP" in action:
            if self.angle % 360 == 0 and self.rect.top > self._play_area_rect.top:
                self.move_up()
            elif self.angle % 360 == 90:
                self.move_left()
            elif self.angle % 360 == 180 and self.rect.bottom < self._play_area_rect.bottom:
                self.move_down()
            else:
                self.move_right()
        if "DOWN" in action:
            if self.angle % 360 == 0 and self.rect.bottom < self._play_area_rect.bottom:
                self.move_down()
            elif self.angle % 360 == 90:
                self.move_right()
            elif self.angle % 360 == 180 and self.rect.top > self._play_area_rect.top:
                self.move_up()
            else:
                self.move_left()
        if "RIGHT" in action:
            self.angle -= 90

    def move_up(self):
        self.rect.centery -= self._speed

    def move_down(self):
        self.rect.centery += self._speed

    def move_right(self):
        self.rect.centerx += self._speed

    def move_left(self):
        self.rect.centerx -= self._speed

    @property
    def score(self):
        return self._score

    @property
    def xy(self):
        return self.rect.topleft

    def reset(self):
        self.rect.topleft = self._init_pos

    def collide_with_walls(self):
        self.rect.x = self.last_x
        self.rect.y = self.last_y

    def collide_with_mobs(self):
        pass

    def collide_with_bullets(self):
        self.live -= 5
        if self.live <= 0:
            self.live = 0
        print(self.live)

    def collide_with_treasure(self):
        self._score += 1

    @property
    def game_object_data(self):
        return create_image_view_data(image_id="player", x=self.rect.x, y=self.rect.y,
                                      width=self.rect.width, height=self.rect.height, angle=(self.angle * math.pi) / 180)

    @property
    def game_init_object_data(self):
        return create_asset_init_data(image_id="player",
                                      width=self.rect.width, height=self.rect.height,
                                      file_path=PLAYER_PATH,
                                      github_raw_url="https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/MyGame/asset/image/player.png")
