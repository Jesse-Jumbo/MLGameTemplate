import random
import pygame

from os import path
from mlgame.game.paia_game import PaiaGame, GameResultState, GameStatus
from mlgame.utils.enum import get_ai_name
from mlgame.view.decorator import check_game_progress, check_game_result
from mlgame.view.view_model import Scene, create_text_view_data, create_scene_progress_data, create_asset_init_data, \
    create_image_view_data

from .Player import Player
from .Prop import Prop
from .SoundController import SoundController
from .TiledMap import TiledMap
from .Wall import Wall
from .Treasure import Treasure
from .Bomb import Bomb

ASSET_PATH = path.join(path.dirname(__file__), "../asset")
WIDTH = 1000
HEIGHT = 600
EXPLOSION_PATH = path.join(path.dirname(__file__), "..", "asset", "image", "explosion.png")


# class 類別名稱(繼承的類別):
# 這是遊戲的類別，用於建立遊戲的模板
class MyGame(PaiaGame):
    # def 方法名稱(參數: 型態 = 預設值):
    # 定義遊戲的初始化
    def __init__(self, user_num=1, frame_limit: int = 300, is_sound: str = "off", map_no: int = None, *args, **kwargs):
        # super().要繼承的父類別方法的名字(初始化父類別的參數)
        super().__init__(user_num=user_num, *args, **kwargs)
        # 初始化場景(寬, 高, 背景顏色, x軸起始點, y軸起始點)
        self.last_explosion_frame = 0
        self.explosion = None
        self.scene = Scene(width=WIDTH, height=HEIGHT, color="#ffffff", bias_x=0, bias_y=0)
        # 宣告存放多個同類別物件的集合
        self.walls = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.treasures = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        # 宣告變數儲存遊戲中需紀錄的資訊
        self.used_frame = 0
        self.frame_to_end = frame_limit
        self.score = 0
        self.is_sound = is_sound
        self.map_no = map_no
        # 若有傳入地圖編號和開啟聲音的參數，則建立地圖和音效物件
        if self.map_no:
            self.map = TiledMap(self.map_no)
        if self.is_sound == "on":
            self.sound_controller = SoundController()
            print(self.sound_controller)
        # 建立遊戲物件，並加入該物件的集合
        self.player = Player(pos=(WIDTH // 2, HEIGHT - 100), size=(50, 50),
                             play_area_rect=pygame.Rect(0, 0, WIDTH, HEIGHT))
        self._set_bomb(1)
        walls = self.map.create_init_obj_list(img_no=1, class_name=Wall, color="#00ff00")
        self.walls.add(*walls)
        treasures = self.map.create_init_obj_list(img_no=82, class_name=Treasure)
        self.treasures.add(*treasures)
        bombs = self.map.create_init_obj_list(img_no=83, class_name=Bomb)
        self.bombs.add(*bombs)
        self.sound_controller.play_music(music_path=path.join(ASSET_PATH, "sound", "BGM.ogg"), volume=0.5)
        self.all_treasures = 8

    # 在這裡將遊戲內所有的物件進行或檢查是否更新（commands={"1P": List}）或檢查程式流程的檢查
    def update(self, commands: dict):
        # 更新已使用的frame
        self.used_frame += 1
        # 更新遊戲的分數
        self.score = self.player.score
        # 更新ＡＩ輸入的指令(command)動作
        ai_1p_cmd = commands[get_ai_name(0)]
        if ai_1p_cmd is not None:
            action = ai_1p_cmd
            if self.used_frame % 6 == 0:
                self.cooldown = True
            else:
                self.cooldown = False
        else:
            action = "NONE"
        # print(ai_1p_cmd)
        # 更新物件內部資訊
        self.player.update(action)
        self.bullets.update()
        self.treasures.update()
        self.bombs.update()
        # 處理碰撞
        hits = pygame.sprite.spritecollide(self.player, self.walls, False, pygame.sprite.collide_rect_ratio(0.8))
        if hits:
            self.player.collide_with_walls()
        hits = pygame.sprite.spritecollide(self.player, self.bullets, False, pygame.sprite.collide_rect_ratio(0.8))
        if hits:
            if hits[0].is_player == False:
                hits[0].kill()
                self.player.collide_with_bullets()
        hits = pygame.sprite.spritecollide(self.player, self.treasures, True, pygame.sprite.collide_rect_ratio(0.8))
        if hits:
            self.all_treasures -= 1
            self.player.collide_with_treasure()
        hits = pygame.sprite.groupcollide(self.bombs, self.walls, True, True, pygame.sprite.collide_rect_ratio(0.8))
        for bomb, walls in hits.items():
            if isinstance(bomb, Bomb):
                bomb.collide_with_walls(self.used_frame)
                self.explosion = self.create_explosion(bomb.xy)
                self.last_explosion_frame = self.used_frame
                self.sound_controller.play_sound(music_path=path.join(ASSET_PATH, "sound", "bomb.wav"), volume=0.5, maz_time=100)
        hits = pygame.sprite.spritecollide(self.player, self.bombs, True, pygame.sprite.collide_rect_ratio(0.8))
        if hits:
            self.player.collide_with_bombs()

        # 判定是否重置遊戲
        if not self.is_running:
            return "RESET"
        if "set_bomb" in action and self.cooldown == True:
            if self.player.own_bombs != 0:
                self._set_bomb(1)
                self.player.own_bombs -= 1

    # update回傳"RESET"時執行，在這裡定義遊戲重置會執行的內容
    # TODO 新增結尾"Game Over"
    def reset(self):
        print("reset MyGame")
        # 重新初始化遊戲
        self.__init__(frame_limit=self.frame_to_end, is_sound=self.is_sound, map_no=self.map_no)

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
            "score": self.score,
            "status": self.get_game_status()
        }
        # to_players_data = {"1P": data_to_1p}
        to_players_data[get_ai_name(0)] = data_to_1p
        # should be equal to config. GAME_SETUP["ml_clients"][0]["name"]

        return to_players_data

    # 獲取遊戲狀態的method，在這裡定義遊戲什麼時候是存活、結束、勝利
    def get_game_status(self):
        if self.is_running:
            status = GameStatus.GAME_ALIVE
        else:
            if self.all_treasures != 0:
                status = GameStatus.GAME_OVER
            else:
                status = GameStatus.GAME_PASS
        return status

    # 若is_running == False, 重置或結束遊戲
    @property
    def is_running(self):
        if self.all_treasures != 0:
            return self.used_frame < self.frame_to_end
        else:
            return False

    # 獲取所有遊戲圖片的資訊，在這裡紀錄所有遊戲內圖片的資訊
    def get_scene_init_data(self):
        """
        Get the initial scene and object information for drawing on the web
        """
        # TODO add music or sound
        # 獲取圖片路徑
        bg_path = path.join(ASSET_PATH, "image/img.png")
        background = create_asset_init_data(
            image_id="background"
            , width=WIDTH
            , height=HEIGHT
            , file_path=bg_path
            ,
            github_raw_url="https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/MyGame/asset/image/background.png")
        # 定義遊戲圖片初始資料，將場景的屬性，轉化為字典
        # 將所有圖片資訊加入assets裡
        scene_init_data = {"scene": self.scene.__dict__,
                           "assets": [background],
                           }
        scene_init_data["assets"].append(self.player.game_init_object_data)
        for treasure in self.treasures:
            if isinstance(treasure, Treasure):
                scene_init_data["assets"].append(treasure.game_init_object_data)
        for bomb in self.bombs:
            if isinstance(bomb, Bomb):
                scene_init_data["assets"].append(bomb.game_init_object_data)
        scene_init_data["assets"].append(create_asset_init_data(image_id="explosion",
                                                                width=50, height=50,
                                                                file_path=EXPLOSION_PATH,
                                                                github_raw_url="https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/MyGame/asset/image/player.png")
                                         )
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
        for bomb in self.bombs:
            if isinstance(bomb, Bomb):
                game_obj_list.append(bomb.game_object_data)
        if self.explosion and self.used_frame - self.last_explosion_frame < 30:
            game_obj_list.append(self.explosion)
        game_obj_list.append(self.player.game_object_data)
        backgrounds = [create_image_view_data(image_id="background", x=25, y=50, width=WIDTH - 50, height=HEIGHT - 50)]
        foregrounds = [create_text_view_data(
            content=f"My_Score: {str(self.score)}", x=WIDTH // 2 - 50, y=5, color="#21A1F1", font_style="35px Arial")]
        foregrounds.append(create_text_view_data(content=f"HP: {str(self.player.live)}", x=0, y=5, color="#21A1F1",
                                                 font_style="35px Arial"))
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
                    "score": self.score,
                    "used_frame": self.used_frame,
                    "status": GameStatus.GAME_PASS
                }
            ]
        # 定義失敗的結果
        else:
            self.game_result_state = GameResultState.FAIL
            attachment = [
                {
                    "player": get_ai_name(0),
                    "score": self.score,
                    "used_frame": self.used_frame,
                    "status": GameStatus.GAME_OVER
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

    # 建立mob物件的method，前面加底線，意指規範此method只供此類別（class）或其實例（instance）呼叫使用

    def _set_bomb(self, count):
        for i in range(count):
            if self.player.angle % 360 == 0:
                bomb = Bomb({"x": self.player.x, "y": self.player.y - 50})
                self.bombs.add(bomb)
            if self.player.angle % 360 == 90:
                bomb = Bomb({"x": self.player.x - 50, "y": self.player.y})
                self.bombs.add(bomb)
            if self.player.angle % 360 == 180:
                bomb = Bomb({"x": self.player.x, "y": self.player.y + 50})
                self.bombs.add(bomb)
            if self.player.angle % 360 == 270:
                bomb = Bomb({"x": self.player.x + 50, "y": self.player.y})
                self.bombs.add(bomb)

    def create_explosion(self, xy: tuple):
        return create_image_view_data(image_id="explosion", x=xy[0], y=xy[1],
                                      width=50, height=50, angle=0)
