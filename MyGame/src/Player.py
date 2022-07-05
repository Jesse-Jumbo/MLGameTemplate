from os import path

import pygame
from mlgame.view.view_model import create_asset_init_data, create_image_view_data


PLAYER_PATH = path.join(path.dirname(__file__), "..", "asset", "image")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.rect = self.image.get_rect()
        self.rect.midbottom = (200, 600)

    def update(self, motion):
        # for motion in motions:
        if motion == "UP":
            self.rect.centery -= 10.5
        elif motion == "DOWN":
            self.rect.centery += 10.5
        elif motion == "LEFT":
            self.rect.centerx -= 10.5
        elif motion == "RIGHT":
            self.rect.centerx += 10.5

    def collide_with_walls(self):
        pass

    def collide_with_mobs(self):
        pass

    @property
    def game_object_data(self):
        return create_image_view_data(image_id="player", x=self.rect.x, y=self.rect.y,
                                      width=self.rect.width, height=self.rect.height, angle=0)

    @property
    def game_init_object_data(self):
        return create_asset_init_data(image_id="player",
                                      width=self.rect.width, height=self.rect.height,
                                      file_path=path.join(PLAYER_PATH, f"player.png"),
                                      github_raw_url="")
