import pygame

from os import path
from mlgame.game.paia_game import PaiaGame, GameResultState, GameStatus
from mlgame.view.decorator import check_game_progress, check_game_result
from mlgame.view.view_model import Scene, create_text_view_data, create_scene_progress_data

from game.src.Mob import Mob
from game.src.Player import Player

ASSET_PATH = path.join(path.dirname(__file__), "../asset")
WIDTH = 1000
HEIGHT = 700


class FindTheWay(PaiaGame):
    def __init__(self, user_num=1, frame_limit: int = 300, is_sound: str = "off", maps: int = None, *args, **kwargs):
        super().__init__(user_num, *args, **kwargs)
        self.game_result_state = GameResultState.FAIL
        self.scene = Scene(width=WIDTH, height=HEIGHT, color="#000000", bias_x=0, bias_y=0)
        # self.sound_controller = SoundController(sound)
        self.player = Player()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.score = 0
        self._begin_frame = 0
        self._timer = frame_limit
        self.frame_count = 0
        self.frame_limit = frame_limit

    def update(self, commands):
        # handle command
        ai_1p_cmd = commands[self.ai_clients()[0]["name"]][0]
        # print(ai_1p_cmd)
        self.player.update(ai_1p_cmd)

        # update sprite
        self.walls.update()
        self.mobs.update()

        # handle collision
        hits = pygame.sprite.spritecollide(self.player, self.walls, True, pygame.sprite.collide_rect_ratio(0.8))
        if hits:
            self.player.collide_with_walls()

        hits = pygame.sprite.spritecollide(self.player, self.walls, True, pygame.sprite.collide_rect_ratio(0.8))
        if hits:
            self.player.collide_with_mobs()

        self.frame_count += 1
        self._timer = self.frame_limit - self.frame_count
        # self.draw()

        if not self.is_running:
            return "QUIT"

    def get_data_from_game_to_player(self):
        """
        send something to game AI
        we could send different data to different ai
        """
        to_players_data = {}
        walls_data = []
        for wall in self.walls:
            walls_data.append({"x": wall.rect.x, "y": wall.rect.y})
        mobs_data = []
        for mob in self.mobs:
            mobs_data.append({"x": mob.rect.x, "y": mob.rect.y})
        data_to_1p = {
            "frame": self.frame_count,
            "ball_x": self.player.rect.centerx,
            "ball_y": self.player.rect.centery,
            "walls": walls_data,
            "mobs": mobs_data,
            "score": self.score,
            "status": self.get_game_status()
        }

        for ai_client in self.ai_clients():
            to_players_data[ai_client['name']] = data_to_1p
        # should be equal to config. GAME_SETUP["ml_clients"][0]["name"]

        return to_players_data

    def get_game_status(self):

        if self.is_running:
            status = GameStatus.GAME_ALIVE
        else:
            status = GameStatus.GAME_PASS
        return status

    def reset(self):
        pass

    @property
    def is_running(self):
        return self._timer

    def get_scene_init_data(self):
        """
        Get the initial scene and object information for drawing on the web
        """
        # TODO add music or sound
        # bg_path = path.join(ASSET_PATH, "img/background.jpg")
        # background = create_asset_init_data("background", 800, 600, bg_path, "url")
        scene_init_data = {"scene": self.scene.__dict__,
                           "assets": [
                               # background
                           ],
                           # "audios": {}
                           }
        return scene_init_data

    @check_game_progress
    def get_scene_progress_data(self):
        """
        Get the position of game objects for drawing on the web
        """
        walls_data = []
        for wall in self.walls:
            walls_data.append(wall.game_object_data)
        mobs_data = []
        for mob in self.mobs:
            mobs_data.append(mob.game_object_data)
        game_obj_list = [self.player.game_object_data]
        game_obj_list.extend(walls_data)
        game_obj_list.extend(mobs_data)
        backgrounds = []
        foregrounds = [create_text_view_data(f"Score: {str(self.score)}", WIDTH // 2 - 50, 5, "#FF0000", "24px Arial BOLD")]
        toggle_objs = [create_text_view_data(f"Timer: {str(self._timer)} s", WIDTH-100, 5, "#FFAA00", "24px Arial")]
        scene_progress = create_scene_progress_data(frame=self.frame_count, background=backgrounds,
                                                    object_list=game_obj_list,
                                                    foreground=foregrounds, toggle=toggle_objs)
        return scene_progress

    @check_game_result
    def get_game_result(self):
        """
        send game result
        """
        if self.get_game_status() == GameStatus.GAME_PASS:
            self.game_result_state = GameResultState.FINISH
        return {"frame_used": self.frame_count,
                "state": self.game_result_state,
                "attachment": [
                    {
                        "player": self.ai_clients()[0]["name"],
                        "rank": 1,
                        "score": self.score
                    }
                ]

                }

    def get_keyboard_command(self):
        """
        Define how your game will run by your keyboard
        """
        cmd_1p = []
        key_pressed_list = pygame.key.get_pressed()
        if key_pressed_list[pygame.K_UP]:
            cmd_1p.append("UP")
        elif key_pressed_list[pygame.K_DOWN]:
            cmd_1p.append("DOWN")
        elif key_pressed_list[pygame.K_LEFT]:
            cmd_1p.append("LEFT")
        elif key_pressed_list[pygame.K_RIGHT]:
            cmd_1p.append("RIGHT")
        else:
            cmd_1p.append("NONE")
        ai_1p = self.ai_clients()[0]["name"]
        return {ai_1p: cmd_1p}

    def _create_mobs(self, count: int = 8):
        for i in range(count):
            mob = Mob()
            # add mob to group
            self.mobs.add(mob)

    @staticmethod
    def ai_clients():
        """
        let MLGame know how to parse your ai,
        you can also use this names to get different cmd and send different data to each ai client
        """
        return [
            {"name": "1P"}
        ]