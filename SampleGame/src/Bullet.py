import pygame
from mlgame.view.view_model import create_rect_view_data


class Bullet(pygame.sprite.Sprite):
    def __init__(self, is_player: bool, init_pos: tuple, play_rect_area: pygame.Rect):
        super().__init__()
        self.rect = pygame.Rect(*init_pos, 8, 8)
        self.play_rect_area = play_rect_area
        self.is_player = is_player
        if is_player:
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
            is_out= False

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








