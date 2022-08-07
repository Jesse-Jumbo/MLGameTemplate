import random
from os import path

import pygame
from mlgame.view.view_model import create_asset_init_data, create_image_view_data


MOB_PATH = path.join(path.dirname(__file__), "..", "asset", "image")


class Mob(pygame.sprite.Sprite):
    def __init__(self, play_area_rect: pygame.Rect):
        super().__init__()
        self._play_area_rect = play_area_rect
        self._size = random.choice([(30, 30), (35, 35), (40, 40), (45, 45), (50, 50), (55, 55), (60, 60)])
        self._pos = (random.randrange(0, (800-self._size[1])), random.randrange(60, 120))
        self.rect = pygame.Rect(*self._pos, *self._size)
        self.img_index = random.randrange(0, 2)
        self._image_id = f"mob_{self.img_index}"
        self.image = pygame.image.load(path.join(MOB_PATH, f"{self._image_id}.png"))
        self._x_speed = random.choice([random.randrange(-4, 0), random.randrange(1, 5)])

    def update(self, *args, **kwargs) -> None:
        self.rect.x += self._x_speed

        if self.rect.left <= self._play_area_rect.left:
            is_out = True
        elif self.rect.right >= self._play_area_rect.right:
            is_out = True
        else:
            is_out = False

        if is_out:
            self._x_speed *= -1

    def collide_with_bullets(self):
        self.kill()

    def reset(self):
        self.__init__(self._play_area_rect)

    @property
    def xy(self):
        return self.rect.topleft

    @property
    def game_object_data(self):
        return create_image_view_data(image_id=self._image_id, x=self.rect.x, y=self.rect.y,
                                      width=self.rect.width, height=self.rect.height, angle=0)

    @property
    def game_init_object_data(self):
        return create_asset_init_data(image_id=self._image_id,
                                      width=self.rect.width, height=self.rect.height,
                                      file_path=path.join(MOB_PATH, f"{self._image_id}.png"),
                                      github_raw_url=f"https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/MyGame/asset/image/{self._image_id}.png")
