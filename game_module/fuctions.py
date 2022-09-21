import pygame.sprite


def get_size(sprite: pygame.sprite.Sprite):
    return sprite.rect.width, sprite.rect.height


def set_topleft(sprite: pygame.sprite.Sprite, top_left: tuple):
    sprite.rect.topleft = top_left


def add_score(sprite: pygame.sprite.Sprite, score: int):
    sprite.score += score


def set_shoot(sprite: pygame.sprite.Sprite, is_shoot: bool):
    sprite.is_shoot = is_shoot


def get_sprites_progress_data(sprites: pygame.sprite.Group):
    data = []
    for sprite in sprites:
        data.append(sprite.get_obj_progress_data())
    return data
