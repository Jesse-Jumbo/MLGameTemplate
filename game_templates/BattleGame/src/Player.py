from os import path

import pygame
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
        self._id = construction["_id"]
        self._no = construction["_no"]
        self.rect = pygame.Rect(construction["_init_pos"], construction["_init_size"])
        self._origin_xy = self.rect.topleft
        self._origin_center = self.rect.center
        self._angle = 0
        self._score = 0
        self._used_frame = 0
        self._last_shoot_frame = 0
        self._shield = 100
        self._lives = 3
        self._power = 10
        self._vel = Vec(0, 0)
        self._is_alive = True
        self._is_shoot = False

    def update(self, command: dict) -> None:
        """
        更新玩家資料
        self._used_frame += 1
        self.rect.center += self._vel
        self.act(command[get_ai_name(self._id)])
        if self._shield <= 0:
            self._lives -= 1
            self._shield = 100
            self.reset()
        if self._lives <= 0:
            self._is_alive = False
        :param command:
        :return:
        """
        self.act(command[self._id])

    def reset(self) -> None:
        """
        Reset Player center = origin_center
        :return:
        """
        self.rect.topleft = self._origin_xy

    def act(self, action: list) -> None:
        pass

    def shoot(self) -> None:
        """
        _is_shoot = True
        :return:
        """
        if not self._is_shoot and self._used_frame - self._last_shoot_frame > 10:
            self._last_shoot_frame = self._used_frame
            self._is_shoot = True

    def stop_shoot(self) -> None:
        """
        _is_shoot = False
        :return:
        """
        self._is_shoot = False

    def add_score(self, score: int) -> None:
        """
        _score += score
        :param score:
        :return:
        """
        self._score += score

    def get_score(self) -> int:
        """
        :return: _score
        """
        return self._score

    def get_lives(self) -> int:
        """
        :return: _lives
        """
        return self._lives

    def get_shield(self) -> int:
        """
        :return: _shield
        """
        return self._shield

    def get_is_alive(self) -> bool:
        """
        :return: _is_alive
        """
        return self._is_alive

    def get_is_shoot(self) -> bool:
        """
        :return: _is_shoot
        """
        return self._is_shoot

    def set_is_shoot(self, is_shoot: bool) -> None:
        """
        _is_shoot = is_shoot
        :param is_shoot:
        :return:
        """
        self._is_shoot = is_shoot

    def reset_xy(self, new_pos=()) -> None:
        """
        :param new_pos:
        :return:
        """
        if new_pos:
            self.rect.topleft = new_pos
        else:
            self.rect.topleft = self._origin_xy

    def get_xy(self) -> tuple:
        """
        :return: topleft
        """
        return self.rect.topleft

    def get_size(self) -> tuple:
        """
        :return: width, height
        """
        return self.rect.width, self.rect.height

    def get_center(self) -> tuple:
        """
        :return: center
        """
        return self.rect.center

    def get_id(self) -> int:
        """
        :return: center
        """
        return self._id

    def get_data_from_obj_to_game(self) -> dict:
        """
        在遊戲主程式獲取遊戲資料給AI時被調用
        :return:
        """
        info = {"id": f"{self._id}P",
                "x": self.rect.x,
                "y": self.rect.y,
                "angle": self._angle
                }
        return info

    def get_obj_progress_data(self) -> dict or list:
        """
        使用view_model函式，建立符合mlgame物件更新資料格式的資料，在遊戲主程式更新畫面資訊時被調用
        :return:
        """
        image_data = create_image_view_data(f"{self._id}P", *self.rect.topleft, self.rect.width, self.rect.height, self._angle)
        return image_data

    def get_obj_init_data(self) -> dict or list:
        """
        使用view_model函式，建立符合mlgame物件初始資料格式的資料，在遊戲主程式初始畫面資訊時被調用
        :return:
        """
        image_init_data = create_asset_init_data(f"{self._id}P", self.rect.width, self.rect.height
                                                 , path.join(IMAGE_DIR, f"{self._id}.png"), "url")
        return image_init_data

    def get_info_to_game_result(self):
        info = {"id": f"{self._id}P"
                , "x": self.rect.x
                , "y": self.rect.y
                }
        return info

