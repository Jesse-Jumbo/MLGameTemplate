import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.rect = self.image.get_rect()
        self.rect.midbottom = (200, 600)

    def update(self, motion):
        # for motion in motions:
        if motion == "UP":
            self.rect.centery -= 10.5
        elif motion == "DOWN":
            self.rect.centery += 10.5
        elif motion == "LEFT":
            self.rect.centerx -= 10.5
        elif motion == "RIGHT":
            self.rect.centerx += 10.5

    def collide_with_walls(self):
        pass

    def collide_with_mobs(self):
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