"""
The game_template of the main script of the machine learning process
"""
import random

import pygame


class MLPlay:
    def __init__(self, ai_name, *args, **kwargs):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.side = ai_name
        print(f"Initial {ai_name} ml script")
        self.time = 0

    def update(self, scene_info: dict, keyboard=[], *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        # print(scene_info)
        # print(keyboard)
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        if scene_info["used_frame"] % 30 == 0:
            act = random.randrange(5)
            is_shoot = random.randrange(2)
        else:
            act = 0
            is_shoot = 0

        command = []
        if self.side == "1P":
            if act == 1:
                command.append("RIGHT")
            elif act == 2:
                command.append("LEFT")
            elif act == 3:
                command.append("UP")
            elif act == 4:
                command.append("DOWN")

            if is_shoot:
                command.append("SHOOT")
        elif self.side == "2P":
            if act == 1:
                command.append("RIGHT")
            elif act == 2:
                command.append("LEFT")
            elif act == 3:
                command.append("UP")
            elif act == 4:
                command.append("DOWN")

            if is_shoot:
                command.append("SHOOT")

        if not command:
            command.append("NONE")

        return command

    def reset(self):
        """
        Reset the status
        """
        print(f"reset {self.side}")
