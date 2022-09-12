import random

import pygame.event
import pygame.event
from mlgame.game.paia_game import GameResultState, GameStatus
from mlgame.utils.enum import get_ai_name
from mlgame.view.view_model import create_asset_init_data, create_text_view_data, \
    create_rect_view_data, create_line_view_data, create_polygon_view_data
from mlgame.view.view_model import create_image_view_data

from GameFramework.SoundController import create_sounds_data, create_bgm_data
from GameFramework.TiledMap import create_construction
from GameFramework.game_mode.BattleMode import BattleMode
from .TankBullet import TankBullet
from .TankPlayer import TankPlayer
from .TankStation import TankStation
from .TankWall import TankWall
from .collide_hit_rect import *
from .env import *


# TODO refactor attribute to method
class TankBattleMode(BattleMode):
    def __init__(self, is_manual: bool, map_path: str, frame_limit: int, sound_path: str):
        super().__init__(map_path, sound_path)
        self.obj_rect_list = []
        self.frame_limit = frame_limit
        self.is_manual = is_manual
        self.scene_height = self.map.map_height + 100
        # control variables
        self.is_invincible = False
        self.is_through_wall = False
        # initialize sprites group
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.bullet_stations = pygame.sprite.Group()
        self.oil_stations = pygame.sprite.Group()
        # init players
        act_cd = 0
        if self.is_manual:
            act_cd = 10
        # init obj data
        self.map.add_init_obj_data(PLAYER_1_IMG_NO, TankPlayer, act_cd=act_cd)
        self.map.add_init_obj_data(PLAYER_2_IMG_NO, TankPlayer, act_cd=act_cd)
        self.map.add_init_obj_data(WALL_IMG_NO, TankWall, margin=8, spacing=8)
        self.map.add_init_obj_data(BULLET_STATION_IMG_NO, TankStation, margin=2, spacing=2, capacity=5, quadrant=1)
        self.map.add_init_obj_data(OIL_STATION_IMG_NO, TankStation, margin=2, spacing=2, capacity=30, quadrant=1)
        # create obj
        all_obj = self.map.create_init_obj_dict()
        # init player
        self.player_1P = all_obj[PLAYER_1_IMG_NO][0]
        self.player_2P = all_obj[PLAYER_2_IMG_NO][0]
        self.players.add(self.player_1P, self.player_2P)
        self.all_sprites.add(self.player_1P, self.player_2P)
        # init walls
        self.walls.add(all_obj[WALL_IMG_NO])
        self.all_sprites.add(*self.walls)
        # init bullet stations
        self.bullet_stations.add(all_obj[BULLET_STATION_IMG_NO])
        self.all_sprites.add(*self.bullet_stations)
        # init oil stations
        self.oil_stations.add(all_obj[OIL_STATION_IMG_NO])
        self.all_sprites.add(*self.oil_stations)
        # init pos list
        self.all_pos_list = self.map.all_pos_list
        self.empty_quadrant_pos_dict = self.map.empty_quadrant_pos_dict
        self.floor_image_data_list = []
        for pos in self.all_pos_list:
            no = random.randrange(3)
            self.floor_image_data_list.append(
                create_image_view_data(f"floor_{no}", pos[0], pos[1], 50, 50, 0))

    def update(self, command: dict):
        self.used_frame += 1
        self.check_collisions()
        self.walls.update()
        self.oil_stations.update()
        self.bullet_stations.update()
        self.bullets.update()
        self.players.update(command)
        if self.used_frame >= self.frame_limit:
            self.get_game_end()

    def reset(self):
        # reset init game
        self.__init__(self.is_manual, self.map_path, self.frame_limit, self.sound_path)
        # reset player pos
        self.empty_quadrant_pos_dict[1].append(self.player_1P._origin_xy)
        self.empty_quadrant_pos_dict[2].append(self.player_2P._origin_xy)
        self.player_1P.reset_xy(self.empty_quadrant_pos_dict[1].pop(random.randrange(len(self.empty_quadrant_pos_dict[1]))))
        self.player_2P.reset_xy(self.empty_quadrant_pos_dict[2].pop(random.randrange(len(self.empty_quadrant_pos_dict[2]))))

    def get_player_end(self):
        if self.player_1P.get_is_alive() and not self.player_2P.get_is_alive():
            self.set_result(GameResultState.FINISH, GameStatus.GAME_1P_WIN)
        elif not self.player_1P.get_is_alive() and self.player_2P.get_is_alive():
            self.set_result(GameResultState.FINISH, GameStatus.GAME_2P_WIN)

    def get_game_end(self):
        score_1P = self.player_1P.get_score()
        score_2P = self.player_2P.get_score()
        if score_1P > score_2P:
            self.set_result(GameResultState.FINISH, GameStatus.GAME_1P_WIN)
        elif score_1P < score_2P:
            self.set_result(GameResultState.FINISH, GameStatus.GAME_2P_WIN)
        else:
            self.set_result(GameResultState.FINISH, GameStatus.GAME_DRAW)

    def set_result(self, state: str, status: str):
        self.state = state
        self.status = status

    def check_collisions(self):
        if not self.is_through_wall:
            collide_with_walls(self.players, self.walls)
        if not self.is_invincible:
            self.add_player_score(collide_with_bullets(self.players, self.bullets)[0])
            # TODO refactor stations
            bs = collide_with_bullet_stations(self.players, self.bullet_stations)
            self.change_obj_pos(bs)
            os = collide_with_oil_stations(self.players, self.oil_stations)
            self.change_obj_pos(os)
        player_id, score = collide_with_bullets(self.walls, self.bullets)
        if player_id == 1:
            self.player_1P.add_score(score)
        elif player_id == 2:
            self.player_2P.add_score(score)

    def change_obj_pos(self, objs=None):
        if objs is None:
            return
        for obj in objs:
            if isinstance(obj, TankStation):
                quadrant = obj.get_quadrant()
                self.empty_quadrant_pos_dict[quadrant].append(obj.get_xy())
                if quadrant == 2 or quadrant == 3:
                    obj.set_quadrant(random.choice([2, 3]))
                else:
                    obj.set_quadrant(random.choice([1, 4]))
                quadrant = obj.get_quadrant()
                new_pos = self.empty_quadrant_pos_dict[quadrant].pop(random.randrange(len(self.empty_quadrant_pos_dict[quadrant])))
                obj.reset_xy(new_pos)

    def create_bullet(self, player):
        if isinstance(player, TankPlayer) and not player.get_is_shoot():
            return
        self.sound_controller.play_sound("shoot", 0.03, -1)
        init_data = create_construction(player.get_id(), 0, player.get_center(), (13, 13))
        bullet = TankBullet(init_data, rot=player.get_rot(), margin=2, spacing=2)
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)
        player.set_is_shoot(False)

    def get_background_view_data(self):
        background_view_data = []
        return background_view_data

    def get_obj_progress_data(self):
        obj_progress_data = self.floor_image_data_list.copy()
        for oil_station in self.oil_stations:
            if isinstance(oil_station, TankStation):
                obj_progress_data.append(oil_station.get_obj_progress_data())

        for bullet_station in self.bullet_stations:
            if isinstance(bullet_station, TankStation):
                obj_progress_data.append(bullet_station.get_obj_progress_data())

        for bullet in self.bullets:
            if isinstance(bullet, TankBullet):
                obj_progress_data.append(bullet.get_obj_progress_data())

        for player in self.draw_players():
            obj_progress_data.append(player)

        for wall in self.walls:
            if isinstance(wall, TankWall):
                obj_progress_data.append(wall.get_obj_progress_data())

        obj_progress_data.extend(self.obj_rect_list)

        obj_progress_data.append(create_image_view_data("border", 0, -50, self.scene_width, WINDOW_HEIGHT, 0))

        return obj_progress_data

    def get_toggle_progress_data(self):
        toggle_data = []
        hourglass_index = 0
        if self.is_manual:
            hourglass_index = self.used_frame // 10 % 15
        toggle_data.append(
            create_image_view_data(image_id=f"hourglass_{hourglass_index}", x=0, y=2, width=20, height=20, angle=0))
        x = 23
        y = 8
        for frame in range((self.frame_limit - self.used_frame) // int((30 * 2))):
            toggle_data.append(create_rect_view_data("frame", x, y, 3, 10, RED))
            x += 3.5
        toggle_data.append(create_text_view_data(f"Frame: {self.frame_limit - self.used_frame}",
                                                     self.WIDTH_CENTER + self.WIDTH_CENTER // 2 + 85, 8, RED,
                                                     "24px Arial BOLD"))
        score_1P = self.player_1P.get_score()
        score_2P = self.player_2P.get_score()
        x = 24
        y = 20
        for score in range(min(score_1P, score_2P)):
            toggle_data.append(create_rect_view_data(name="score", x=x, y=y, width=1, height=10, color=ORANGE))
            x += 1.5
            if x > self.WIDTH_CENTER:
                if y == 32:
                    y = 44
                else:
                    y = 32
                x = 24
        for score in range(abs(score_1P - score_2P)):
            if score_1P > score_2P:
                toggle_data.append(create_rect_view_data("score", x, y, 1, 10, DARKGREEN))
            else:
                toggle_data.append(create_rect_view_data("score", x, y, 1, 10, BLUE))
            x += 1.5
            if x > self.WIDTH_CENTER:
                if y == 32:
                    y = 44
                else:
                    y = 32
                x = 24
        # 1P
        x = WINDOW_WIDTH - 105
        y = WINDOW_HEIGHT - 40
        toggle_data.append(create_text_view_data(f"Score: {score_1P}", x, y, DARKGREEN, "24px Arial BOLD"))
        x = self.WIDTH_CENTER + 5
        y = WINDOW_HEIGHT - 40
        for live in range(self.player_1P._lives):
            toggle_data.append(create_image_view_data("1P_lives", x, y, 30, 30))
            x += 35
        # 620 px
        x = self.WIDTH_CENTER + 120
        y = WINDOW_HEIGHT - 40
        toggle_data.append(
            create_rect_view_data("1P_oil", x, y, self.player_1P.oil, 10, ORANGE))
        x = self.WIDTH_CENTER + 121
        y = WINDOW_HEIGHT - 20
        for power in range(self.player_1P._power):
            toggle_data.append(create_rect_view_data("1P_power", x, y, 8, 10, BLUE))
            x += 10
        # 2P
        x = 5
        y = WINDOW_HEIGHT - 40
        toggle_data.append(create_text_view_data(f"Score: {score_2P}", x, y, BLUE, "24px Arial BOLD"))
        x = self.WIDTH_CENTER - 40
        y = WINDOW_HEIGHT - 40
        for live in range(self.player_2P._lives):
            toggle_data.append(create_image_view_data("2P_lives", x, y, 30, 30))
            x -= 35
        # 375 px
        x = self.WIDTH_CENTER - 125 - 100 + (100 - self.player_2P.oil)
        y = WINDOW_HEIGHT - 40
        toggle_data.append(
            create_rect_view_data("2P_oil", x, y, self.player_2P.oil, 10,
                                  ORANGE))
        x = self.WIDTH_CENTER - 125 - 9
        y = WINDOW_HEIGHT - 20
        for power in range(self.player_2P._power):
            toggle_data.append(create_rect_view_data("2P_power", x, y, 8, 10, BLUE))
            x -= 10

        return toggle_data

    def get_init_image_data(self):
        init_image_data = []
        for i in range(3):
            init_image_data.append(create_asset_init_data(f"floor_{i}", 50, 50
                                                              , path.join(IMAGE_DIR, f"grass_{i}.png"),
                                                              f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/grass_{i}.png"))
        for i in range(15):
            init_image_data.append(create_asset_init_data(f"hourglass_{i}", 42, 42
                                                              , path.join(IMAGE_DIR, f"hourglass_{i}.png"),
                                                              f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/hourglass_{i}.png"))
        for station in self.bullet_stations:
            if isinstance(station, TankStation):
                for data in station.get_obj_init_data():
                    init_image_data.append(data)
                break
        for wall in self.walls:
            if isinstance(wall, TankWall):
                for data in wall.get_obj_init_data():
                    init_image_data.append(data)
                break
        img_id = "bullet"
        img_url = "https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/bullet.png"
        bullet_image_init_data = create_asset_init_data(img_id, BULLET_SIZE[0], BULLET_SIZE[1],
                                                        path.join(IMAGE_DIR, f"{img_id}.png"), img_url)
        init_image_data.append(bullet_image_init_data)
        border_image_init_data = create_asset_init_data("border", self.scene_width, WINDOW_HEIGHT,
                                                        path.join(IMAGE_DIR, "border.png"),
                                                        f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/border.png")
        init_image_data.append(border_image_init_data)
        for data in self.player_1P.get_obj_init_data():
            init_image_data.append(data)
        lives_image_init_data_1 = create_asset_init_data("1P_lives", 30, 30, path.join(IMAGE_DIR, "1P_lives.png"),
                                                         "https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/1P_lives.png")
        init_image_data.append(lives_image_init_data_1)
        lives_image_init_data_2 = create_asset_init_data("2P_lives", 30, 30, path.join(IMAGE_DIR, "2P_lives.png"),
                                                         "https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/2P_lives.png")
        init_image_data.append(lives_image_init_data_2)
        return init_image_data

    def get_ai_data_to_player(self):
        to_player_data = {}
        num = 0
        for player in self.players:
            if isinstance(player, TankPlayer):
                to_game_data = player.get_data_from_obj_to_game()
                to_game_data["used_frame"] = self.used_frame
                to_game_data["status"] = self.status
                to_game_data["player_info"] = [ai.get_data_from_obj_to_game() for ai in self.players if isinstance(ai, TankPlayer)]
                to_game_data["walls_info"] = [wall.get_data_from_obj_to_game() for wall in self.walls if isinstance(wall, TankWall)]
                to_game_data["bullet_stations_info"] = [bullst_station.get_data_from_obj_to_game() for bullst_station in self.bullet_stations if isinstance(bullst_station, TankStation)]
                to_game_data["oil_stations_info"] = [oil_station.get_data_from_obj_to_game() for oil_station in self.oil_stations if isinstance(oil_station, TankStation)]
                to_player_data[get_ai_name(num)] = to_game_data
                num += 1

        return to_player_data

    def get_bgm_data(self):
        return create_bgm_data("BGM.ogg", 0.1)

    def get_sound_data(self):
        return [create_sounds_data("shoot", "shoot.wav")
                , create_sounds_data("touch", "touch.wav")]

    def add_player_score(self, player_id: int):
        if not player_id:
            return
        if player_id == 1:
            self.player_1P.add_score(20)
        else:
            self.player_2P.add_score(20)

    def debugging(self, is_debug: bool):
        self.obj_rect_list = []
        if not is_debug:
            return
        for sprite in self.all_sprites:
            if isinstance(sprite, pygame.sprite.Sprite):
                points = [sprite.rect.topleft, sprite.rect.topright, sprite.rect.bottomright
                          , sprite.rect.bottomleft, sprite.rect.topleft]
                hit_points = [sprite.hit_rect.topleft, sprite.hit_rect.topright, sprite.hit_rect.bottomright
                              , sprite.hit_rect.bottomleft, sprite.rect.topleft]
                for index in range(len(points)-1):
                    self.obj_rect_list.append(create_line_view_data("rect", *points[index], *points[index+1], WHITE))
                    self.obj_rect_list.append(create_line_view_data("hit_rect", *hit_points[index], *hit_points[index+1], RED))