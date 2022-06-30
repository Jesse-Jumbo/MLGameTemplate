import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.collide_with_bomb()

    def collide_with_bomb(self):
        pass

    @property
    def game_object_data(self):
        return {"type": "rect",
                "name": "player",
                "x": self.rect.x,
                "y": self.rect.y,
                "angle": 0,
                "width": self.rect.width,
                "height": self.rect.height,
                "color": "#ff0000"
                }