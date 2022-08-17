from mlgame.view.view_model import create_rect_view_data

from GameFramework.Prop import Prop


class SampleBullet(Prop):
    def __init__(self, construction: dict, **kwargs):
        super().__init__(construction, **kwargs)
        self.rect.center = construction["_init_pos"]
        self.play_rect_area = kwargs["play_rect_area"]
        self.is_player = kwargs["is_player"]
        if self.is_player:
            self.color = "#21A1F1"
        else:
            self.color = "#FFA500"

    def update(self):
        if self.is_player:
            self.rect.y -= 10
        else:
            self.rect.y += 10

        if self.rect.bottom <= self.play_rect_area.top:
            is_out = True
        elif self.rect.top >= self.play_rect_area.bottom:
            is_out = True
        else:
            is_out = False

        if is_out:
            self.kill()

    def get_data_from_obj_to_game(self) -> dict:
        return {"x": self.rect.x, "y": self.rect.y}

    def get_obj_progress_data(self):
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
