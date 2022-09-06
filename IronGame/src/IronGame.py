from mlgame.game.paia_game import PaiaGame, GameStatus
from mlgame.utils.enum import get_ai_name
from mlgame.view.view_model import Scene


class IronGame(PaiaGame):
    def __init__(self, user_num=1, *args, **kwargs):
        super().__init__(user_num=user_num, *args, **kwargs)
        self.scene = Scene(width=600, height=800, color="#000000", bias_x=0, bias_y=0)
        self.status = GameStatus.GAME_ALIVE

    def update(self, commands: dict):
        self.frame_count += 1

    def get_data_from_game_to_player(self) -> dict:
        """
        send something to game AI
        we could send different data to different ai
        """
        data_to_player = {}
        data_to_1p = {
            "frame": self.frame_count,
            "status": self.status
        }
        for i in range(self.user_num):
            data_to_player[get_ai_name(i)] = data_to_1p
        return data_to_player

    def reset(self):
        self.__init__()

    def get_scene_init_data(self) -> dict:
        """
        Get the initial scene and object information for drawing on the web
        """
        # TODO add music or sound
        scene_init_data = {"scene": self.scene.__dict__,
                           "assets": []
                           }
        return scene_init_data

    def get_scene_progress_data(self) -> dict:
        """
        Get the position of game objects for drawing on the web
        """

        scene_progress = {
            # background view data will be draw first
            "background": [],
            # game object view data will be draw on screen by order , and it could be shifted by WASD
            "object_list": [],
            "toggle": [],
            "toggle_with_bias": [],
            "foreground": [],
            # other information to display on web
            "user_info": [],
            # other information to display on web
            "game_sys_info": {}
        }
        return scene_progress

    def get_game_result(self) -> dict:
        """
        send game result
        """
        return {"frame_used": self.frame_count,
                "result": {

                },

                }