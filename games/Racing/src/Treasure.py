from os import path

import pygame
from mlgame.view.view_model import create_image_view_data, create_asset_init_data

IMG_PATH = path.join(path.dirname(__file__), "../asset/image")


class Treasure(pygame.sprite.Sprite):
    def __init__(self, construction: dict, **kwargs):
        super().__init__()
        init_pos = construction["x"], construction["y"]
        init_size = construction["width"], construction["height"]
        self.rect = pygame.Rect(*init_pos, *init_size)

    @property
    def xy(self):
        return self.rect.topleft

    @property
    def game_object_data(self):
        return create_image_view_data(image_id="treasure", x=self.rect.x, y=self.rect.y,
                                      width=self.rect.width, height=self.rect.height, angle=0)

    @property
    def game_init_object_data(self):
        return create_asset_init_data(image_id="treasure",
                                      width=self.rect.width, height=self.rect.height,
                                      file_path=path.join(IMG_PATH, "treasure.png"),
                                      github_raw_url=f"https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/MyGame/asset/image/treasure.png")
