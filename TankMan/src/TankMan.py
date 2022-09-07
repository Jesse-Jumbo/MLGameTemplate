import pygame

from os import path
from mlgame.view.view_model import Scene
from GameFramework.game_mode.Game import Game

from .TankBattleMode import TankBattleMode
from .env import MAP_DIR, IMAGE_DIR


class TankMan(Game):
    def __init__(self, user_num: int, is_manual: str, map_no: int, frame_limit: int, sound: str):
        super().__init__(user_num, map_no, sound)
        self.frame_limit = frame_limit
        self.is_manual = False
        if is_manual:
            self.is_manual = True
        self.game_mode = self.set_game_mode()
        self.scene = Scene(width=self.game_mode.map_width, height=self.game_mode.map_height + 100, color="#ffffff",
                           bias_y=50)
        self.attachements = []
        pygame.display.set_caption(
            f"TankMan！ user_num: {user_num} ；is_manual: {is_manual} ；map_no: {map_no} ；frame_limit: {frame_limit} ；sound: {sound}")
        pygame.display.set_icon(pygame.image.load(path.join(IMAGE_DIR, "logo.png")))

    def update_game(self, commands: dict):
        pass

    def set_game_mode(self):
        map_path = path.join(MAP_DIR, self.map_name)
        game_mode = TankBattleMode(self.user_num, self.is_manual, map_path, self.frame_limit, self.is_sound)
        return game_mode
