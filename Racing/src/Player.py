from enum import auto
from os import path

import pygame
from mlgame.utils.enum import StringEnum
from mlgame.view.view_model import create_asset_init_data, create_image_view_data

PLAYER_PATH = path.join(path.dirname(__file__), "..", "asset", "image", "car.png")
PLAYER_UP = path.join(path.dirname(__file__), "..", "asset", "image", "car_up.png")
PLAYER_DOWN = path.join(path.dirname(__file__), "..", "asset", "image", "car_down.png")
PLAYER_RIGHT = path.join(path.dirname(__file__), "..", "asset", "image", "car_right.png")
PLAYER_LEFT = path.join(path.dirname(__file__), "..", "asset", "image", "car_left.png")


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, size: tuple, play_area_rect: pygame.Rect):
        super().__init__()
        self._play_area_rect = play_area_rect
        self.vel = [0, 0]
        self.speed_up = [0, 0]
        self.speed_low = -2
        self._init_pos = pos
        self.rect = pygame.Rect(*pos, *size)
        self._image_id = "car"
        self._score = 0
        self._lives = 100
        self.last_x = self.rect.x
        self.last_y = self.rect.y
        self._image_id = 'car_up'

    def update(self, action: list) -> None:
        self.last_x = self.rect.x
        self.last_y = self.rect.y
        if "UP" in action and self.rect.top > self._play_area_rect.top:
            self.move_up()
            self.vel[1] -= self.speed_up[1]
            self.speed_up[1] += 1
        elif "DOWN" in action and self.rect.bottom < self._play_area_rect.bottom:
            self.move_down()
            self.vel[1] += self.speed_low

        elif "LEFT" in action and self.rect.left > self._play_area_rect.left:
            self.move_left()
            self.vel[0] -= self.speed_up[0]
            self.speed_up[0] += 1
        elif "RIGHT" in action and self.rect.right < self._play_area_rect.right:
            self.move_right()
            self.vel[0] += self.speed_up[0]
            self.speed_up[0] += 1
        else:
            # 這可做慢慢降速
            self.vel = [0, 0]
            self.speed_up[0] -= 2
            self.speed_up[1] -= 2

        if self.speed_up[0] > 15:
            self.speed_up[0] = 15
        elif self.speed_up[1] > 15:
            self.speed_up[1] = 15
        elif self.speed_up[0] < 0:
            self.speed_up[0] = 0
        elif self.speed_up[1] < 0:
            self.speed_up[1] = 0
        self.rect.centerx += self.vel[0]
        self.rect.centery += self.vel[1]

    def move_right(self):
        self._image_id = "car_right"
        self.vel = [5, 0]

    def move_left(self):
        self._image_id = "car_left"
        self.vel = [-5, 0]

    def move_down(self):
        self._image_id = "car_up"
        self.vel = [0, 5]

    def move_up(self):
        self._image_id = "car_up"
        self.vel = [0, -5]

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
        self._lives -= 10

    @property
    def game_object_data(self):
        return create_image_view_data(image_id=self._image_id, x=self.rect.x, y=self.rect.y,
                                      width=self.rect.width, height=self.rect.height, angle=0)

    @property
    def game_init_object_data(self):
        return [create_asset_init_data(image_id="car",
                                       width=self.rect.width, height=self.rect.height,
                                       file_path=PLAYER_PATH,
                                       github_raw_url="https://raw.githubusercontent.com/LiPeggy/GameFramework/main/Racing/asset/image/car.png"),
                create_asset_init_data(image_id="car_up",
                                       width=self.rect.width, height=self.rect.height,
                                       file_path=PLAYER_UP,
                                       github_raw_url="https://raw.githubusercontent.com/LiPeggy/GameFramework/main/Racing/asset/image/car_up.png"),
                create_asset_init_data(image_id="car_down",
                                       width=self.rect.width, height=self.rect.height,
                                       file_path=PLAYER_DOWN,
                                       github_raw_url="https://raw.githubusercontent.com/LiPeggy/GameFramework/main/Racing/asset/image/car_down.png"),
                create_asset_init_data(image_id="car_right",
                                       width=self.rect.width, height=self.rect.height,
                                       file_path=PLAYER_RIGHT,
                                       github_raw_url="https://raw.githubusercontent.com/LiPeggy/GameFramework/main/Racing/asset/image/car_right.png"),
                create_asset_init_data(image_id="car_left",
                                       width=self.rect.width, height=self.rect.height,
                                       file_path=PLAYER_LEFT,
                                       github_raw_url="https://raw.githubusercontent.com/LiPeggy/GameFramework/main/Racing/asset/image/car_left.png"),
                ]
