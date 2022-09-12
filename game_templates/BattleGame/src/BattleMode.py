import pygame

from os import path
from mlgame.game.paia_game import GameResultState, GameStatus
from mlgame.utils.enum import get_ai_name

from game_module.TiledMap import create_construction
from .Player import Player


SCENE_WIDTH = 800
SCENE_HEIGHT = 600


class BattleMode:
    def __init__(self, play_rect_area: pygame.Rect):
        pygame.init()
        self._user_num = 2
        self.scene_width = SCENE_WIDTH
        self.scene_height = SCENE_HEIGHT
        self.play_rect_area = play_rect_area
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.player_1P = Player(create_construction(get_ai_name(0), 0, (0, 0), (50, 50)))
        self.player_2P = Player(create_construction(get_ai_name(1), 1, (SCENE_WIDTH-50, SCENE_HEIGHT-50), (50, 50)))
        self.players.add(self.player_1P)
        self.players.add(self.player_2P)
        self.all_sprites.add(*self.players)
        self.used_frame = 0
        self.state = GameResultState.FAIL
        self.status = GameStatus.GAME_ALIVE
        self.WIDTH_CENTER = SCENE_WIDTH // 2
        self.HEIGHT_CENTER = SCENE_HEIGHT // 2

    def update(self, command: dict) -> None:
        self.used_frame += 1
        self.players.update(command)
        self.get_player_end()

    def reset(self) -> None:
        self.__init__(self.play_rect_area)

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
        init_image_data = [self.player_1P.get_obj_init_data()
                           , self.player_2P.get_obj_init_data()]
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
        obj_progress_data = self.draw_players()
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
