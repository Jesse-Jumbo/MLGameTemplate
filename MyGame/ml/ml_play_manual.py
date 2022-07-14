import random
import pygame
from mlgame.game.paia_game import GameStatus


class MLPlay:
    def __init__(self, *args, **kwargs):
        print("Initial ml script")

    def update(self, scene_info: dict, keyboard=None, *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        # print("AI received data from MyGame :", json.dumps(scene_info))
        # print(scene_info)
        if keyboard is None:
            keyboard = []

        if scene_info["status"] == GameStatus.GAME_OVER or scene_info["status"] == GameStatus.GAME_PASS:
            return "RESET"

        if pygame.K_w in keyboard or pygame.K_UP in keyboard:
            actions = "UP"
        elif pygame.K_s in keyboard or pygame.K_DOWN in keyboard:
            actions = "DOWN"

        elif pygame.K_a in keyboard or pygame.K_LEFT in keyboard:
            actions = "LEFT"
        elif pygame.K_d in keyboard or pygame.K_RIGHT in keyboard:
            actions = "RIGHT"
        else:
            actions = "NONE"

        return actions

    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
        pass
