import random
from os import path

from mlgame.view.view_model import create_asset_init_data, create_image_view_data

from game_module.game_role.Mob import Mob

MOB_PATH = path.join(path.dirname(__file__), "..", "asset", "image")


class SampleMob(Mob):
    def __init__(self, construction: dict, **kwargs):
        super().__init__(construction, **kwargs)
        self._play_area_rect = kwargs["play_area_rect"]
        self._vel.x = random.choice([random.randrange(-4, 0), random.randrange(1, 5)])

    def update(self, *args, **kwargs) -> None:
        self.rect.x += self._vel.x

        if self.rect.left < self._play_area_rect.left:
            is_out = True
        elif self.rect.right > self._play_area_rect.right:
            is_out = True
        else:
            is_out = False

        if is_out:
            self._vel.x *= -1
            self.rect.x += self._vel.x
            self._vel.x = random.choice([random.randrange(-4, 0), random.randrange(1, 5)])

    def collide_with_bullets(self) -> None:
        self.kill()

    def get_obj_progress_data(self) -> dict or list:
        return create_image_view_data(image_id=self._image_id, x=self.rect.x, y=self.rect.y,
                                      width=self.rect.width, height=self.rect.height, angle=0)

    def get_obj_init_data(self) -> dict or list:
        return [
            create_asset_init_data(
                image_id="mob_0"
                , width=self.rect.width
                , height=self.rect.height
                , file_path=path.join(MOB_PATH, f"mob_0.png")
                , github_raw_url=f"https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/MyGame/asset/image/mob_0.png")
            , create_asset_init_data(
                image_id="mob_1"
                , width=self.rect.width
                , height=self.rect.height
                , file_path=path.join(MOB_PATH, f"mob_1.png")
                , github_raw_url=f"https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/MyGame/asset/image/mob_1.png")
        ]

    def get_data_from_obj_to_game(self) -> dict:
        return {"x": self.rect.x, "y": self.rect.y}