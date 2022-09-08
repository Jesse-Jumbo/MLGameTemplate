import pygame

from os import path
from mlgame.game.paia_game import GameResultState, GameStatus
from GameFramework.SoundController import SoundController
from GameFramework.TiledMap import TiledMap
from GameFramework.game_role.Player import Player


class BattleMode:
    def __init__(self, map_path: str, sound_path: str):
        pygame.init()
        self._user_num = 2
        self.sound_path = sound_path
        self.map_path = map_path
        self.map = TiledMap(self.map_path)
        self.map_width = self.map.map_width
        self.map_height = self.map.map_height
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.used_frame = 0
        self.state = GameResultState.FAIL
        self.status = GameStatus.GAME_ALIVE
        self.sound_controller = SoundController(sound_path, self.get_sound_data())
        self.sound_controller.play_music(self.get_bgm_data())
        self.WIDTH_CENTER = self.map.map_width // 2
        self.HEIGHT_CENTER = self.map.map_height // 2

    def update(self, command: dict) -> None:
        raise Exception("Please overwrite update")

    def reset(self) -> None:
        raise Exception("Please overwrite reset")

    def get_background_view_data(self) -> list:
        raise Exception("Please overwrite get_background_view_data")

    def get_obj_progress_data(self) -> list:
        raise Exception("Please overwrite get_obj_progress_data")

    def get_bias_toggle_progress_data(self) -> list:
        raise Exception("Please overwrite get_bias_toggle_progress_data")

    def get_toggle_progress_data(self) -> list:
        raise Exception("Please overwrite get_toggle_progress_data")

    def get_foreground_progress_data(self) -> list:
        raise Exception("Please overwrite get_foreground_progress_data")

    def get_user_info_data(self) -> list:
        raise Exception("Please overwrite get_user_info_data")

    def get_game_sys_info_data(self) -> dict:
        raise Exception("Please overwrite get_game_sys_info_data")

    def get_sound_data(self) -> list:
        if self.sound_path:
            raise Exception("Please overwrite get_music_data")
        return []

    def get_bgm_data(self) -> dict:
        if self.sound_path:
            raise Exception("Please overwrite get_bgm_data")
        return {}

    def draw_players(self) -> list:
        player_data = []
        for player in self.players:
            if isinstance(player, Player):
                player_data.append(player.get_obj_progress_data())

        return player_data

    def debugging(self, is_debug: bool) -> list:
        if is_debug:
            raise Exception("Please over writing debugging")
        return []
