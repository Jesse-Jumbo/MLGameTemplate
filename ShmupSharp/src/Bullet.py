import pygame
from mlgame.view.view_model import create_rect_view_data

class Bullet(pygame.sprite.Sprite):
    def __init__(self, is_player: bool, init_pos: tuple, play_area_rect: pygame.Rect):
        super().__init__()
        self.rect = pygame.Rect(*init_pos, 5, 4)
        self.is_player = is_player
        self.y_speed = 5
        self.play_area_rect = play_area_rect
        if is_player:
            self.color = "#00ff00"
        else:
            self.color = "#ff0000"

    @property
    def xy(self):
        return self.rect.topleft

    def update(self, *args, **kwargs) -> None:
        #如果子彈整個超出畫面(超出頂端or超出底面),
        if self.is_player:
            self.rect.y -= 10
        else:
            self.rect.y += 10

        if self.rect.top <= self.play_area_rect.top -20:
            is_out = True
        elif self.rect.bottom >= self.play_area_rect.bottom + 20:
            is_out = True
        else:
            is_out = False

        if is_out:
            self.kill()

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
