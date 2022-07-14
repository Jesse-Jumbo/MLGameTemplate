from enum import auto
from os import path

import pygame
from mlgame.utils.enum import StringEnum
from mlgame.view.view_model import create_asset_init_data, create_image_view_data


PLAYER_PATH = path.join(path.dirname(__file__), "..", "asset", "image")


class PlayerAction(StringEnum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    NONE = auto()


class Player(pygame.sprite.Sprite):
    def __init__(self, init_pos: tuple, init_size: tuple, play_area_rect: pygame.Rect, side, *group):
        super().__init__(*group)
        self._play_area_rect = play_area_rect
        self._shift_speed = 5
        self._speed = [0, 0]
        self._init_pos = init_pos
        self.rect = pygame.Rect(*init_pos, *init_size)
        self._score = 0

    @property
    def score(self):
        return self._score

    @property
    def xy(self):
        return self.rect.topleft

    def reset(self):
        self.rect.x, self.rect.y = self._init_pos

    def move(self, move_action: PlayerAction):
        if move_action == PlayerAction.UP and self.rect.top > self._play_area_rect.top:
            self._speed[1] = -self._shift_speed
        elif move_action == PlayerAction.DOWN and self.rect.bottom < self._play_area_rect.bottom:
            self._speed[1] = self._shift_speed
        elif move_action == PlayerAction.LEFT and self.rect.left > self._play_area_rect.left:
            self._speed[0] = -self._shift_speed
        elif move_action == PlayerAction.RIGHT and self.rect.right < self._play_area_rect.right:
            self._speed[0] = self._shift_speed
        else:
            self._speed = [0, 0]

        self.rect.move_ip(*self._speed)

    def collide_with_walls(self):
        pass

    def collide_with_mobs(self):
        pass

    @property
    def get_object_data(self):
        return create_image_view_data(image_id="player", x=self.rect.x, y=self.rect.y,
                                      width=self.rect.width, height=self.rect.height, angle=0)

    @property
    def get_init_object_data(self):
        return create_asset_init_data(image_id="player",
                                      width=self.rect.width, height=self.rect.height,
                                      file_path=path.join(PLAYER_PATH, f"player.png"),
                                      github_raw_url="")
