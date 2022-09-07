import pygame
from os import path
from mlgame.view.view_model import create_asset_init_data, create_image_view_data

from GameFramework.Props import Props
from .env import WINDOW_HEIGHT, WINDOW_WIDTH, IMAGE_DIR

vec = pygame.math.Vector2


class TankBullet(Props):
    def __init__(self, construction, **kwargs):
        super().__init__(construction, **kwargs)
        self.rect.center = construction["_init_pos"]
        self.hit_rect = pygame.Rect(0, 0, construction["_init_size"][0] - kwargs["margin"]
                                    , construction["_init_size"][1] - kwargs["spacing"])
        self.hit_rect.center = self.rect.center
        self.speed = 10
        self.map_height = 0
        self.map_width = 0
        self._angle = 0

        self.map_width = WINDOW_WIDTH
        self.map_height = WINDOW_HEIGHT
        self.rot = kwargs["rot"]
        self._angle = 3.14 / 180 * (self.rot + 90)
        self.move = {"left_up": vec(-self.speed, -self.speed), "right_up": vec(self.speed, -self.speed),
                     "left_down": vec(-self.speed, self.speed), "right_down": vec(self.speed, self.speed),
                     "left": vec(-self.speed, 0), "right": vec(self.speed, 0), "up": vec(0, -self.speed),
                     "down": vec(0, self.speed)}

    def update(self):
        self.hit_rect.center = self.rect.center

        if self.rect.bottom < 0 or self.rect.top > self.map_height \
                or self.rect.left > self.map_width or self.rect.right < 0:
            self.kill()

        if self.rot == 0 or self.rot == 360:
            self.rect.center += self.move["left"]
        elif self.rot == 315 or self.rot == -45:
            self.rect.center += self.move["left_up"]
        elif self.rot == 270 or self.rot == -90:
            self.rect.center += self.move["up"]
        elif self.rot == 225 or self.rot == -135:
            self.rect.center += self.move["right_up"]
        elif self.rot == 180 or self.rot == -180:
            self.rect.center += self.move["right"]
        elif self.rot == 135 or self.rot == -225:
            self.rect.center += self.move["right_down"]
        elif self.rot == 90 or self.rot == -270:
            self.rect.center += self.move["down"]
        elif self.rot == 45 or self.rot == -315:
            self.rect.center += self.move["left_down"]

    def get_obj_init_data(self):
        url = "https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/bullet.png"
        image_init_data = create_asset_init_data("bullet", self.rect.width, self.rect.height, path.join(IMAGE_DIR, "bullet.png"), url)
        return image_init_data

    def get_obj_progress_data(self):
        return create_image_view_data("bullet", self.rect.x, self.rect.y, self.rect.width, self.rect.height, self._angle)

    def get_data_from_obj_to_game(self) -> dict:
        info = {"id": f"{self._id}P_bullet",
                "x": self.rect.x,
                "y": self.rect.y,
                "speed": self.speed,
                "rot": self.rot
                }
        return info
