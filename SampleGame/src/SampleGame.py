import random
import pygame

from os import path
from mlgame.game.paia_game import PaiaGame, GameResultState, GameStatus
from mlgame.utils.enum import get_ai_name
from mlgame.view.decorator import check_game_progress, check_game_result
from mlgame.view.view_model import Scene, create_text_view_data, create_scene_progress_data, create_asset_init_data, \
    create_image_view_data, create_rect_view_data

from game_module.SoundController import SoundController, create_sounds_data
from game_module.TiledMap import TiledMap, create_construction
from .SampleBullet import SampleBullet
from .SampleMob import SampleMob
from .SamplePlayer import SamplePlayer
from .SampleWall import SampleWall

ASSET_PATH = path.join(path.dirname(__file__), "../asset")
WIDTH = 800
HEIGHT = 600


# class 類別名稱(繼承的類別):
# 這是遊戲的類別，用於建立遊戲的模板
class SampleGame(PaiaGame):
    # def 方法名稱(參數: 型態 = 預設值):
    # 定義遊戲的初始化
    def __init__(self, user_num=1, frame_limit: int = 300, target_score: int = 3000, is_sound: str = "off", map_no: int = None, *args, **kwargs):
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
        self.is_sound = False
        self.map_no = map_no
        # 若有傳入地圖編號，則建立地圖
        if self.map_no:
            self.map = TiledMap(map_path=path.join(ASSET_PATH, f"map/map_0{self.map_no}.tmx"))
        if is_sound == "on":
            self.is_sound = True
        # 建立聲音物件
        self.sound_controller = SoundController(self.is_sound, self.get_music_data())
        # 建立遊戲物件，並加入該物件的集合
        self.player = SamplePlayer(
                        construction=create_construction(
                                        _id=1
                                        , _no=1
                                        , _init_pos=(WIDTH // 2, HEIGHT - 80)
                                        , _init_size=(50, 50))
                        , play_area_rect=pygame.Rect(0, 0, WIDTH, HEIGHT))
        self._create_mobs(8)
        for i in range(random.randrange(10)):
            wall = SampleWall(
                    construction=create_construction(
                                    _id=1
                                    , _no=i
                                    , _init_pos=(random.randrange(WIDTH - 50), random.randrange(HEIGHT - 100))
                                    , _init_size=(50, 50))
                    , image_id="wall")
            self.walls.add(wall)
        # 撥放音樂
        self.sound_controller.play_music(
            music_path=path.join(ASSET_PATH, "sound/bgm.ogg")
            , volume=0.4)

    # 在這裡將遊戲內所有的物件進行或檢查是否更新（commands={"1P": list}）或檢查程式流程的檢查
    def update(self, commands: dict):
        # 更新已使用的frame
        self.used_frame += 1
        # 更新遊戲的分數
        self.score = self.player.get_score()
        # 更新ＡＩ輸入的指令(command)動作
        ai_1p_cmd = commands[get_ai_name(0)]
        if self.player.get_is_shoot():
            self.sound_controller.play_sound(music_id="test", maz_time=100, volume=0.4)
            self._create_bullets()
            self.player.stop_shoot()
        # print(ai_1p_cmd)
        if self.used_frame % 30 == 0:
            for mob in self.mobs:
                if isinstance(mob, SampleMob):
                    self._create_bullets(init_pos=mob.get_center())
        # 更新物件內部資訊
        self.player.update(ai_1p_cmd)
        self.mobs.update()
        self.bullets.update()
        self.walls.update()
        # 處理碰撞
        # 玩家和敵人
        hits = pygame.sprite.spritecollide(self.player, self.mobs, True, pygame.sprite.collide_rect_ratio(0.8))
        if hits:
            self.player.collide_with_mobs()
        # 玩家和子彈
        hits = pygame.sprite.spritecollide(self.player, self.bullets, False, pygame.sprite.collide_rect_ratio(0.8))
        for bullet in hits:
            if isinstance(bullet, SampleBullet) and not bullet.is_player:
                bullet.kill()
                self.player.collide_with_bullets()
        # 子彈和敵人
        hits = pygame.sprite.groupcollide(self.bullets, self.mobs, False, False, pygame.sprite.collide_rect_ratio(0.8))
        for bullet, mobs in hits.items():
            if isinstance(bullet, SampleBullet) and bullet.is_player:
                bullet.kill()
                for mob in mobs:
                    if isinstance(mob, SampleMob):
                        mob.collide_with_bullets()
                        self._create_mobs()
                        self.player.add_score(100 - mob.get_size()[0])
        # 牆和子彈
        hits = pygame.sprite.groupcollide(self.walls, self.bullets, False, False, pygame.sprite.collide_rect_ratio(0.8))
        for wall, bullets in hits.items():
            if isinstance(wall, SampleWall):
                for bullet in bullets:
                    if wall.get_shield():
                        bullet.kill()
                        wall.collide_with_bullets()

        # 判定是否重置遊戲
        if not self.is_running:
            return "RESET"

    # update回傳"RESET"時執行，在這裡定義遊戲重置會執行的內容
    def reset(self):
        print("reset MyGame")
        if self.is_sound:
            is_sound = "on"
        else:
            is_sound = "off"
        # 重新初始化遊戲
        self.__init__(frame_limit=self.frame_to_end, is_sound=is_sound, map_no=self.map_no)

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
            if isinstance(wall, SampleWall):
                # 將wall的座標記錄下來
                walls_data.append(wall.get_data_from_obj_to_game())
        mobs_data = []
        for mob in self.mobs:
            if isinstance(mob, SampleMob):
                mobs_data.append(mob.get_data_from_obj_to_game())
        # 將所有要給（AI）玩家1的資料打包起來
        data_to_1p = {
            "used_frame": self.used_frame,
            "player_x": self.player.get_xy()[0],
            "player_y": self.player.get_xy()[1],
            "walls": walls_data,
            "mobs": mobs_data,
            "target_score": self.target_score - self.score,
            "status": self.get_game_status()
        }
        # to_players_data = {"1P": data_to_1p}
        to_players_data[get_ai_name(0)] = data_to_1p
        # should be equal to config. GAME_SETUP["ml_clients"][0]["name"]

        return to_players_data

    # 獲取遊戲狀態的method，在這裡定義遊戲什麼時候是存活、結束、勝利
    def get_game_status(self):
        if self.score >= self.target_score:
            status = GameStatus.GAME_PASS
        elif self.is_running:
            status = GameStatus.GAME_ALIVE
        else:
            status = GameStatus.GAME_OVER
        return status

    # 若is_running == False, 重置或結束遊戲
    @property
    def is_running(self):
        if self.player.get_is_alive() and self.score < self.target_score:
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
        bg_path = path.join(ASSET_PATH, "image/background.png")
        background = create_asset_init_data(
            image_id="background"
            , width=WIDTH-50
            , height=HEIGHT-50
            , file_path=bg_path
            , github_raw_url="https://raw.githubusercontent.com/Jesse-Jumbo/GameFramework/main/MyGame/asset/image/background.png")
        # 定義遊戲圖片初始資料，將場景的屬性，轉化為字典
        # 將所有圖片資訊加入assets裡
        scene_init_data = {"scene": self.scene.__dict__,
                           "assets": [background],
                           }
        for mob in self.mobs:
            if isinstance(mob, SampleMob):
                scene_init_data["assets"].extend(mob.get_obj_init_data())
                break
        scene_init_data["assets"].append(self.player.get_obj_init_data())
        return scene_init_data

    # 獲取所有遊戲畫面的更新資訊
    @check_game_progress
    def get_scene_progress_data(self):
        """
        Get the position of MyGame objects for drawing on the web
        """
        game_obj_list = []
        for bullet in self.bullets:
            if isinstance(bullet, SampleBullet):
                game_obj_list.append(bullet.get_obj_progress_data())
        for wall in self.walls:
            if isinstance(wall, SampleWall):
                game_obj_list.append(wall.get_obj_progress_data())
        for mob in self.mobs:
            if isinstance(mob, SampleMob):
                game_obj_list.append(mob.get_obj_progress_data())
        game_obj_list.append(self.player.get_obj_progress_data())
        backgrounds = [create_image_view_data(image_id="background", x=25, y=50, width=WIDTH-50, height=HEIGHT-50)]
        foregrounds = [
            create_text_view_data(
                content=f"Target Score: {self.target_score - self.score}", x=WIDTH // 2 - 50, y=5, color="#21A1F1", font_style="24px Arial")
            , create_text_view_data(
                content=f"Lives: {str(self.player.get_lives())}", x=5, y=5, color="#22390A", font_style="24px Arial")
            , create_text_view_data(
                content=f"Shield: {self.player.get_shield()}", x=5, y=HEIGHT-30, color="#ff0000", font_style="24px Arial")
        ]
        _x = 110
        for i in range(self.player.get_shield() // 10):
            foregrounds.append(create_rect_view_data(
                name="Shield", x=_x, y=HEIGHT-25, width= 5, height= 20, color="#ff0000", angle=0))
            _x += 7
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

    # 這裡若用ＡＩ玩遊戲，則應到ＡＩ的update定義此function的內容
    # 若以main.py啟動遊戲程式，請在此定義按鍵回傳命令
    def get_keyboard_command(self):
        """
        Define how your MyGame will run by your keyboard
        """
        keyboard = pygame.key.get_pressed()
        action = []

        if keyboard[pygame.K_w] or keyboard[pygame.K_UP]:
            action.append("UP")
        elif keyboard[pygame.K_s] or keyboard[pygame.K_DOWN]:
            action.append("DOWN")
        elif keyboard[pygame.K_a] or keyboard[pygame.K_LEFT]:
            action.append("LEFT")
        elif keyboard[pygame.K_d] or keyboard[pygame.K_RIGHT]:
            action.append("RIGHT")

        if keyboard[pygame.K_f]:
            action.append("SHOOT")

        # print({get_ai_name(0): actions})
        return {get_ai_name(0): action}

    # 建立mob物件的method，前面加底線，意指規範此method只供此類別（class）或其實例（instance）呼叫使用
    def _create_mobs(self, count: int = 1):
        # 根據傳入的參數，決定建立幾個mob（莫認為8）
        for i in range(count):
            # 建立mob物件，並加入到mob的集合裡
            mob = SampleMob(
                construction=create_construction(
                    _id=random.choice([0, 1])
                    , _no=i
                    , _init_pos=(random.randrange(0, 740), random.randrange(60, 120))
                    , _init_size=random.choice([(30, 30), (35, 35), (40, 40), (45, 45), (50, 50), (55, 55), (60, 60)]))
                , play_area_rect=pygame.Rect(0, -100, WIDTH, HEIGHT + 100))
            self.mobs.add(mob)

    def _create_bullets(self, init_pos: tuple = None):
        if not init_pos:
            init_pos = self.player.get_center()
            is_player = True
        else:
            is_player = False
        bullet = SampleBullet(create_construction(_id=0, _no=0
                                                  , _init_pos=init_pos
                                                  , _init_size=(5, 8))
                              , is_player=is_player
                              , play_rect_area=pygame.Rect(0, 0, WIDTH, HEIGHT)
                              , image_id="bullet")
        self.bullets.add(bullet)

    def get_music_data(self):
        return [create_sounds_data(music_id="test", music_name=path.join(ASSET_PATH, "sound/bgm.ogg"))]
