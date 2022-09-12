import pygame

from os import path
from mlgame.game.paia_game import GameResultState, GameStatus
from mlgame.utils.enum import get_ai_name

from .SoundController import SoundController, create_bgm_data, create_sounds_data
from .TiledMap import TiledMap, create_construction
from .Player import Player


class BattleMode:
    def __init__(self, map_path: str, sound_path: str, play_rect_area: pygame.Rect):
        pygame.init()
        self._user_num = 2
        self.sound_path = sound_path
        self.map_path = map_path
        self.map = TiledMap(self.map_path)
        self.scene_width = self.map.map_width
        self.scene_height = self.map.map_height
        self.play_rect_area = play_rect_area
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.player_1P = Player(create_construction(get_ai_name(0), 0, (0, 0), (50, 50)))
        self.player_2P = Player(create_construction(get_ai_name(1), 1, (0, 0), (50, 50)))
        self.players.add(self.player_1P)
        self.players.add(self.player_2P)
        self.all_sprites.add(*self.players)
        self.used_frame = 0
        self.state = GameResultState.FAIL
        self.status = GameStatus.GAME_ALIVE
        self.sound_controller = SoundController(sound_path, self.get_sound_data())
        self.sound_controller.play_music(self.get_bgm_data())
        self.WIDTH_CENTER = self.map.map_width // 2
        self.HEIGHT_CENTER = self.map.map_height // 2

    def update(self, command: dict) -> None:
        self.used_frame += 1
        self.players.update(command)
        self.get_player_end()

        raise Exception("Please overwrite update")

    def reset(self) -> None:
        self.__init__(self.map_path,self.sound_path, self.play_rect_area)

        raise Exception("Please overwrite reset")

    def get_player_end(self):
        if self.player_1P.get_is_alive() and not self.player_2P.get_is_alive():
            self.set_result(GameResultState.FINISH, GameStatus.GAME_1P_WIN)
        elif not self.player_1P.get_is_alive() and self.player_2P.get_is_alive():
            self.set_result(GameResultState.FINISH, GameStatus.GAME_2P_WIN)

    def set_result(self, state: str, status: str):
        self.state = state
        self.status = status

    def get_player_result(self) -> list:
        """Define the end of game will return the player's info for user"""
        res = []
        for player in self.players:
            if isinstance(player, Player):
                get_res = player.get_info_to_game_result()
                get_res["state"] = self.state
                get_res["status"] = self.status
                get_res["used_frame"] = self.used_frame
                res.append(get_res)
        return res

    def check_collisions(self):
        raise Exception("Please overwrite check_collisions")

    def get_init_image_data(self):
        init_image_data = []
        return init_image_data

    def get_ai_data_to_player(self):
        to_player_data = {}
        num = 0
        for player in self.players:
            if isinstance(player, Player):
                to_game_data = player.get_data_from_obj_to_game()
                to_game_data["used_frame"] = self.used_frame
                to_game_data["status"] = self.status
                to_game_data["player_info"] = [ai.get_data_from_obj_to_game() for ai in self.players if isinstance(ai, Player)]
                to_player_data[get_ai_name(num)] = to_game_data
                num += 1

        return to_player_data

    def get_background_view_data(self) -> list:
        background_view_data = []
        return background_view_data

    def get_obj_progress_data(self) -> list:
        obj_progress_data = []
        return obj_progress_data

    def get_bias_toggle_progress_data(self) -> list:
        bias_toggle_progress_data = []
        return bias_toggle_progress_data

    def get_toggle_progress_data(self) -> list:
        toggle_data = []
        return toggle_data

    def get_foreground_progress_data(self) -> list:
        foreground_data = []
        return foreground_data

    def get_user_info_data(self) -> list:
        user_info_data = []
        return user_info_data

    def get_game_sys_info_data(self) -> dict:
        game_sys_info_data = {}
        return game_sys_info_data

    def get_bgm_data(self) -> dict:
        bgm_data = {}
        if self.sound_path:
            bgm_data = create_bgm_data("BGM.ogg", 0.1)
            raise Exception("Please overwrite get_bgm_data")
        return bgm_data

    def get_sound_data(self):
        sound_data = []
        if self.sound_path:
            sound_data = [create_sounds_data("shoot", "shoot.wav")
                          , create_sounds_data("touch", "touch.wav")]
            raise Exception("Please overwrite get_sound_data")
        return sound_data

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
