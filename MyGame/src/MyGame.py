import random

import pygame

from os import path
from mlgame.game.paia_game import PaiaGame, GameResultState, GameStatus
from mlgame.utils.enum import get_ai_name
from mlgame.view.decorator import check_game_progress, check_game_result
from mlgame.view.view_model import Scene, create_text_view_data, create_scene_progress_data

from .Mob import Mob
from .Player import Player, PlayerAction
from .SoundController import SoundController
from .TiledMap import TiledMap
from .Wall import Wall

ASSET_PATH = path.join(path.dirname(__file__), "../asset")
WIDTH = 800
HEIGHT = 600


class MyGame(PaiaGame):
    def __init__(self, user_num=1, frame_limit: int = 300, is_sound: str = "off", map_no: int = None, *args, **kwargs):
        super().__init__(user_num=user_num, *args, **kwargs)
        self._timer = frame_limit
        self._is_sound = False
        if is_sound == "on":
            self._is_sound = True
        self._map_no = map_no
        self._score = 0
        self._begin_frame = 0
        self._frame_count = 0
        self._frame_limit = frame_limit
        self._game_status = GameStatus.GAME_ALIVE
        self._mobs = pygame.sprite.Group()
        self._walls = pygame.sprite.Group()
        self.scene = Scene(width=WIDTH, height=HEIGHT, color="#000000", bias_x=0, bias_y=0)
        self._create_init_scene()

    def _create_init_scene(self):
        self._draw_group = pygame.sprite.RenderPlain()

        if self._map_no:
            self.map = TiledMap(self._map_no)
        if self._is_sound:
            self.sound_controller = SoundController()
        self._player_1P = Player((WIDTH//2, 50), (50, 50), pygame.Rect(0, 0, WIDTH, HEIGHT), "1P", self._draw_group)
        for i in range(random.randrange(1, 10)):
            self._create_mobs(random.randrange(50))
        for i in range(random.randrange(10)):
            wall = Wall((random.randrange(WIDTH), random.randrange(HEIGHT)), (50, 50), self._draw_group)
            self._walls.add(wall)

    def update(self, commands: dict):
        self._frame_count += 1
        self._timer = self._frame_limit - self._frame_count
        # handle command
        ai_1p_cmd = commands[get_ai_name(0)]
        # print(ai_1p_cmd)
        if ai_1p_cmd in PlayerAction.__members__:
            command_1P = PlayerAction(ai_1p_cmd)
        else:
            command_1P = PlayerAction.NONE
        # update player
        self._player_1P.move(command_1P)
        for mob in self._mobs:
            mob.move()

        if self.get_game_status() != GameStatus.GAME_ALIVE:
            self._game_status = self.get_game_status()
            self._print_result()
            return "RESET"

        if not self.is_running:
            return "QUIT"

        # handle collision
        hits = pygame.sprite.spritecollide(self._player_1P, self._walls, True, pygame.sprite.collide_rect_ratio(0.8))
        if hits:
            self._player_1P.collide_with_walls()

        hits = pygame.sprite.spritecollide(self._player_1P, self._walls, True, pygame.sprite.collide_rect_ratio(0.8))
        if hits:
            self._player_1P.collide_with_mobs()

    def _game_over(self, status: str):
        """
        Check if the game is over
        :param status:
        :return:
        """
        if status == GameStatus.GAME_OVER or status == GameStatus.GAME_PASS or self._frame_count >= self._frame_limit:
            is_game_over = True
        else:
            is_game_over = False

        return is_game_over

    def _print_result(self):
        """
        Print the result
        :return:
        """
        if self._frame_count >= self._frame_limit:
            print(f"Time Out ! Your Score is {self._score}")

        if not self.is_running:
            return "RESET"

    def get_data_from_game_to_player(self):
        """
        send something to MyGame AI
        we could send different data to different ai
        """
        to_players_data = {}
        walls_data = []
        for wall in self._walls:
            walls_data.append({"x": wall.rect.x, "y": wall.rect.y})
        mobs_data = []
        for mob in self._mobs:
            mobs_data.append({"x": mob.rect.x, "y": mob.rect.y})
        data_to_1p = {
            "frame": self._frame_count,
            "ball_x": self._player_1P.rect.centerx,
            "ball_y": self._player_1P.rect.centery,
            "walls": walls_data,
            "mobs": mobs_data,
            "score": self._score,
            "status": self.get_game_status()
        }

        to_players_data[get_ai_name(0)] = data_to_1p
        # should be equal to config. GAME_SETUP["ml_clients"][0]["name"]

        return to_players_data

    def get_game_status(self):
        if self._frame_count >= self._frame_limit:
            status = GameStatus.GAME_OVER
        elif self.is_running:
            status = GameStatus.GAME_ALIVE
        else:
            status = GameStatus.GAME_PASS
        return status

    def reset(self):
        print("reset MyGame")
        self.__init__()

    @property
    def is_running(self):
        return self._game_status != GameStatus.GAME_OVER

    def get_scene_init_data(self):
        """
        Get the initial scene and object information for drawing on the web
        """
        scene_init_data = {"scene": self.scene.__dict__,
                           "assets": [mob.get_init_object_data for mob in self._mobs],
                           }
        scene_init_data["assets"].append(self._player_1P.get_init_object_data)
        return scene_init_data

    @check_game_progress
    def get_scene_progress_data(self):
        """
        Get the position of MyGame objects for drawing on the web
        """
        walls_data = []
        for wall in self._walls:
            walls_data.append(wall.get_object_data)
        mobs_data = []
        for mob in self._mobs:
            mobs_data.append(mob.get_object_data)
        game_obj_list = [self._player_1P.get_object_data]
        game_obj_list.extend(walls_data)
        game_obj_list.extend(mobs_data)
        backgrounds = []
        foregrounds = [create_text_view_data(f"Score: {str(self._score)}", WIDTH // 2 - 50, 5, "#FF0000", "24px Arial BOLD")]
        toggle_objs = [create_text_view_data(f"Timer: {str(self._timer)} s", WIDTH-150, 5, "#FFAA00", "24px Arial")]
        scene_progress = create_scene_progress_data(frame=self._frame_count, background=backgrounds,
                                                    object_list=game_obj_list,
                                                    foreground=foregrounds, toggle=toggle_objs)
        return scene_progress

    @check_game_result
    def get_game_result(self):
        """
        send MyGame result
        """
        if self.get_game_status() == GameStatus.GAME_PASS:
            attachment = [
                {
                    "player": get_ai_name(0),
                    "score": self._score,
                    "used_frame": self._frame_count,
                    "status": GameStatus.GAME_PASS
                }
            ]
        else:
            attachment = [
                {
                    "player": get_ai_name(0),
                    "score": self._score,
                    "used_frame": self._frame_count,
                    "status": GameStatus.GAME_OVER
                }
            ]

        return {"frame_used": self._frame_count,
                "state": self.game_result_state,
                "attachment": attachment}

    def get_keyboard_command(self):
        """
        Define how your MyGame will run by your keyboard
        """
        cmd_1p = ""
        key_pressed_list = pygame.key.get_pressed()
        if key_pressed_list[pygame.K_UP]:
            cmd_1p = PlayerAction.UP
        elif key_pressed_list[pygame.K_DOWN]:
            cmd_1p = PlayerAction.DOWN
        elif key_pressed_list[pygame.K_LEFT]:
            cmd_1p = PlayerAction.LEFT
        elif key_pressed_list[pygame.K_RIGHT]:
            cmd_1p = PlayerAction.RIGHT
        else:
            cmd_1p = PlayerAction.NONE
        ai_1p = get_ai_name(0)
        return {ai_1p: cmd_1p}

    def _create_mobs(self, count: int = 8):
        for i in range(count):
            mob = Mob(pygame.Rect(0, -100, WIDTH, HEIGHT+100), pygame.sprite.RenderPlain())
            self._mobs.add(mob)