import pygame

from os import path
from mlgame.view.view_model import Scene
from .template.Game import Game

from .TankBattleMode import TankBattleMode
from .env import MAP_DIR, IMAGE_DIR, SOUND_DIR

MAP_WIDTH = 1000
MAP_HEIGHT = 600


class TankMan(Game):
    def __init__(self, user_num: int, is_manual: str, map_no: int, frame_limit: int, sound: str):
        self.frame_limit = frame_limit
        self.is_manual = False
        if is_manual:
            self.is_manual = True
        super().__init__(user_num, map_no, sound)
        self.scene = Scene(width=self.game_mode.scene_width, height=self.game_mode.scene_height, color="#ffffff",
                           bias_y=50)
        pygame.display.set_caption(
            f"TankMan！ user_num: {user_num} ；is_manual: {is_manual} ；map_no: {map_no} ；frame_limit: {frame_limit} ；sound: {sound}")
        pygame.display.set_icon(pygame.image.load(path.join(IMAGE_DIR, "logo.png")))

    def set_game_mode(self):
        map_path = path.join(MAP_DIR, self.map_name)
        sound_path = ""
        if self.is_sound:
            sound_path = SOUND_DIR
        play_rect_area = pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT)
        game_mode = TankBattleMode(self.is_manual, map_path, self.frame_limit, sound_path, play_rect_area)
        return game_mode
