from os import path

import pygame.key
from mlgame.game.paia_game import PaiaGame, GameStatus
from mlgame.utils.enum import get_ai_name
from mlgame.view.view_model import Scene

from .BattleMode import BattleMode

GAME_DIR = path.dirname(__file__)
MAP_DIR = path.join(GAME_DIR, "..", "asset", 'maps')
SOUND_DIR = path.join(GAME_DIR, "..", "asset", "sound")


class Game(PaiaGame):
    def __init__(self, user_num):
        super().__init__(user_num)
        self.is_paused = False
        self.is_debug = False
        self.is_sound = False
        self.game_mode = self.set_game_mode()
        self.attachements = []

    def get_data_from_game_to_player(self) -> dict:
        to_players_data = self.game_mode.get_ai_data_to_player()
        return to_players_data

    def update(self, commands: dict):
        self.handle_event()
        self.game_mode.debugging(self.is_debug)
        if not self.is_paused:
            self.frame_count += 1
            self.game_mode.update(commands)
            if not self.is_running():
                return "RESET"

    def reset(self):
        self.frame_count = 0
        self.game_mode.reset()
        self.rank()

    def get_scene_init_data(self) -> dict:
        """
        Get the scene and object information for drawing on the web
        """
        game_info = {'scene': self.scene.__dict__,
                     'assets': self.game_mode.get_init_image_data()}

        return game_info

    def get_scene_progress_data(self) -> dict:
        """
        Get the position of src objects for drawing on the web
        """
        scene_progress = {'background': self.game_mode.get_background_view_data(),
                          'object_list': self.game_mode.get_obj_progress_data(),
                          'toggle_with_bias': self.game_mode.get_bias_toggle_progress_data(),
                          'toggle': self.game_mode.get_toggle_progress_data(),
                          'foreground': self.game_mode.get_foreground_progress_data(),
                          'user_info': self.game_mode.get_user_info_data(),
                          'game_sys_info': self.game_mode.get_game_sys_info_data()}

        return scene_progress

    def get_game_result(self):
        """
        Get the src result for the web
        """
        self.rank()
        return {"frame_used": self.frame_count,
                "state": self.game_result_state,
                "attachment": self.attachements
                }

    def is_running(self):
        return self.game_mode.status == GameStatus.GAME_ALIVE

    def set_game_mode(self):
        play_rect_area = pygame.Rect(0, 0, 1000, 600)
        game_mode = BattleMode(play_rect_area)
        return game_mode

    def rank(self):
        self.game_result_state = self.game_mode.state
        self.attachements = self.game_mode.get_player_result()
        return self.attachements

    def handle_event(self):
        key_board_list = pygame.key.get_pressed()
        if key_board_list[pygame.K_b]:
            self.is_debug = not self.is_debug
        if key_board_list[pygame.K_SPACE]:
            self.is_paused = not self.is_paused
