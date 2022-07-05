import random
from os import path

import pygame
from mlgame.view.view_model import create_asset_init_data, create_image_view_data


MOB_PATH = path.join(path.dirname(__file__), "..", "asset", "image")


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img_index = random.randrange(0, 2)
        self.image = pygame.image.load(path.join(MOB_PATH, f"mob_{self.img_index}.png"))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(0, 400)
        self.rect.centery = random.randrange(-100, -50)
        self.speed_x = random.randrange(-4, 5)
        self.speed_y = random.randrange(4, 8)

    def update(self) -> None:
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

    @property
    def game_object_data(self):
        return create_image_view_data(image_id=f"mob_{self.img_index}", x=self.rect.x, y=self.rect.y,
                                      width=self.rect.width, height=self.rect.height, angle=0)

    @property
    def game_init_object_data(self):
        return create_asset_init_data(image_id=f"mob_{self.img_index}",
                                      width=self.rect.width, height=self.rect.height,
                                      file_path=path.join(MOB_PATH, f"mob_{self.img_index}.png"),
                                      github_raw_url="")
