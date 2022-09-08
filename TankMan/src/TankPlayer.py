import pygame.draw
from os import path
from mlgame.view.view_model import create_asset_init_data, create_image_view_data
from .env import WINDOW_WIDTH, WINDOW_HEIGHT, LEFT_CMD, RIGHT_CMD, FORWARD_CMD, BACKWARD_CMD, SHOOT, SHOOT_COOLDOWN, \
    IMAGE_DIR
from GameFramework.game_role.Player import Player
from GameFramework.constants import *

vec = pygame.math.Vector2


class TankPlayer(Player):
    def __init__(self, construction, **kwargs):
        super().__init__(construction, **kwargs)
        self.origin_size = (self.rect.width, self.rect.height)
        self.surface = pygame.Surface((self.rect.width, self.rect.height))
        self.hit_rect = pygame.Rect(0, 0, construction["_init_size"][0]-2, construction["_init_size"][1]-2)
        self.hit_rect.center = self.rect.center
        self.speed = 8
        # TODO refactor use vel
        self.move = {"left_up": vec(-self.speed, -self.speed), "right_up": vec(self.speed, -self.speed),
                     "left_down": vec(-self.speed, self.speed), "right_down": vec(self.speed, self.speed),
                     "left": vec(-self.speed, 0), "right": vec(self.speed, 0), "up": vec(0, -self.speed),
                     "down": vec(0, self.speed)}
        self.rot = 0
        self.last_shoot_frame = self._used_frame
        self.last_turn_frame = self._used_frame
        self.rot_speed = 45
        self.oil = 100
        self.is_turn = False
        self.is_forward = False
        self.is_backward = False
        self.act_cd = kwargs["act_cd"]

    def update(self, actions: list):
        self._used_frame += 1
        self.hit_rect.center = self.rect.center
        self.act(actions)
        if self._lives <= 0:
            self._is_alive = False

        self.rotate()

        if not self.act_cd:
            self.is_turn = False
        elif self._used_frame - self.last_turn_frame > self.act_cd:
            self.is_turn = False

        if self.hit_rect.right > WINDOW_WIDTH+8 or self.hit_rect.left < -8 \
                or self.hit_rect.bottom > WINDOW_HEIGHT+8 or self.hit_rect.top < -8:
            self.collide_with_walls()

    def rotate(self):
        new_sur = pygame.transform.rotate(self.surface, self.rot)
        self.rot = self.rot % 360
        self._angle = 3.14 / 180 * self.rot
        origin_center = self.rect.center
        self.rect = new_sur.get_rect()
        self.rect.center = origin_center

    def act(self, commands: list):
        if not commands:
            return None
        if self._power and SHOOT in commands:
            self.shoot()
        if self.oil <= 0:
            self.oil = 0
            return
        if LEFT_CMD in commands:
            self.oil -= 0.1
            self.turn_left()
        elif RIGHT_CMD in commands:
            self.oil -= 0.1
            self.turn_right()
        elif FORWARD_CMD in commands and BACKWARD_CMD not in commands:
            self.oil -= 0.1
            self.forward()
            self.is_forward = True
            self.is_backward = False
        elif BACKWARD_CMD in commands and FORWARD_CMD not in commands:
            self.oil -= 0.1
            self.backward()
            self.is_backward = True
            self.is_forward = False

    def shoot(self):
        if self.act_cd and self._used_frame - self.last_shoot_frame > SHOOT_COOLDOWN:
            self.last_shoot_frame = self._used_frame
            self._power -= 1
            self._is_shoot = True
        elif not self.act_cd:
            self._power -= 1
            self._is_shoot = True

    def forward(self):
        if self._id != 1:
            rot = self.rot + 180
            if rot >= 360:
                rot -= 360
        else:
            rot = self.rot
        if rot == 0:
            self.rect.center += self.move["left"]
        elif rot == 315:
            self.rect.center += self.move["left_up"]
        elif rot == 270:
            self.rect.center += self.move["up"]
        elif rot == 225:
            self.rect.center += self.move["right_up"]
        elif rot == 180:
            self.rect.center += self.move["right"]
        elif rot == 135:
            self.rect.center += self.move["right_down"]
        elif rot == 90:
            self.rect.center += self.move["down"]
        elif rot == 45:
            self.rect.center += self.move["left_down"]

    def backward(self):
        if self._id != 1:
            rot = self.rot + 180
            if rot >= 360:
                rot -= 360
        else:
            rot = self.rot
        if rot == 0:
            self.rect.center += self.move["right"]
        elif rot == 315:
            self.rect.center += self.move["right_down"]
        elif rot == 270:
            self.rect.center += self.move["down"]
        elif rot == 225:
            self.rect.center += self.move["left_down"]
        elif rot == 180:
            self.rect.center += self.move["left"]
        elif rot == 135:
            self.rect.center += self.move["left_up"]
        elif rot == 90:
            self.rect.center += self.move["up"]
        elif rot == 45:
            self.rect.center += self.move["right_up"]

    def turn_left(self):
        if not self.is_turn:
            self.last_turn_frame = self._used_frame
            self.rot += self.rot_speed
            self.is_turn = True

    def turn_right(self):
        if not self.is_turn:
            self.last_turn_frame = self._used_frame
            self.rot -= self.rot_speed
            self.is_turn = True

    def collide_with_walls(self):
        if self.is_forward:
            self.backward()
        else:
            self.forward()

    def collide_with_bullets(self):
        self._lives -= 1

    def get_power(self, power: int):
        self._power += power
        if self._power > 10:
            self._power = 10
        elif self._power < 0:
            self._power = 0

    def get_oil(self, oil: int):
        self.oil += oil
        if self.oil > 100:
            self.oil = 100
        elif self.oil < 0:
            self.oil = 0

    def get_rot(self):
        if self._id == 2:
            return self.rot + 180
        return self.rot

    def get_data_from_obj_to_game(self) -> dict:
        rot = self.rot
        if self._id != 1:
            rot = self.rot + 180
            if rot >= 360:
                rot -= 360
        info = {"id": f"{self._id}P",
                "x": self.rect.x,
                "y": self.rect.y,
                "speed": self.speed,
                "score": self._score,
                "power": self._power,
                "oil": self.oil,
                "lives": self._lives,
                "angle": rot
                }
        return info

    def get_info_to_game_result(self) -> dict:
        info = {"id": f"{self._id}P",
                "x": self.rect.x,
                "y": self.rect.y,
                "score": self._score,
                "lives": self._lives
                }
        return info

    def get_obj_progress_data(self) -> dict:
        image_data = create_image_view_data(f"{self._id}P", self.rect.x, self.rect.y
                                            , self.origin_size[0], self.origin_size[1], self._angle)
        return image_data

    def get_obj_init_data(self) -> list:
        img_data = {"1P": "https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/1P.svg",
                    "2P": "https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/2P.svg"}
        image_init_data = []
        for id, url in img_data.items():
            image_init_data.append(create_asset_init_data(id, self.origin_size[0], self.origin_size[1],
                                                          path.join(IMAGE_DIR, f"{id}.png"), url))
        return image_init_data
