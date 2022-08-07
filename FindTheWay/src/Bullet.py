import pygame
from mlgame.view.view_model import create_rect_view_data


class Bullet(pygame.sprite.Sprite):
    def __init__(self, is_player: bool, init_pos: tuple, play_area_rect: pygame.Rect):
        super().__init__()
        self._play_area_rect = play_area_rect
        self.rect = pygame.Rect(*init_pos, 8, 8)
        self.is_player = is_player
        self._y_speed = 5
        if is_player:
            self.color = "#ffff00"
        else:
            self.color = "#ff0000"

    def xy(self):
        return self.rect.topleft

    @property
    def game_object_data(self):
        return create_rect_view_data(
            name="bullet"
            , x=self.rect.x
            , y=self.rect.y
            , width=self.rect.width
            , height=self.rect.height
            , color=self.color
            , angle=0)

    def update(self, *args, **kwargs):
        if self.is_player:
            self.rect.y -= self._y_speed
        else:
            self.rect.y += self._y_speed
        is_out = False

        if self.rect.top <= self._play_area_rect.top:
            is_out = True
        elif self.rect.bottom >= self._play_area_rect.bottom:
            is_out = True

        if is_out:
            self.kill()