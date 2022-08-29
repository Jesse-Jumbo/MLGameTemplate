from enum import auto
from os import path
import math

import pygame
from mlgame.view.view_model import create_asset_init_data, create_image_view_data
from .Wall import Wall
from .Bomb import Bomb

PLAYER_PATH = path.join(path.dirname(__file__), "..", "asset", "image", "player.png")

class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, size: tuple, play_area_rect: pygame.Rect):
        super().__init__()
        self._play_area_rect = play_area_rect
        self._speed = 6
        self._init_pos = pos
        self.rect = pygame.Rect(*pos, 50, 50)
        self._score = 0
        self.live = 100
        self.angle = 0
        self.last_x = self.rect.x
        self.last_y = self.rect.y
        self.used_frame = 0
        self.row = False
        self.x = 0
        self.y = 0
        self.own_bombs = 0

    def update(self, action: list) -> None:
        if self.used_frame % 60 == 0:
            self.live -= 1
        self.used_frame += 1
        self.last_x = self.rect.x
        self.last_y = self.rect.y
        self.x = self.rect.x
        self.y = self.rect.y

        while(self.angle < 0):
            self.angle += 360

        if self.used_frame % 5 == 0:
            self.row = True
        else:
            self.row = False

        if "LEFT" in action and self.row == True:
            self.angle += 90
        if "UP" in action:
            if self.angle % 360 == 0:
                self.move_up()
            elif self.angle % 360 == 90:
                self.move_left()
            elif self.angle % 360 == 180:
                self.move_down()
            else:
                self.move_right()
        if "DOWN" in action:
            if self.angle % 360 == 0:
                self.move_down()
            elif self.angle % 360 == 90:
                self.move_right()
            elif self.angle % 360 == 180:
                self.move_up()
            else:
                self.move_left()
        if "RIGHT" in action and self.row == True:
            self.angle -= 90

    def move_up(self):
        if self.rect.top > self._play_area_rect.top:
            self.rect.centery -= self._speed

    def move_down(self):
        if self.rect.bottom < self._play_area_rect.bottom:
            self.rect.centery += self._speed

    def move_right(self):
        if self.rect.right < self._play_area_rect.right:
            self.rect.centerx += self._speed

    def move_left(self):
        if self.rect.left > self._play_area_rect.left:
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

    def collide_with_treasure(self):
        self._score += 1

    def collide_with_bombs(self):
        self.own_bombs += 1

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
