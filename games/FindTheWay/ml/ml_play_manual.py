import random
import pygame
from mlgame.game.paia_game import GameStatus


class MLPlay:
    def __init__(self, *args, **kwargs):
        print("Initial ml script")

    def update(self, scene_info: dict, keyboard=[], *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        # print("AI received data from MyGame :", json.dumps(scene_info))
        # print(scene_info)
        action = []

        if pygame.K_w in keyboard:
            action.append("UP")
        elif pygame.K_s in keyboard:
            action.append("DOWN")
        elif pygame.K_a in keyboard:
            action.append("LEFT")
        elif pygame.K_d in keyboard:
            action.append("RIGHT")

        if pygame.K_f in keyboard:
            action.append("set_bomb")

        return action

    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
        pass
