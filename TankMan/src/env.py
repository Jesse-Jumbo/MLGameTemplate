from os import path

import pygame

# TODO remove width and height setting
'''width and height'''
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

'''environment data'''
FPS = 30
SHOOT_COOLDOWN = FPS // 4

'''color'''
BLACK = "#000000"
WHITE = "#ffffff"
RED = "#ff0000"
YELLOW = "#ffff00"
GREEN = "#00ff00"
DARKGREEN = "#006400"
GREY = "#8c8c8c"
BLUE = "#0000ff"
LIGHT_BLUE = "#21A1F1"
CYAN_BLUE = "#00FFFF"
PINK = "#FF00FF"
DARKGREY = "#282828"
LIGHTGREY = "#646464"
BROWN = "#643705"
FOREST = "#22390A"
MAGENTA = "#FF00FF"
MEDGRAY = "#4B4B4B"
ORANGE =  "#FFA500"

'''command'''
LEFT_CMD = "TURN_LEFT"
RIGHT_CMD = "TURN_RIGHT"
FORWARD_CMD = "FORWARD"
BACKWARD_CMD = "BACKWARD"
SHOOT = "SHOOT"

'''data path'''
GAME_DIR = path.dirname(__file__)
IMAGE_DIR = path.join(GAME_DIR, "..", "asset", "image")
SOUND_DIR = path.join(GAME_DIR, "..", "asset", "sound")
MAP_DIR = path.join(GAME_DIR, "..", "asset", 'maps')

'''BG View'''
TITLE = "TankMan!"
BG_COLOR = DARKGREY
TILE_X_SIZE = 60
TILE_Y_SIZE = 60
TILE_SIZE = 60
TEXT_SIZE = 100

'''object size'''
ALL_OBJECT_SIZE = pygame.Rect(0, 0, 60, 60)
BULLET_SIZE = (13, 13)

"""all setting"""
DOWN_IMG = 'down'
RIGHT_IMG = 'right'
UP_IMG = 'up'
LEFT_IMG = 'left'

"""collide setting"""
WITH_PLAYER = 'player'

"""map data numbers"""
PLAYER_1_IMG_NO = 1
PLAYER_2_IMG_NO = 2
WALL_IMG_NO = 3
BULLET_STATION_IMG_NO = 4
OIL_STATION_IMG_NO = 5

"""music"""
BGM = 'background_music.ogg/.wav/.mp3'
MENU_SND = 'MenuTheme.ogg/.wav/.mp3'

