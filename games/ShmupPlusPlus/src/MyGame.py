import random
import pygame

from os import path
from mlgame.game.paia_game import PaiaGame, GameResultState, GameStatus
from mlgame.utils.enum import get_ai_name
from mlgame.view.decorator import check_game_progress, check_game_result
from mlgame.view.view_model import Scene, create_text_view_data, create_scene_progress_data, create_asset_init_data, \
    create_image_view_data

from .Mob import Mob
from .Player import Player
from .Prop import Prop
from .SoundController import SoundController
from .TiledMap import TiledMap
from .Wall import Wall
from .Bullet import Bullet

ASSET_PATH = path.join(path.dirname(__file__), "../asset")
WIDTH = 1000
HEIGHT = 600


def collide_hit_rect(one: pygame.sprite, two: pygame.sprite):
    return one.rect.colliderect(two.hit_rect)
# class 類別名稱(繼承的類別):
# 這是遊戲的類別，用於建立遊戲的模板
# def bullet(pos, size, play_area_rect):
#  pass


class MyGame(PaiaGame):
    # def 方法名稱(參數: 型態 = 預設值):
    # 定義遊戲的初始化
    def __init__(self, user_num=1, frame_limit: int = 300, target_score: int = 500, is_sound: str = "off", map_no: int = None, *args, **kwargs):
        # super().要繼承的父類別方法的名字(初始化父類別的參數)
        super().__init__(user_num=user_num, *args, **kwargs)
        # 初始化場景(寬, 高, 背景顏色, x軸起始點, y軸起始點)
        self.scene = Scene(width=WIDTH, height=HEIGHT, color="#ffffff", bias_x=0, bias_y=0)
        # 宣告存放多個同類別物件的集合
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        # 宣告變數儲存遊戲中需紀錄的資訊
        self.used_frame = 0
        self.frame_to_end = frame_limit
        self.score = 0
        self.target_score = target_score
        self.is_sound = is_sound
        self.map_no = map_no
        # 若有傳入地圖編號和開啟聲音的參數，則建立地圖和音效物件
        if self.map_no:
            self.map = TiledMap(self.map_no)
        if self.is_sound == "on":
            self.sound_controller = SoundController()
            # 播出聲音
            self.sound_controller.play_music(
                music_path=path.join(ASSET_PATH, "sound", "music1.mp3")
                , volume=0.5)
        # 建立遊戲物件，並加入該物件的集合
        self.player = Player(pos=(WIDTH // 2, HEIGHT - 80), size=(50, 50),
                             play_area_rect=pygame.Rect(0, 0, WIDTH, HEIGHT))
        # self.Bullets = Bullet(is_player=False, init_pos=self.rect.center, play_area_rect=pygame.Rect(0, 0, WIDTH, HEIGHT))
        for i in range(random.randrange(1, 3)):
            self._create_mobs(random.randrange(50))
        for i in range(3):
            wall = Wall(init_pos=(random.randrange(WIDTH - 50), random.randrange(190, 230)), init_size=(90, 45))
            self.walls.add(wall)


    # 在這裡將遊戲內所有的物件進行或檢查是否更新（commands={"1P": list}）或檢查程式流程的檢查
    def update(self, commands: dict):  # update 更新
        # 更新已使用的frame
        self.used_frame += 1
        # 更新遊戲的分數
        self.score = self.player._score
        # 更新ＡＩ輸入的指令(command)動作
        ai_1p_cmd = commands[get_ai_name(0)]
        if ai_1p_cmd is not None:
            action = ai_1p_cmd
            if "Shoot" in ai_1p_cmd:
                self._create_bullet(is_player=True, init_pos=self.player.rect.center)
        else:
            action = ["NONE"]
        # print(ai_1p_cmd)

        # 讓mob不會只出現在開局
        if len(self.mobs) < 20:
            self._create_mobs(10)

        # 每秒子彈速度
        if self.used_frame % 50 == 0:
            # 怪物的子彈
            for mob in self.mobs:
                if isinstance(mob, Mob):
                    self._create_bullet(is_player=False, init_pos=mob.rect.center)

        # 更新物件內部資訊
        self.player.update(action)
        self.mobs.update()
        self.bullets.update()

        # 處理碰撞
        # 玩家and牆
        hits = pygame.sprite.spritecollide(self.player, self.walls, False, pygame.sprite.collide_rect_ratio(0.8))
        if hits:
            self.player.collide_with_walls()
        # 子彈和牆
        hits = pygame.sprite.groupcollide(self.bullets, self.walls, True, False, pygame.sprite.collide_rect_ratio(0.8))

        # 玩家and怪物
        hits = pygame.sprite.spritecollide(self.player, self.mobs, True, pygame.sprite.collide_rect_ratio(0.8))
        if hits:
            self.player.collide_with_mobs()  # 玩家碰到怪物
        # 玩家and子彈
        hits = pygame.sprite.spritecollide(self.player, self.bullets, False, pygame.sprite.collide_rect_ratio(0.8))
        for hit in hits:
            if not hits[0].is_player:  # 不是玩家子彈
                hit.kill()  # 刪除子彈
                # 玩家碰到怪物子彈 玩家消失 怪物碰到子彈 safe
                self.player.collide_with_bullets()
        # 怪物and子彈
        hits = pygame.sprite.groupcollide(self.mobs, self.bullets, False, False, pygame.sprite.collide_rect_ratio(0.8))
        for mob, bullet in hits.items():
            if bullet[0].is_player:
                self.score += 10
                mob.kill()
                bullet[0].kill()
                self.player.bullets_with_mobs()
        # wall and bullet
        hits = pygame.sprite.spritecollide(self.player, self.walls, False, collide_hit_rect)
        if hits:
            self.player.collide_with_walls()
            # print(bullet)
        # if hits:        #是玩家子彈
        #     self.mods.collide_with_player()  #怪物碰子彈怪物消失 玩家碰到子彈safe

        if not self.is_running:
            return "RESET"

    # update回傳"RESET"時執行，在這裡定義遊戲重置會執行的內容
    def reset(self):
        print("reset MyGame")
        # 重新初始化遊戲
        self.__init__(frame_limit=self.frame_to_end, is_sound=self.is_sound)

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
        mobs_data = []
        for mob in self.mobs:
            if isinstance(mob, Mob):
                mobs_data.append({"x": mob.xy[0], "y": mob.xy[1]})
        # 將所有要給（AI）玩家1的資料打包起來
        data_to_1p = {
            "used_frame": self.used_frame,
            "player_x": self.player.xy[0],
            "player_y": self.player.xy[1],
            "walls": walls_data,
            "mobs": mobs_data,
            "score": self.score,
            "status": self.get_game_status()
        }
        # to_players_data = {"1P": data_to_1p}
        to_players_data[get_ai_name(0)] = data_to_1p
        # should be equal to config. GAME_SETUP["ml_clients"][0]["name"]

        return to_players_data

    # 獲取遊戲狀態的method，在這裡定義遊戲什麼時候是存活、結束、勝利
    def get_game_status(self):
        if self.player.HP <= 0:
            status = GameStatus.GAME_OVER
        elif self.score >= self.target_score:
            status = GameStatus.GAME_PASS
        else:
            status = GameStatus.GAME_ALIVE
        return status

    # 若is_running == False, 重置或結束遊戲
    @property
    def is_running(self):
        if self.player.HP <= 0:
            return False
        elif self.player.score > self.target_score:
            return False
        return self.used_frame < self.frame_to_end

    # 獲取所有遊戲圖片的資訊，在這裡紀錄所有遊戲內圖片的資訊
    def get_scene_init_data(self):
        """
        Get the initial scene and object information for drawing on the web
        """
        # TODO add music or sound
        # 獲取圖片路徑
        bg_path = path.join(ASSET_PATH, "image/stone 1.png")
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
        for mob in self.mobs:
            if isinstance(mob, Mob):
                scene_init_data["assets"].append(mob.game_init_object_data)
        scene_init_data["assets"].append(self.player.game_init_object_data)
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
        for bullet in self.bullets:
            if isinstance(bullet, Bullet):
                game_obj_list.append(bullet.game_object_data)
        for mob in self.mobs:
            if isinstance(mob, Mob):
                game_obj_list.append(mob.game_object_data)
        game_obj_list.append(self.player.game_object_data)
        backgrounds = [create_image_view_data(image_id="background", x=20, y=20, width=WIDTH - 50, height=HEIGHT - 50)]
        foregrounds = [create_text_view_data(
            content=f"Score: {str(self.score)}", x=WIDTH // 2 - 50, y=5, color="#00FFFF", font_style="24px Arial")]
        toggle_objs = [create_text_view_data(
            f"Timer: {str(self.frame_to_end - self.used_frame)} s", WIDTH - 150, 5, "#00FFFF", "24px Arial BOLD")]
        toggle_objs.append(create_text_view_data(
            content=f"HP: {self.player.HP}", x=5, y=5, color="#ff0000", font_style="24px Arial BOLD"
        ))

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
    def _create_mobs(self, count: int = 8):
        # 根據傳入的參數，決定建立幾個mob（莫認為8）
        for i in range(count):
            # 建立mob物件，並加入到mob的集合裡
            mob = Mob(pygame.Rect(0, -100, WIDTH, HEIGHT + 100))
            self.mobs.add(mob)

    # 建立bullet物件
    def _create_bullet(self, is_player: bool, init_pos: tuple):
        bullet = Bullet(is_player=is_player, init_pos=init_pos, play_rect_area=pygame.Rect(0, 0, WIDTH, HEIGHT + 100))
        # 加入到bullet裡面
        self.bullets.add(bullet)
