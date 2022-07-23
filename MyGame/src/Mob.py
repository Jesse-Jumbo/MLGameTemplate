import random
from os import path

import pygame
from mlgame.view.view_model import create_asset_init_data, create_image_view_data


MOB_PATH = path.join(path.dirname(__file__), "..", "asset", "image")


class Mob(pygame.sprite.Sprite):
    def __init__(self, play_area_rect: pygame.Rect):
        super().__init__()
        self._play_area_rect = play_area_rect
        self._pos = (random.randrange(-60, 800), random.randrange(-200, -60))
        self._size = random.choice([(30, 30), (35, 35), (40, 40), (45, 45), (50, 50), (55, 55), (60, 60)])
        self.rect = pygame.Rect(*self._pos, *self._size)
        self.img_index = random.randrange(0, 2)
        self._image_id = f"mob_{self.img_index}"
        self.image = pygame.image.load(path.join(MOB_PATH, f"{self._image_id}.png"))
        self._speed = [random.randrange(-4, 5), random.randrange(4, 8)]

    def update(self, *args, **kwargs) -> None:
        self.rect.move_ip(self._speed)

        if self.rect.left >= self._play_area_rect.right:
            is_out = True
        elif self.rect.right <= self._play_area_rect.left:
            is_out = True
        elif self.rect.top >= self._play_area_rect.bottom:
            is_out = True
        elif self.rect.bottom <= self._play_area_rect.top:
            is_out = True
        else:
            is_out = False

        if is_out:
            self.reset()

    def reset(self):
        self._pos = (random.randrange(-60, 800), random.randrange(-200, -60))
        self._size = random.choice([(30, 30), (35, 35), (40, 40), (45, 45), (50, 50), (55, 55), (60, 60)])
        self.rect = pygame.Rect(*self._pos, *self._size)
        self.img_index = random.randrange(0, 2)
        self._image_id = f"mob_{self.img_index}"
        self.image = pygame.image.load(path.join(MOB_PATH, f"{self._image_id}.png"))
        self._speed = [random.randrange(-4, 5), random.randrange(4, 8)]

    @property
    def get_xy(self):
        return self.rect.topleft

    @property
    def get_object_data(self):
        return create_image_view_data(image_id=self._image_id, x=self.rect.x, y=self.rect.y,
                                      width=self.rect.width, height=self.rect.height, angle=0)

    @property
    def get_init_object_data(self):
        return create_asset_init_data(image_id=self._image_id,
                                      width=self.rect.width, height=self.rect.height,
                                      file_path=path.join(MOB_PATH, f"{self._image_id}.png"),
                                      github_raw_url=f"https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/MyGame/asset/image/{self._image_id}.png")
