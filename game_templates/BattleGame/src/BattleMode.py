import pygame

from os import path
from mlgame.game.paia_game import GameResultState, GameStatus
from mlgame.utils.enum import get_ai_name
from mlgame.view.view_model import create_line_view_data

from game_module.TiledMap import create_construction
from .Player import Player
from .env import WHITE, RED

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
        self.width_center = SCENE_WIDTH // 2
        self.height_center = SCENE_HEIGHT // 2
        self.obj_rect_list = []

    def update(self, command: dict) -> None:
        self.used_frame += 1
        self.players.update(command)
        self.get_player_end()

    def reset(self) -> None:
        self.__init__(self.play_rect_area)

    def get_player_end(self):
        if self.player_1P.is_alive and not self.player_2P.is_alive:
            self.set_result(GameResultState.FINISH, GameStatus.GAME_1P_WIN)
        elif not self.player_1P.is_alive and self.player_2P.is_alive:
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

    def get_init_image_data(self):
        init_image_data = []
        for player in self.players:
            if isinstance(player, Player):
                init_image_data.append(player.get_obj_init_data())
        return init_image_data

    def get_ai_data_to_player(self):
        to_player_data = {}
        num = 0
        competitor_info = {1: self.player_2P.get_data_from_obj_to_game()
                           , 2: self.player_1P.get_data_from_obj_to_game()
                           }
        for player in self.players:
            if isinstance(player, Player):
                to_game_data = player.get_data_from_obj_to_game()
                to_game_data["used_frame"] = self.used_frame
                to_game_data["status"] = self.status
                to_game_data["competitor_info"] = competitor_info
                to_player_data[get_ai_name(num)] = to_game_data
                num += 1

        return to_player_data

    def get_obj_progress_data(self) -> list:
        obj_progress_data = []
        for player in self.players:
            if isinstance(player, Player):
                obj_progress_data.append(player.get_obj_progress_data())
        if self.obj_rect_list:
            obj_progress_data.extend(self.obj_rect_list)

        return obj_progress_data

    def debugging(self, is_debug: bool) -> list:
        self.obj_rect_list = []
        if not is_debug:
            return
        for sprite in self.all_sprites:
            if isinstance(sprite, pygame.sprite.Sprite):
                top_left = sprite.rect.topleft
                points = [top_left, sprite.rect.topright, sprite.rect.bottomright
                    , sprite.rect.bottomleft, top_left]
                for index in range(len(points) - 1):
                    self.obj_rect_list.append(create_line_view_data("rect", *points[index], *points[index + 1], WHITE))

