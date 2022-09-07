import pygame.sprite

from .env import *


def collide_hit_rect(one: pygame.sprite, two: pygame.sprite):
    return one.hit_rect.colliderect(two.hit_rect)


def collide_with_walls(group1: pygame.sprite.Group, group2: pygame.sprite.Group):
    hits = pygame.sprite.groupcollide(group1, group2, False, False, collide_hit_rect)
    for sprite, walls in hits.items():
        sprite.collide_with_walls()


def collide_with_bullets(group1: pygame.sprite.Group, group2: pygame.sprite.Group):
    hits = pygame.sprite.groupcollide(group1, group2, False, False, collide_hit_rect)
    for sprite, bullets in hits.items():
        for bullet in bullets:
            if bullet._id != sprite._id:
                bullet.kill()
                score = 1
                if sprite.get_lives() == 1:
                    score += 5
                sprite.collide_with_bullets()
                return bullet._id, score
    return None, None


def collide_with_bullet_stations(player: pygame.sprite.Group, stations: pygame.sprite.Group):
    hits = pygame.sprite.groupcollide(player, stations, False, False, collide_hit_rect)
    for player, stations in hits.items():
        player.get_power(stations[0].get_supply())
        return stations


def collide_with_oil_stations(player: pygame.sprite.Group, stations: pygame.sprite.Group):
    hits = pygame.sprite.groupcollide(player, stations, False, False, collide_hit_rect)
    for player, stations in hits.items():
        player.get_oil(stations[0].get_supply())
        return stations
