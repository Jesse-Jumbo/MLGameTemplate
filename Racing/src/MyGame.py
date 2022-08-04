import random
import pygame

from os import path
from mlgame.game.paia_game import PaiaGame, GameResultState, GameStatus
from mlgame.utils.enum import get_ai_name
from mlgame.view.decorator import check_game_progress, check_game_result
from mlgame.view.view_model import Scene, create_text_view_data, create_scene_progress_data, create_asset_init_data, \
    create_image_view_data

from .Mob import Mob
from .Player import Player
from .Prop import Prop
from .SoundController import SoundController
from .TiledMap import TiledMap
from .Wall import Wall

ASSET_PATH = path.join(path.dirname(__file__), "../asset")
WIDTH = 800
HEIGHT = 600


class MyGame(PaiaGame):
    def __init__(self, user_num=1, frame_limit: int = 300, is_sound: str = "off", map_no: int = None, *args, **kwargs):
        super().__init__(user_num=user_num, *args, **kwargs)
        self.scene = Scene(width=WIDTH, height=HEIGHT, color="#000000", bias_x=0, bias_y=0)
        self.mobs = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.used_frame = 0
        self.frame_to_end = frame_limit
        self.score = 0
        self.is_sound = is_sound
        self.map_no = map_no
        if self.map_no:
            self.map = TiledMap(self.map_no)
        if self.is_sound == "on":
            self.sound_controller = SoundController()

        self.player = Player((WIDTH // 2, 50), (50, 50), pygame.Rect(0, 0, WIDTH, HEIGHT))
        for i in range(random.randrange(1, 10)):
            self._create_mobs(random.randrange(50))
        for i in range(random.randrange(10)):
            wall = Wall((random.randrange(WIDTH-50), random.randrange(HEIGHT-50)), (50, 50))
            self.walls.add(wall)

    def update(self, commands: dict):
        self.used_frame += 1
        self.score = self.player.score
        # handle command
        ai_1p_cmd = commands[get_ai_name(0)]
        if ai_1p_cmd is not None:
            action = ai_1p_cmd
        else:
            action = "NONE"
        # print(ai_1p_cmd)

        # update sprite
        self.player.update(action)
        self.mobs.update()

        # handle collision
        hits = pygame.sprite.spritecollide(self.player, self.walls, False, pygame.sprite.collide_rect_ratio(0.8))
        if hits:
            self.player.collide_with_walls()

        hits = pygame.sprite.spritecollide(self.player, self.mobs, True, pygame.sprite.collide_rect_ratio(0.8))
        if hits:
            self.player.collide_with_mobs()

        if not self.is_running:
            return "RESET"

    def reset(self):
        print("reset MyGame")
        self.__init__(frame_limit=self.frame_to_end, is_sound=self.is_sound, map_no=self.map_no)

    def get_data_from_game_to_player(self):
        """
        send something to MyGame AI
        we could send different data to different ai
        """
        to_players_data = {}
        walls_data = []
        for wall in self.walls:
            if isinstance(wall, Wall):
                walls_data.append({"x": wall.xy[0], "y": wall.xy[1]})
        mobs_data = []
        for mob in self.mobs:
            if isinstance(mob, Mob):
                mobs_data.append({"x": mob.xy[0], "y": mob.xy[1]})
        data_to_1p = {
            "used_frame": self.used_frame,
            "player_x": self.player.xy[0],
            "player_y": self.player.xy[1],
            "walls": walls_data,
            "mobs": mobs_data,
            "score": self.score,
            "status": self.get_game_status()
        }

        to_players_data[get_ai_name(0)] = data_to_1p
        # should be equal to config. GAME_SETUP["ml_clients"][0]["name"]

        return to_players_data

    def get_game_status(self):
        if self.is_running:
            status = GameStatus.GAME_ALIVE
        else:
            status = GameStatus.GAME_OVER
        return status

    @property
    def is_running(self):
        return self.used_frame < self.frame_to_end

    def get_scene_init_data(self):
        """
        Get the initial scene and object information for drawing on the web
        """
        # TODO add music or sound
        bg_path = path.join(ASSET_PATH, "image/mob_0.png")
        background = create_asset_init_data(
            "background", 800, 600, bg_path, "https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/MyGame/asset/image/background.png")
        scene_init_data = {"scene": self.scene.__dict__,
                           "assets": [background],
                           }
        for mob in self.mobs:
            if isinstance(mob, Mob):
                scene_init_data["assets"].append(mob.game_init_object_data)
        scene_init_data["assets"].append(self.player.game_init_object_data)
        return scene_init_data

    @check_game_progress
    def get_scene_progress_data(self):
        """
        Get the position of MyGame objects for drawing on the web
        """
        game_obj_list = []
        for wall in self.walls:
            if isinstance(wall, Wall):
               game_obj_list.append(wall.game_object_data)
        for mob in self.mobs:
            if isinstance(mob, Mob):
                game_obj_list.append(mob.game_object_data)
        game_obj_list.append(self.player.game_object_data)
        backgrounds = [create_image_view_data("background", 0, 0, WIDTH, HEIGHT)]
        foregrounds = [create_text_view_data(
            f"Score123: {str(self.score)}", WIDTH // 1 - 150, 30, "#FF00FF", "24px Arial BOLD")]
        toggle_objs = [create_text_view_data(
            f"Timer456: {str(self.frame_to_end - self.used_frame)} s", WIDTH - 150, 5, "#FFAAAA", "24px Arial")]
        scene_progress = create_scene_progress_data(
            frame=self.used_frame, background=backgrounds,
            object_list=game_obj_list, foreground=foregrounds, toggle=toggle_objs)
        return scene_progress

    @check_game_result
    def get_game_result(self):
        """
        send MyGame result
        """
        if self.get_game_status() == GameStatus.GAME_PASS:
            self.game_result_state = GameResultState.FINISH
            attachment = [
                {
                    "player": get_ai_name(0),
                    "score": self.score,
                    "used_frame": self.used_frame,
                    "status": GameStatus.GAME_PASS
                }
            ]
        else:
            self.game_result_state = GameResultState.FAIL
            attachment = [
                {
                    "player": get_ai_name(0),
                    "score": self.score,
                    "used_frame": self.used_frame,
                    "status": GameStatus.GAME_OVER
                }
            ]

        return {"frame_used": self.used_frame,
                "state": self.game_result_state,
                "attachment": attachment}

    def get_keyboard_command(self):
        """
        Define how your MyGame will run by your keyboard
        """
        cmd_1p = "NONE"
        key_pressed_list = pygame.key.get_pressed()
        if key_pressed_list[pygame.K_UP]:
            cmd_1p = "UP"
        elif key_pressed_list[pygame.K_DOWN]:
            cmd_1p = "DOWN"
        elif key_pressed_list[pygame.K_LEFT]:
            cmd_1p = "LEFT"
        elif key_pressed_list[pygame.K_RIGHT]:
            cmd_1p = "RIGHT"
        return {get_ai_name(0): cmd_1p}

    def _create_mobs(self, count: int = 8):
        for i in range(count):
            mob = Mob(pygame.Rect(0, -100, WIDTH, HEIGHT+100))
            self.mobs.add(mob)
