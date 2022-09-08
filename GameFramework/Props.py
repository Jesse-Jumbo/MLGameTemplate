import pygame


vec = pygame.math.Vector2


class Props(pygame.sprite.Sprite):
    def __init__(self, construction: dict, **kwargs):
        """
        初始化物件資料
        construction可直接由TiledMap打包地圖資訊後傳入
        :param construction:
        :param kwargs:
        """
        super().__init__()
        self._id = construction["_id"]
        self._no = construction["_no"]
        self.rect = pygame.Rect(construction["_init_pos"], construction["_init_size"])
        self._origin_xy = self.rect.topleft
        self._origin_center = self.rect.center
        self._angle = 0
        self._used_frame = 0
        self._shield = 100
        self._lives = 3
        self._vel = vec(0, 0)
        self._is_alive = True

    def update(self, *args, **kwargs) -> None:
        """
        更新物件資料
        self._used_frame += 1
        self.rect.center += self._vel
        if self._shield <= 0:
            self._lives -= 1
            self._shield = 100
            self.reset()
        if self._lives <= 0:
            self._is_alive = False
        :param args:
        :param kwargs:
        :return:
        """
        raise Exception("Please overwrite update")

    def reset(self) -> None:
        """
        Reset Prop center = origin_center
        :return:
        """
        self.rect.center = self._origin_center

    def collide_with_walls(self) -> None:
        raise Exception("Please overwrite collide_with_walls")

    def collide_with_bullets(self) -> None:
        raise Exception("Please overwrite collide_with_bullets")

    def collide_with_players(self) -> None:
        raise Exception("Please overwrite collide_with_players")

    def collide_with_mobs(self) -> None:
        raise Exception("Please overwrite collide_with_mobs")

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

    def get_data_from_obj_to_game(self) -> dict:
        """
        在遊戲主程式獲取遊戲資料給AI時被調用
        return {
            "x": self.rect.x,
            "y": self.rect.y
            }
        :return:
        """
        raise Exception("Please overwrite get_data_from_obj_to_game")

    def get_obj_progress_data(self) -> dict or list:
        """
        使用view_model函式，建立符合mlgame物件更新資料格式的資料，在遊戲主程式更新畫面資訊時被調用
        :return:
        """
        raise Exception("Please overwrite get_obj_progress_data")

    def get_obj_init_data(self) -> dict or list:
        """
        使用view_model函式，建立符合mlgame物件初始資料格式的資料，在遊戲主程式初始畫面資訊時被調用
        :return:
        """
        raise Exception("Please overwrite get_obj_progress_data")

    def reset_xy(self, new_pos=()) -> None:
        """
        :param new_pos:
        :return:
        """
        if new_pos:
            self.rect.topleft = new_pos
        else:
            self.rect.topleft = self._origin_xy

