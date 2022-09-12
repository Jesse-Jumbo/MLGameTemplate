import pygame

from os import path
from mlgame.view.view_model import create_asset_init_data, create_image_view_data


PLAYER_PATH = path.join(path.dirname(__file__), "../asset/image/player.png")
vec = pygame.math.Vector2


class SamplePlayer(Player):
    def __init__(self, construction: dict, **kwargs):
        super().__init__(construction, **kwargs)
        self._play_area_rect = kwargs["play_area_rect"]

    def update(self, command: list) -> None:
        self._used_frame += 1
        self.rect.center += self._vel
        self._vel = vec(0, 0)
        if self._is_alive:
            self.act(command)
        if self._shield <= 0:
            self._lives -= 1
            self._shield = 100
            self.reset()
        if self._lives <= 0:
            self._is_alive = False

    def act(self, action: list) -> None:
        if "UP" in action and self.rect.top > self._play_area_rect.top:
            self.move_up()
        elif "DOWN" in action and self.rect.bottom < self._play_area_rect.bottom:
            self.move_down()
        elif "LEFT" in action and self.rect.left > self._play_area_rect.left:
            self.move_left()
        elif "RIGHT" in action and self.rect.right < self._play_area_rect.right:
            self.move_right()
        if "SHOOT" in action and not self._is_shoot:
            self.shoot()

    def move_right(self) -> None:
        self._vel.x = 10

    def move_left(self) -> None:
        self._vel.x = -10

    def move_down(self) -> None:
        self._vel.y = 10

    def move_up(self) -> None:
        self._vel.y = -10

    def collide_with_mobs(self) -> None:
        self._lives -= 1
        self._shield = 100
        self.reset()

    def collide_with_bullets(self) -> None:
        self._shield -= 10

    def get_obj_progress_data(self) -> dict:
        return create_image_view_data(
            image_id="player"
            , x=self.rect.x
            , y=self.rect.y
            , width=self.rect.width
            , height=self.rect.height
            , angle=0)

    def get_obj_init_data(self) -> dict:
        return create_asset_init_data(
            image_id="player"
            , width=self.rect.width
            , height=self.rect.height
            , file_path=PLAYER_PATH
            , github_raw_url="https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/MyGame/asset/image/player.png")

    def get_data_from_obj_to_game(self) -> dict:
        return {"x": self.rect.x, "y": self.rect.y}
