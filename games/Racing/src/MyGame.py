import random
import pygame

from os import path
from mlgame.game.paia_game import PaiaGame, GameResultState, GameStatus
from mlgame.utils.enum import get_ai_name
from mlgame.view.decorator import check_game_progress, check_game_result
from mlgame.view.view_model import Scene, create_text_view_data, create_scene_progress_data, create_asset_init_data, \
    create_image_view_data

from .Bullet import Bullet
from .Mob import Mob
from .Player import Player
from .Prop import Prop
from .SoundController import SoundController
from .TiledMap import TiledMap
from .Treasure import Treasure
from .Wall import Wall

ASSET_PATH = path.join(path.dirname(__file__), "../asset")
WIDTH = 1000
HEIGHT = 600


# class 類別名稱(繼承的類別):
# 這是遊戲的類別，用於建立遊戲的模板
class MyGame(PaiaGame):
    # def 方法名稱(參數: 型態 = 預設值):
    # 定義遊戲的初始化
    def __init__(self, user_num=1, frame_limit: int = 300, is_sound: str = "off", map_no: int = None, *args, **kwargs):
        # super().要繼承的父類別方法的名字(初始化父類別的參數)
        super().__init__(user_num=user_num, *args, **kwargs)
        # 初始化場景(寬, 高, 背景顏色, x軸起始點, y軸起始點)
        self.scene = Scene(width=WIDTH, height=HEIGHT, color="#ffffff", bias_x=0, bias_y=0)
        # 宣告存放多個同類別物件的集合
        self.walls = pygame.sprite.Group()
        self.treasures = pygame.sprite.Group()
        # 宣告變數儲存遊戲中需紀錄的資訊
        self.used_frame = 0
        self.frame_to_end = frame_limit
        self.record = 0
        self.best_record = 0
        self.is_sound = is_sound
        self.map_no = map_no
        # 若有傳入地圖編號和開啟聲音的參數，則建立地圖和音效物件
        if self.map_no:
            self.map = TiledMap(self.map_no)
        if self.is_sound == "on":
            self.sound_controller = SoundController()
        # 建立遊戲物件，並加入該物件的集合
        self.player = Player(pos=(WIDTH // 2, HEIGHT - 50), size=(50, 50),
                             play_area_rect=pygame.Rect(0, 0, WIDTH, HEIGHT))
        walls = self.map.create_init_obj_list(img_no=1, class_name=Wall, color="#000000")
        self.walls.add(*walls)
        treasures = self.map.create_init_obj_list(img_no=2, class_name=Treasure)
        self.treasures.add(*treasures)
        self.sound_controller.play_music(
            music_path=path.join(ASSET_PATH, "sound/Desert Theme.mp3")
            , volume=1)

    # 在這裡將遊戲內所有的物件進行或檢查是否更新（commands={"1P": str}）或檢查程式流程的檢查
    def update(self, commands: dict):
        # 更新已使用的frame
        self.used_frame += 1
        # 更新ＡＩ輸入的指令(command)動作
        ai_1p_cmd = commands[get_ai_name(0)]
        if ai_1p_cmd is not None:
            action = ai_1p_cmd
            if "SHOOT" in ai_1p_cmd:
                self._create_bullets(is_player=True, init_pos=self.player.rect.center)
        else:
            action = "NONE"
        # if self.used_frame % 10 == 0:
        #     for mob in self.mobs:
        #         if isinstance(mob, Mob):
        #             self._create_bullets(is_player=False, init_pos=mob.xy)
        # print(ai_1p_cmd)
        # 更新物件內部資訊
        self.player.update(action)
        self.walls.update()
        # 處理碰撞
        hits = pygame.sprite.spritecollide(self.player, self.walls, False, pygame.sprite.collide_rect_ratio(0.8))
        if hits:
            self.player.collide_with_walls()
        # 玩家和寶藏的碰撞
        hits = pygame.sprite.spritecollide(self.player, self.treasures, False, pygame.sprite.collide_rect_ratio(0.8))
        if hits:
            self.record = self.used_frame
            if self.best_record:
                self.best_record = min(self.record, self.best_record)
            else:
                self.best_record = self.record

        # 判定是否重置遊戲
        if not self.is_running:
            return "RESET"

    # update回傳"RESET"時執行，在這裡定義遊戲重置會執行的內容
    def reset(self):
        print("reset MyGame")
        # super().要繼承的父類別方法的名字(初始化父類別的參數)
        # 初始化場景(寬, 高, 背景顏色, x軸起始點, y軸起始點)
        self.scene = Scene(width=WIDTH, height=HEIGHT, color="#ffffff", bias_x=0, bias_y=0)
        # 宣告存放多個同類別物件的集合
        self.walls = pygame.sprite.Group()
        self.treasures = pygame.sprite.Group()
        # 宣告變數儲存遊戲中需紀錄的資訊
        self.used_frame = 0
        self.frame_to_end = self.frame_to_end
        self.record = 0
        self.is_sound = self.is_sound
        self.map_no = self.map_no
        # 若有傳入地圖編號和開啟聲音的參數，則建立地圖和音效物件
        if self.map_no:
            self.map = TiledMap(self.map_no)
        if self.is_sound == "on":
            self.sound_controller = SoundController()
        # 建立遊戲物件，並加入該物件的集合
        self.player = Player(pos=(WIDTH // 2, HEIGHT - 50), size=(50, 50),
                             play_area_rect=pygame.Rect(0, 0, WIDTH, HEIGHT))
        walls = self.map.create_init_obj_list(img_no=1, class_name=Wall, color="#000000")
        self.walls.add(*walls)
        treasures = self.map.create_init_obj_list(img_no=2, class_name=Treasure)
        self.treasures.add(*treasures)
        self.sound_controller.play_music(
            music_path=path.join(ASSET_PATH, "sound/Desert Theme.mp3")
            , volume=1)

    # 在這裡定義要回傳給ＡＩ哪些資料
    def get_data_from_game_to_player(self):
        """
        send something to MyGame AI
        we could send different data to different ai
        """
        # 一個玩家是key對應一份完整的資料value
        to_players_data = {}
        # 存放一筆筆所有wall的資訊
        walls_data = []
        for wall in self.walls:
            # 確認walls裡的物件是wall這個class的instance
            if isinstance(wall, Wall):
                # 將wall的座標記錄下來
                walls_data.append({"x": wall.xy[0], "y": wall.xy[1]})
        # 將所有要給（AI）玩家1的資料打包起來
        data_to_1p = {
            "used_frame": self.used_frame,
            "player_x": self.player.xy[0],
            "player_y": self.player.xy[1],
            "walls": walls_data,
            "record": self.record,
            "status": self.get_game_status()
        }
        # to_players_data = {"1P": data_to_1p}
        to_players_data[get_ai_name(0)] = data_to_1p
        # should be equal to config. GAME_SETUP["ml_clients"][0]["name"]

        return to_players_data

    # 獲取遊戲狀態的method，在這裡定義遊戲什麼時候是存活、結束、勝利
    def get_game_status(self):
        if self.record:
            status = GameStatus.GAME_PASS
        elif self.is_running:
            status = GameStatus.GAME_ALIVE
        else:
            status = GameStatus.GAME_OVER
        return status

    # 若is_running == False, 重置或結束遊戲
    @property
    def is_running(self):
        if self.record:
            return False
        return self.used_frame < self.frame_to_end

    # 獲取所有遊戲圖片的資訊，在這裡紀錄所有遊戲內圖片的資訊
    def get_scene_init_data(self):
        """
        Get the initial scene and object information for drawing on the web
        """
        # TODO add music or sound
        # 獲取圖片路徑
        bg_path = path.join(ASSET_PATH, "image/white.jpg")
        background = create_asset_init_data(
            image_id="background"
            , width=WIDTH - 50
            , height=HEIGHT - 50
            , file_path=bg_path
            ,
            github_raw_url="https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/MyGame/asset/image/background.png")
        # 定義遊戲圖片初始資料，將場景的屬性，轉化為字典
        # 將所有圖片資訊加入assets裡
        scene_init_data = {"scene": self.scene.__dict__,
                           "assets": [background],
                           }
        for treasure in self.treasures:
            if isinstance(treasure, Treasure):
                scene_init_data["assets"].append(treasure.game_init_object_data)
        scene_init_data["assets"].extend(self.player.game_init_object_data)

        return scene_init_data

    # 獲取所有遊戲畫面的更新資訊
    @check_game_progress
    def get_scene_progress_data(self):
        """
        Get the position of MyGame objects for drawing on the web
        """
        game_obj_list = []
        for wall in self.walls:
            if isinstance(wall, Wall):
                game_obj_list.append(wall.game_object_data)
        for treasure in self.treasures:
            if isinstance(treasure, Treasure):
                game_obj_list.append(treasure.game_object_data)
        game_obj_list.append(self.player.game_object_data)
        backgrounds = [create_image_view_data(image_id="background", x=25, y=50, width=WIDTH - 50, height=HEIGHT - 50)]
        foregrounds = [create_text_view_data(
            content=f"Best Record: {self.best_record}", x=5, y=5, color="#ffffff", font_style="24px Arial")]
        toggle_objs = [create_text_view_data(
            f"Timer: {str(self.frame_to_end - self.used_frame)} s", WIDTH - 150, 5, "#FFA500", "24px Arial BOLD")]
        scene_progress = create_scene_progress_data(
            frame=self.used_frame, background=backgrounds,
            object_list=game_obj_list, foreground=foregrounds, toggle=toggle_objs)
        return scene_progress

    # 遊戲結束或重置前，讀取遊戲結果資料，在這裡定義遊戲結果的資料
    @check_game_result
    def get_game_result(self):
        """
        send MyGame result
        """
        # 定義獲勝的結果
        if self.get_game_status() == GameStatus.GAME_PASS:
            self.game_result_state = GameResultState.FINISH
            attachment = [
                {
                    "player": get_ai_name(0),
                    "record": self.record,
                    "used_frame": self.used_frame,
                    "status": GameStatus.GAME_PASS,
                    "best_record": self.best_record
                }
            ]
        # 定義失敗的結果
        else:
            self.game_result_state = GameResultState.FAIL
            attachment = [
                {
                    "player": get_ai_name(0),
                    "record": self.record,
                    "used_frame": self.used_frame,
                    "status": GameStatus.GAME_OVER,
                    "best_record": self.best_record
                }
            ]

        # 回傳使用時間、遊戲狀態給mlgame並把結果資料（attachment）顯示在terminal
        return {"frame_used": self.used_frame,
                "state": self.game_result_state,
                "attachment": attachment}

    # 這裡由於我們是用ＡＩ玩遊戲，定義在ＡＩ的update即可
    def get_keyboard_command(self):
        """
        Define how your MyGame will run by your keyboard
        """
        pass

    def _create_wall(self):
        wall = self.wall((self.player.x, self.player.y - 50), (50, 50))
        self.walls.add(wall)
