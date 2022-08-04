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
        action = ""

        if pygame.K_w in keyboard or pygame.K_UP in keyboard:
            action = "UP"
        elif pygame.K_s in keyboard or pygame.K_DOWN in keyboard:
            action = "DOWN"

        elif pygame.K_a in keyboard or pygame.K_LEFT in keyboard:
            action = "LEFT"
        elif pygame.K_d in keyboard or pygame.K_RIGHT in keyboard:
            action = "RIGHT"
        elif pygame.K_f in keyboard:
            action = "SHOOT"
        else:
            action = "NONE"

        return action

    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
        pass
