from enum import auto
from os import path

import pygame
from mlgame.utils.enum import StringEnum
from mlgame.view.view_model import create_asset_init_data, create_image_view_data

PLAYER_PATH = path.join(path.dirname(__file__), "..", "asset", "image", "player.png")


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, size: tuple, play_area_rect: pygame.Rect):
        super().__init__()
        self._play_area_rect = play_area_rect
        self.HP = 100
        self._speed = 8
        self._init_pos = pos
        self.rect = pygame.Rect(*pos, *size)
        self.hit_rect = pygame.Rect(0, 0, self.rect.width - 2, self.rect.height - 2)
        self.hit_rect.center = self.rect.center
        self._score = 0
        self._is_up = False
        self._is_down = False
        self._is_left = False
        self._is_right = False

    def update(self, action: list) -> None:
        self.rect.center = self.hit_rect.center
        if "DOWN" in action and self.rect.bottom < self._play_area_rect.bottom:
            self.move_down()
            self._is_up = False
            self._is_down = True
            self._is_left = False
            self._is_right = False
        elif "UP" in action and self.rect.top > self._play_area_rect.top:
            self.move_up()
            self._is_up = True
            self._is_down = False
            self._is_left = False
            self._is_right = False
        elif "RIGHT" in action and self.rect.right < self._play_area_rect.right:
            self.move_right()
            self._is_left = False
            self._is_up = False
            self._is_down = False
            self._is_right = True
        elif "LEFT" in action and self.rect.left > self._play_area_rect.left:
            self.move_left()
            self._is_right = False
            self._is_left = True
            self._is_up = False
            self._is_down = False

    def move_left(self):
        self.hit_rect.centerx -= self._speed

    def move_right(self):
        self.hit_rect.centerx += self._speed

    def move_up(self):
        self.hit_rect.centery -= self._speed

    def move_down(self):
        self.hit_rect.centery += self._speed

    @property
    def score(self):
        self.score += 10

    @property
    def xy(self):
        return self.rect.topleft

    def reset(self):
        self.rect.topleft = self._init_pos

    def collide_with_walls(self):
        if self._is_up:
            self.move_down()
        elif self._is_down:
            self.move_up()
        elif self._is_left:
            self.move_right()
        elif self._is_right:
            self.move_left()

    def collide_with_mobs(self):
        self.HP -= 5

    def collide_with_bullet(self):
        self.HP -= 2

        # 受到傷害血量減少2

    @property
    def game_object_data(self):
        return create_image_view_data(image_id="player", x=self.rect.x, y=self.rect.y,
                                      width=self.rect.width, height=self.rect.height, angle=0)

    @property
    def game_init_object_data(self):
        return create_asset_init_data(image_id="player",
                                      width=self.rect.width, height=self.rect.height,
                                      file_path=PLAYER_PATH,
                                      github_raw_url="https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/MyGame/asset/image/player.png")
