import random

import pygame


class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        print("Initial BattleGame ml script 1P")
        self.side = ai_name
        self.time = 0

    def update(self, scene_info: dict, *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        # print(scene_info)
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        command = []
        act = random.randrange(5)
        is_shoot = random.randrange(1)
        # debug
        if act == 1:
            command.append("RIGHT")
        elif act == 2:
            command.append("LEFT")
        elif act == 3:
            command.append("UP")
        elif act == 4:
            command.append("DOWN")
        else:
            command.append("NONE")

        if is_shoot == 0:
            command.append("SHOOT")

        return command

    def reset(self):
        """
        Reset the status
        """
        print(f"reset BattleGame {self.side}")
