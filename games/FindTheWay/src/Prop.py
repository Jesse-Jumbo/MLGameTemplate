from os import path

import pygame
from mlgame.view.view_model import create_image_view_data, create_asset_init_data

IMG_PATH = path.join(path.dirname(__file__), "../asset/image")


class Prop(pygame.sprite.Sprite):
    def __init__(self, image_id: str, init_pos: tuple, init_size: tuple):
        super().__init__()
        self.rect = pygame.Rect(*init_pos, *init_size)
        self._image_id = image_id

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
                                      file_path=path.join(IMG_PATH, f"{self._image_id}.png"),
                                      github_raw_url=f"https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/MyGame/asset/image/{self._image_id}.png")
