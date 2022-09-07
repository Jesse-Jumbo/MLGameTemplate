import pygame.event

from .GameMode import GameMode


class SingleMode(GameMode):
    def __init__(self, map_path: str, frame_limit: int, is_sound: bool):
        super().__init__(map_path, frame_limit, is_sound)
        self.player = pygame.sprite.Sprite
        self.players.add(self.player)

    def get_scene_info(self):
        scene_info = {"frame": self.used_frame,
                      "status": self.status,
                      "background": [1320, 660],
                      "Player_xy_pos": self.player.get_xy_pos(),
                      "game_result": self.get_result(),
                      "state": self.state}

        return scene_info

    def get_game_data_to_player(self):
        to_player_data = {}
        info = self.player.get_info()
        info["used_frame"] = self.used_frame
        info["status"] = self.status

        to_player_data["1P"] = info
        return to_player_data
