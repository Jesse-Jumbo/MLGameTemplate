from os import path

import pygame
from mlgame.game.paia_game import GameResultState, GameStatus

from GameFramework.SoundController import SoundController
from GameFramework.TiledMap import TiledMap


class BattleMode:
    def __init__(self, map_path: str, sound_path: str):
        pygame.init()
        self._user_num = 2
        self.map_path = map_path
        self.map = TiledMap(self.map_path)
        self.map_width = self.map.map_width
        self.map_height = self.map.map_height
        self.is_paused = False
        self.is_debug = False
        self.sound_path = sound_path
        self.all_sprites = pygame.sprite.Group()
        self.used_frame = 0
        self.state = GameResultState.FAIL
        self.status = GameStatus.GAME_ALIVE
        self.players = pygame.sprite.Group()
        self.sound_controller = SoundController(sound_path, self.get_music_data())
        self.sound_controller.play_music("BGM.ogg", 0.1)
        self.WIDTH_CENTER = self.map.map_width // 2
        self.HEIGHT_CENTER = self.map.map_height // 2


    def get_background_view_data(self):
        return []

    def get_obj_progress_data(self):
        return []

    def get_bias_toggle_progress_data(self):
        return []

    def get_toggle_progress_data(self):
        return []

    def get_foreground_progress_data(self):
        return []

    def get_user_info_data(self):
        return []

    def get_game_sys_info_data(self):
        return {}
