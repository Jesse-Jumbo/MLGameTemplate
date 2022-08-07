import pygame
from mlgame.view.view_model import create_rect_view_data


class Bullet(pygame.sprite.Sprite):
    def __init__(self, is_player:bool, init_pos: tuple, play_area_rect: pygame.Rect):
        super().__init__()
        self._play_area_rect = play_area_rect
        self.rect = pygame.Rect(*init_pos, 5, 5)
        self.is_player = is_player
        if is_player:
            self.color = "#8c8c8c"
            self.move_y = -10
        else:
            self.color = "#000000"
            self.move_y = 10

    def update(self):
        self.rect.y += self.move_y

        if self.rect.bottom >= self._play_area_rect.bottom:
            is_out = True
        elif self.rect.top <= self._play_area_rect.top:
            is_out = True
        else:
            is_out = False

        if is_out:
            self.kill()

    @property
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
