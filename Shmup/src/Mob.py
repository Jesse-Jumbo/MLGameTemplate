import random

import pygame


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        width = random.randrange(30, 50)
        height = random.randrange(30, 50)
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(0, 400)
        self.rect.centery = random.randrange(-100, -50)
        self.speed_x = random.randrange(-4, 5)
        self.speed_y = random.randrange(4, 8)

    def update(self) -> None:
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

    @property
    def game_object_data(self):
        return {"type": "rect",
                "name": "mob",
                "x": self.rect.x,
                "y": self.rect.y,
                "angle": 0,
                "width": self.rect.width,
                "height": self.rect.height,
                "color": "#ffffff"
                }
