"""
The template of the main script of the machine learning process
"""
import random

import pygame


class MLPlay:
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.side = side
        print(f"Initial TankMan {side} ml script")
        self.time = 0

    def update(self, scene_info: dict, keyboard=[], *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        # print(scene_info)
        # print(keyboard)
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        if scene_info["used_frame"] % 120 == 0:
            act = random.randrange(10)
        else:
            act = 10

        command = []
        if self.side == "1P":
            if act == 1:
                command.append("TURN_RIGHT")
            elif act == 2:
                command.append("TURN_LEFT")
            elif act == 3:
                command.append("FORWARD")
            elif act == 4:
                command.append("BACKWARD")
            elif act == 0:
                command.append("SHOOT")
            elif act == 5:
                command.append("TURN_RIGHT")
                command.append("SHOOT")
            elif act == 6:
                command.append("TURN_LEFT")
                command.append("SHOOT")
            elif act == 7:
                command.append("FORWARD")
                command.append("SHOOT")
            elif act == 8:
                command.append("BACKWARD")
                command.append("SHOOT")
            elif act == 9:
                command.append("SHOOT")

        return command

    def reset(self):
        """
        Reset the status
        """
        print(f"reset TankMan {self.side}")
