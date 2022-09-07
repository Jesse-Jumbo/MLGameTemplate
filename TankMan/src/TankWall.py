from os import path

import pygame

from GameFramework.Props import Props
from .env import IMAGE_DIR
from mlgame.view.view_model import create_asset_init_data, create_image_view_data


class TankWall(Props):
    def __init__(self, construction, **kwargs):
        super().__init__(construction, **kwargs)
        self.hit_rect = pygame.Rect(0, 0, construction["_init_size"][0] - kwargs["margin"]
                                    , construction["_init_size"][1] - kwargs["spacing"])
        self.hit_rect.center = self.rect.center
        self._lives = 3

    def update(self, *args, **kwargs) -> None:
        self.rect.center = self.hit_rect.center
        if self._lives <= 0:
            self.kill()

    def collide_with_bullets(self):
        if self._lives > 0:
            self._lives -= 1

    def get_lives(self):
        return self._lives

    def get_xy(self):
        return self.rect.x, self.rect.y

    def get_data_from_obj_to_game(self):
        info = {"id": f"wall_{self._lives}", "x": self.rect.x, "y": self.rect.y, "lives": self._lives}
        return info

    def get_obj_progress_data(self):
        if self._lives > 0:
            return create_image_view_data(f"wall_{self._lives}", self.rect.x, self.rect.y,
                                          self.rect.width, self.rect.height, 0)

    def get_obj_init_data(self):
        image_init_data = []
        for i in range(1, 4):
            image_init_data.append(create_asset_init_data(f"wall_{i}", self.rect.width, self.rect.height,
                                                          path.join(IMAGE_DIR, f"wall_{i}.png"), f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/wall_{i}.png"))
        return image_init_data

