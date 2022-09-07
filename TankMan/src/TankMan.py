import sys
from os import path

import pygame
from mlgame.game.paia_game import PaiaGame, GameStatus
from mlgame.view.view_model import Scene

from .TankBattleMode import TankBattleMode
from .env import MAP_DIR, IMAGE_DIR

'''need some fuction same as arkanoid which without dash in the name of fuction'''


class TankMan(PaiaGame):
    def __init__(self, user_num: int, is_manual: str, map_no: int, frame_limit: int, sound: str):
        super().__init__(user_num)
        self._user_num = user_num
        self.map_name = f"map_0{map_no}.tmx"
        self.frame_limit = frame_limit
        if sound == "on":
            self.is_sound = True
        else:
            self.is_sound = False
        self.is_manual = is_manual
        self.game_mode = self.set_game_mode()
        self.scene = Scene(width=self.game_mode.map_width, height=self.game_mode.map_height+100, color="#ffffff", bias_y=50)
        self.attachements = []
        pygame.display.set_caption(
            f"TankMan！ user_num: {user_num} ；is_manual: {is_manual} ；map_no: {map_no} ；frame_limit: {frame_limit} ；sound: {sound}")
        pygame.display.set_icon(pygame.image.load(path.join(IMAGE_DIR, "logo.png")))

    def get_data_from_game_to_player(self) -> dict:
        return self.game_mode.create_game_data_to_player()

    @property
    def get_scene_info(self):
        """
        Get the scene information
        """
        scene_info = self.game_mode.create_scene_info()
        return scene_info

    def update(self, commands: dict):
        self.frame_count += 1
        self.game_mode.update(commands)
        if not self.is_running():
            return "RESET"

    def reset(self):
        self.frame_count = 0
        self.game_mode.reset_game()
        self.rank()

    def is_running(self):
        if self.game_mode.status == GameStatus.GAME_ALIVE:
            return True
        else:
            return False

    def get_scene_init_data(self) -> dict:
        """
        Get the scene and object information for drawing on the web
        """
        game_info = {'scene': self.scene.__dict__,
                     'assets': self.game_mode.create_init_image_data()}

        return game_info

    def get_scene_progress_data(self) -> dict:
        """
        Get the position of src objects for drawing on the web
        """

        scene_progress = {'background': [],
                         'object_list': self.game_mode.draw_sprite_data(),
                         'toggle_with_bias': [],
                         'toggle': self.game_mode.draw_toggle_data(),
                         'foreground': self.game_mode.draw_foreground_data(),
                         'user_info': [],
                         'game_sys_info': {}}

        return scene_progress

    def get_game_result(self):
        """
        Get the src result for the web
        """

        return {"frame_used": self.frame_count,
                "state": self.game_result_state,
                "attachment": self.rank()
                }

    def get_keyboard_command(self):
        """
        Get the command according to the pressed keys
        """
        # 此處回傳的資料 要與 ml_play.py 一致
        print(self.is_running())

        if not self.is_running():
            reset_dict = {}
            for i in range(1, len(self.game_mode.playes)+1):
                reset_dict[f"{i}P"] = "RESET"
            return reset_dict

        return self.game_mode.get_act_command()

    def set_game_mode(self):
        map_path = path.join(MAP_DIR, self.map_name)
        game_mode = TankBattleMode(self._user_num, self.is_manual, map_path, self.frame_limit, self.is_sound)
        return game_mode

    def rank(self):
        self.game_result_state = self.game_mode.state
        self.attachements = self.game_mode.get_result()
        return self.attachements

