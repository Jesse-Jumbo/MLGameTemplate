import random

from mlgame.view.view_model import create_rect_view_data
from game_module.Props import Props


class SampleWall(Props):
    def __init__(self, construction: dict, **kwargs):
        super().__init__(construction, **kwargs)
        self.color = "#ff0000"
        self._image_id = kwargs["image_id"]

    def update(self, *args, **kwargs) -> None:
        if self._shield <= 0:
            self.kill()

    def collide_with_bullets(self):
        self._shield -= random.randrange(100)

    def get_data_from_obj_to_game(self) -> dict:
        return {"x": self.rect.x, "y": self.rect.y}

    def get_obj_progress_data(self) -> dict or list:
        return create_rect_view_data(
            name=self._image_id
            , x=self.rect.x
            , y=self.rect.y
            , width=self.rect.width
            , height=self.rect.height
            , color=self.color
            , angle=0)

    def get_obj_init_data(self) -> dict or list:
        pass
