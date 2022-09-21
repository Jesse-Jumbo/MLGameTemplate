from os import path

import pygame
from mlgame.utils.enum import get_ai_name
from mlgame.view.view_model import create_image_view_data, create_asset_init_data

from game_templates.BattleGame.src.env import IMAGE_DIR

Vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, construction: dict, **kwargs):
        """
        初始化玩家資料
        construction可直接由TiledMap打包地圖資訊後傳入
        :param construction:
        :param kwargs:
        """
        super().__init__()
        self.image_id = "1P"
        self.id = construction["_id"]
        self.no = construction["_no"]
        self.rect = pygame.Rect(construction["_init_pos"], construction["_init_size"])
        self.origin_xy = self.rect.topleft
        self.origin_center = self.rect.center
        self.angle = 0
        self.used_frame = 0
        self.vel = Vec(0, 0)
        self.is_alive = True

    def update(self, command: dict) -> None:
        """
        更新玩家資料
        :param command:
        :return:
        """
        self.used_frame += 1
        self.rect.center += self.vel
        self.act(command[self.id])

    def reset(self) -> None:
        """
        Reset Player center = origin_center
        :return:
        """
        self.rect.topleft = self.origin_xy

    def act(self, action: list) -> None:
        pass

    def get_size(self) -> tuple:
        """
        :return: width, height
        """
        return self.rect.width, self.rect.height

    def get_data_from_obj_to_game(self) -> dict:
        """
        在遊戲主程式獲取遊戲資料給AI時被調用
        :return:
        """
        info = {"id": f"{self.id}P",
                "x": self.rect.x,
                "y": self.rect.y,
                "angle": self.angle
                }
        return info

    def get_obj_progress_data(self) -> dict or list:
        """
        使用view_model函式，建立符合mlgame物件更新資料格式的資料，在遊戲主程式更新畫面資訊時被調用
        :return:
        """
        image_data = create_image_view_data(f"{self.id}P", *self.rect.topleft, self.rect.width, self.rect.height, self.angle)
        return image_data

    def get_obj_init_data(self) -> dict or list:
        """
        使用view_model函式，建立符合mlgame物件初始資料格式的資料，在遊戲主程式初始畫面資訊時被調用
        :return:
        """
        image_init_data = create_asset_init_data(f"{self.id}P", self.rect.width, self.rect.height
                                                 , path.join(IMAGE_DIR, f"{self.id}.png"), "url")
        return image_init_data

    def get_info_to_game_result(self):
        info = {"id": f"{self.id}P"
                , "x": self.rect.x
                , "y": self.rect.y
                }
        return info

