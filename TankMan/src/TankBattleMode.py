import random

import pygame.event
import pygame.event
from mlgame.game.paia_game import GameResultState, GameStatus
from mlgame.utils.enum import get_ai_name
from mlgame.view.view_model import create_asset_init_data, create_text_view_data, \
    create_rect_view_data, create_line_view_data
from mlgame.view.view_model import create_image_view_data

from GameFramework.SoundController import create_music_data
from GameFramework.TiledMap import TiledMap, create_construction
from GameFramework.constants import ID, X, Y, WIDTH, HEIGHT, ANGLE
from GameFramework.game_mode.BattleMode import BattleMode
from .TankBullet import TankBullet
from .TankPlayer import TankPlayer
from .TankSoundController import TankSoundController
from .TankStation import TankStation
from .TankWall import TankWall
from .collide_hit_rect import *
from .env import *


# TODO refactor attribute to method
class TankBattleMode(BattleMode):
    _ID = ID
    _X = X
    _Y = Y
    _WIDTH = WIDTH
    _HEIGHT = HEIGHT
    _ANGLE = ANGLE

    def __init__(self, user_num: int, is_manual: bool, map_path: str, frame_limit: int, is_sound: bool):
        self._user_num = user_num
        self.map_path = map_path
        self.frame_limit = frame_limit
        self.is_paused = False
        self.is_debug = False
        self.all_sprites = pygame.sprite.Group()
        self.map = TiledMap(self.map_path)
        self.used_frame = 0
        self.state = GameResultState.FAIL
        self.status = GameStatus.GAME_ALIVE
        self.players = pygame.sprite.Group()
        self.map_width = self.map.map_width
        self.map_height = self.map.map_height

        pygame.init()
        self.is_sound = is_sound
        self.is_manual = is_manual
        self.sound_controller = TankSoundController(is_sound, self.get_music_data())
        self.sound_controller.play_music(path.join(SOUND_DIR, "BGM.ogg"), 0.1)
        self.WIDTH_CENTER = self.map.map_width // 2
        self.HEIGHT_CENTER = self.map.map_height // 2
        # control variables
        self.is_invincible = False
        self.is_through_wall = False
        # initialize sprites group
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
        self.empty_quadrant_1_pos = self.map.empty_quadrant_1_pos_list
        self.empty_quadrant_2_pos = self.map.empty_quadrant_2_pos_list
        self.empty_quadrant_3_pos = self.map.empty_quadrant_3_pos_list
        self.empty_quadrant_4_pos = self.map.empty_quadrant_4_pos_list
        self.floor_image_data_list = []
        for pos in self.all_pos_list:
            no = random.randrange(3)
            self.floor_image_data_list.append(
                create_image_view_data(f"floor_{no}", pos[0], pos[1], 50, 50, 0))

    def update(self, command: dict):
        if command["1P"] and "DEBUG" in command["1P"]:
            self.is_debug = not self.is_debug
        self.walls.update()
        self.update_game_mode(command)
        self.oil_stations.update()
        self.bullet_stations.update()
        self.bullets.update()
        if self.player_1P._is_shoot:
            shoot_info = self.player_1P.create_shoot_info()
            self.create_bullet(shoot_info)
            self.player_1P._is_shoot = False

        if self.player_2P._is_shoot:
            shoot_info = self.player_2P.create_shoot_info()
            shoot_info["rot"] -= 180
            self.create_bullet(shoot_info)
            self.player_2P._is_shoot = False

    # TODO refactor result info and position
    def get_result(self) -> list:
        """Define the end of game will return the player's info for user"""
        res = []
        for player in self.players:
            get_res = player.get_result()
            get_res = self.get_other_result(get_res)
            get_res["state"] = self.state
            get_res["status"] = self.status
            res.append(get_res)
        return res

    def get_other_result(self, origin_result):
        """You can overwrite or append new result to origin result, when you finished, return origin_result"""
        return origin_result

    def update_game_mode(self, command: dict):
        self.set_result(GameResultState.FAIL, GameStatus.GAME_ALIVE)
        if not self.is_paused:
            self.used_frame += 1
            number = 1
            for player in self.players:
                player.update(command[f"{number}P"])
                number += 1
                # TODO refactor reset method
                if not player.get_is_alive() or self.used_frame >= self.frame_limit:
                    self.reset()
            self.check_collisions()

    def calculate_score(self) -> tuple:
        score_1P = (3 - self.player_2P._lives) * 20
        score_2P = (3 - self.player_1P._lives) * 20
        return score_1P, score_2P

    def reset(self):
        if self.player_1P._is_alive and not self.player_2P._is_alive:
            self.set_result(GameResultState.FINISH, GameStatus.GAME_1P_WIN)
        elif not self.player_1P._is_alive and self.player_2P._is_alive:
            self.set_result(GameResultState.FINISH, GameStatus.GAME_2P_WIN)
        self.reset_2()

    def reset_2(self):
        if self.status == GameStatus.GAME_ALIVE:
            score_1P = self.player_1P._score + self.calculate_score()[0]
            score_2P = self.player_2P._score + self.calculate_score()[1]
            if score_1P > score_2P:
                self.set_result(GameResultState.FINISH, GameStatus.GAME_1P_WIN)
            elif score_1P < score_2P:
                self.set_result(GameResultState.FINISH, GameStatus.GAME_2P_WIN)
            else:
                self.set_result(GameResultState.FAIL, GameStatus.GAME_DRAW)

    def reset_game(self):
        # reset init game
        self.__init__(2, self.is_manual, self.map_path, self.frame_limit, self.is_sound)
        # reset player pos
        self.empty_quadrant_1_pos.append(self.player_1P._origin_xy)
        self.empty_quadrant_2_pos.append(self.player_2P._origin_xy)
        self.player_1P.rect.topleft = self.empty_quadrant_1_pos.pop(random.randrange(len(self.empty_quadrant_1_pos)))
        self.player_2P.rect.topleft = self.empty_quadrant_2_pos.pop(random.randrange(len(self.empty_quadrant_2_pos)))
        self.player_1P.hit_rect.center = self.player_1P.rect.center
        self.player_2P.hit_rect.center = self.player_2P.rect.center

    def set_result(self, state: str, status: str):
        self.state = state
        self.status = status

    def get_act_command(self):
        """
        Define the actions represented by the key
        (1) press to execute
        key_pressed_list = pygame.key.get_pressed()
        (2)
        get key to execute
        for even in pygame.event.get():
            pass
        """
        ai_1P = get_ai_name[0]
        ai_2P = get_ai_name[1]
        cmd_1P = self.get_1P_command()
        cmd_2P = self.get_2P_command()

        return {ai_1P: cmd_1P, ai_2P: cmd_2P}

    def get_1P_command(self) -> list:
        cmd_1P = []
        key_pressed_list = pygame.key.get_pressed()
        if key_pressed_list[pygame.K_UP]:
            cmd_1P.append(FORWARD_CMD)
        elif key_pressed_list[pygame.K_DOWN]:
            cmd_1P.append(BACKWARD_CMD)

        if key_pressed_list[pygame.K_SPACE]:
            cmd_1P.append(SHOOT)

        for even in pygame.event.get():
            if even.type == pygame.KEYDOWN:
                if even.key == pygame.K_RIGHT:
                    cmd_1P.append(RIGHT_CMD)
                elif even.key == pygame.K_LEFT:
                    cmd_1P.append(LEFT_CMD)

        return cmd_1P

    def get_2P_command(self) -> list:
        cmd_2P = []
        key_pressed_list = pygame.key.get_pressed()
        if key_pressed_list[pygame.K_w]:
            cmd_2P.append(FORWARD_CMD)
        elif key_pressed_list[pygame.K_s]:
            cmd_2P.append(BACKWARD_CMD)

        if key_pressed_list[pygame.K_f]:
            cmd_2P.append(SHOOT)

        for even in pygame.event.get():
            if even.type == pygame.KEYDOWN:
                if even.key == pygame.K_d:
                    cmd_2P.append(RIGHT_CMD)
                elif even.key == pygame.K_a:
                    cmd_2P.append(LEFT_CMD)

        return cmd_2P

    def get_scene_info(self):
        scene_info = {"frame": self.used_frame,
                      "status": self.status,
                      "background": [1320, 660],
                      "1P_xy_pos": self.player_1P.get_xy(),
                      "2P_xy_pos": self.player_2P.get_xy(),
                      "game_result": self.get_result(),
                      "state": self.state}

        return scene_info

    def check_collisions(self):
        if not self.is_through_wall:
            collide_with_walls(self.players, self.walls)
        if not self.is_invincible:
            collide_with_bullets(self.players, self.bullets)
            # TODO refactor stations
            bs = collide_with_bullet_stations(self.players, self.bullet_stations)
            self.change_obj_pos(bs)
            os = collide_with_oil_stations(self.players, self.oil_stations)
            self.change_obj_pos(os)
        player_id, score = collide_with_bullets(self.walls, self.bullets)
        if player_id == 1:
            self.player_1P._score += score
        elif player_id == 2:
            self.player_2P._score += score

    def change_obj_pos(self, stations: list):
        if not stations:
            return
        for station in stations:
            if station.get_quadrant() == 1:
                self.empty_quadrant_1_pos.append(station.get_xy())
            elif station.get_quadrant() == 2:
                self.empty_quadrant_2_pos.append(station.get_xy())
            elif station.get_quadrant() == 3:
                self.empty_quadrant_3_pos.append(station.get_xy())
            else:
                self.empty_quadrant_4_pos.append(station.get_xy())
            if station.get_quadrant() == 2 or station.get_quadrant() == 3:
                quadrant = random.choice([2, 3])
                station.set_quadrant(quadrant)
            else:
                quadrant = random.choice([1, 4])
                station.set_quadrant(quadrant)
            if quadrant == 1:
                new_pos = self.empty_quadrant_1_pos.pop(random.randrange(len(self.empty_quadrant_1_pos)))
                station.change_pos(new_pos)
            elif quadrant == 2:
                new_pos = self.empty_quadrant_2_pos.pop(random.randrange(len(self.empty_quadrant_2_pos)))
                station.change_pos(new_pos)
            elif quadrant == 3:
                new_pos = self.empty_quadrant_3_pos.pop(random.randrange(len(self.empty_quadrant_3_pos)))
                station.change_pos(new_pos)
            else:
                new_pos = self.empty_quadrant_4_pos.pop(random.randrange(len(self.empty_quadrant_4_pos)))
                station.change_pos(new_pos)

    def create_bullet(self, shoot_info):
        self.sound_controller.play_shoot_sound()
        init_data = create_construction(shoot_info["id"], 0, shoot_info["init_pos"], (13, 13))
        bullet = TankBullet(init_data, rot=shoot_info["rot"], margin=2, spacing=2)
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)

    def draw_players(self):
        player_data = []
        for player in self.players:
            data = player.get_obj_progress_data()
            player_data.append(create_image_view_data(data[self._ID], data[self._X], data[self._Y],
                                                      data[self._WIDTH], data[self._HEIGHT],
                                                      data[self._ANGLE]))

        return player_data

    def get_obj_progress_data(self):
        all_sprite_data = self.floor_image_data_list.copy()
        for oil_station in self.oil_stations:
            if isinstance(oil_station, TankStation):
                data = oil_station.get_obj_progress_data()
                all_sprite_data.append(create_image_view_data(data[self._ID], data[self._X], data[self._Y],
                                                              data[self._WIDTH], data[self._HEIGHT],
                                                              data[self._ANGLE]))

        for bullet_station in self.bullet_stations:
            if isinstance(bullet_station, TankStation):
                data = bullet_station.get_obj_progress_data()
                all_sprite_data.append(create_image_view_data(data[self._ID], data[self._X], data[self._Y],
                                                              data[self._WIDTH], data[self._HEIGHT],
                                                              data[self._ANGLE]))

        for bullet in self.bullets:
            if isinstance(bullet, TankBullet):
                data = bullet.get_obj_progress_data()
                all_sprite_data.append(create_image_view_data(data[self._ID], data[self._X], data[self._Y],
                                                              data[self._WIDTH], data[self._HEIGHT],
                                                              data[self._ANGLE]))

        for player in self.draw_players():
            all_sprite_data.append(player)

        for wall in self.walls:
            if isinstance(wall, TankWall):
                data = wall.get_obj_progress_data()
                if data:
                    all_sprite_data.append(create_image_view_data(data[self._ID], data[self._X], data[self._Y],
                                                                  data[self._WIDTH], data[self._HEIGHT],
                                                                  data[self._ANGLE]))

        if self.is_debug:
            for sprite in self.all_sprites:
                all_sprite_data.extend(self.draw_rect(sprite))

        all_sprite_data.append(create_image_view_data("border", 0, -50, self.map.map_width, WINDOW_HEIGHT, 0))

        return all_sprite_data

    def get_foreground_progress_data(self):
        all_foreground_data = []

        return all_foreground_data

    def get_toggle_progress_data(self):
        all_toggle_data = []
        # hourglass_index = self.used_frame // 10 % 15
        hourglass_index = 1
        all_toggle_data.append(
            create_image_view_data(image_id=f"hourglass_{hourglass_index}", x=0, y=2, width=20, height=20, angle=0))
        x = 23
        y = 8
        for frame in range((self.frame_limit - self.used_frame) // int((30 * 2))):
            all_toggle_data.append(create_rect_view_data("frame", x, y, 3, 10, RED))
            x += 3.5
        all_toggle_data.append(create_text_view_data(f"Frame: {self.frame_limit - self.used_frame}",
                                                     self.WIDTH_CENTER + self.WIDTH_CENTER // 2 + 85, 8, RED,
                                                     "24px Arial BOLD"))
        score_1P = self.player_1P._score + self.calculate_score()[0]
        score_2P = self.player_2P._score + self.calculate_score()[1]
        x = 24
        y = 20
        for score in range(min(score_1P, score_2P)):
            all_toggle_data.append(create_rect_view_data(name="score", x=x, y=y, width=1, height=10, color=ORANGE))
            x += 1.5
            if x > self.WIDTH_CENTER:
                if y == 32:
                    y = 44
                else:
                    y = 32
                x = 24
        for score in range(abs(score_1P - score_2P)):
            if score_1P > score_2P:
                all_toggle_data.append(create_rect_view_data("score", x, y, 1, 10, DARKGREEN))
            else:
                all_toggle_data.append(create_rect_view_data("score", x, y, 1, 10, BLUE))
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
        all_toggle_data.append(create_text_view_data(f"Score: {score_1P}", x, y, DARKGREEN, "24px Arial BOLD"))
        x = self.WIDTH_CENTER + 5
        y = WINDOW_HEIGHT - 40
        for live in range(self.player_1P._lives):
            all_toggle_data.append(create_image_view_data("1P_lives", x, y, 30, 30))
            x += 35
        # 620 px
        x = self.WIDTH_CENTER + 120
        y = WINDOW_HEIGHT - 40
        all_toggle_data.append(
            create_rect_view_data("1P_oil", x, y, self.player_1P.oil, 10, ORANGE))
        x = self.WIDTH_CENTER + 121
        y = WINDOW_HEIGHT - 20
        for power in range(self.player_1P._power):
            all_toggle_data.append(create_rect_view_data("1P_power", x, y, 8, 10, BLUE))
            x += 10
        # 2P
        x = 5
        y = WINDOW_HEIGHT - 40
        all_toggle_data.append(create_text_view_data(f"Score: {score_2P}", x, y, BLUE, "24px Arial BOLD"))
        x = self.WIDTH_CENTER - 40
        y = WINDOW_HEIGHT - 40
        for live in range(self.player_2P._lives):
            all_toggle_data.append(create_image_view_data("2P_lives", x, y, 30, 30))
            x -= 35
        # 375 px
        x = self.WIDTH_CENTER - 125 - 100 + (100 - self.player_2P.oil)
        y = WINDOW_HEIGHT - 40
        all_toggle_data.append(
            create_rect_view_data("2P_oil", x, y, self.player_2P.oil, 10,
                                  ORANGE))
        x = self.WIDTH_CENTER - 125 - 9
        y = WINDOW_HEIGHT - 20
        for power in range(self.player_2P._power):
            all_toggle_data.append(create_rect_view_data("2P_power", x, y, 8, 10, BLUE))
            x -= 10

        return all_toggle_data

    def get_init_image_data(self):
        all_init_image_data = []
        for i in range(3):
            all_init_image_data.append(create_asset_init_data(f"floor_{i}", 50, 50
                                                              , path.join(IMAGE_DIR, f"grass_{i}.png"),
                                                              f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/grass_{i}.png"))
        for i in range(1, 2):
            all_init_image_data.append(create_asset_init_data(f"hourglass_{i}", 42, 42
                                                              , path.join(IMAGE_DIR, f"hourglass_{i}.png"),
                                                              f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/hourglass_{i}.png"))
        for station in self.bullet_stations:
            if isinstance(station, TankStation):
                for data in station.get_obj_init_data():
                    all_init_image_data.append(data)
                break
        for wall in self.walls:
            if isinstance(wall, TankWall):
                for data in wall.get_obj_init_data():
                    all_init_image_data.append(data)
                break
        img_id = "bullet"
        img_url = "https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/bullet.png"
        bullet_image_init_data = create_asset_init_data(img_id, BULLET_SIZE[0], BULLET_SIZE[1],
                                                        path.join(IMAGE_DIR, f"{img_id}.png"), img_url)
        all_init_image_data.append(bullet_image_init_data)
        border_image_init_data = create_asset_init_data("border", self.map.map_width, WINDOW_HEIGHT,
                                                        path.join(IMAGE_DIR, "border.png"),
                                                        f"https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/border.png")
        all_init_image_data.append(border_image_init_data)
        for data in self.player_1P.get_obj_init_data():
            all_init_image_data.append(data)
        lives_image_init_data_1 = create_asset_init_data("1P_lives", 30, 30, path.join(IMAGE_DIR, "1P_lives.png"),
                                                         "https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/1P_lives.png")
        all_init_image_data.append(lives_image_init_data_1)
        lives_image_init_data_2 = create_asset_init_data("2P_lives", 30, 30, path.join(IMAGE_DIR, "2P_lives.png"),
                                                         "https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/2P_lives.png")
        all_init_image_data.append(lives_image_init_data_2)
        return all_init_image_data

    def get_ai_data_to_player(self, ai_no: int):
        if ai_no == 1:
            player = self.player_1P
        else:
            player = self.player_2P
        to_game_data = player.get_data_from_obj_to_game()
        to_game_data["used_frame"] = self.used_frame
        to_game_data["status"] = self.status
        to_game_data["player_info"] = [ai.get_data_from_obj_to_game() for ai in self.players if isinstance(ai, TankPlayer)]
        to_game_data["walls_info"] = [wall.get_data_from_obj_to_game() for wall in self.walls if isinstance(wall, TankWall)]
        to_game_data["bullet_stations_info"] = [bullst_station.get_data_from_obj_to_game() for bullst_station in self.bullet_stations if isinstance(bullst_station, TankStation)]
        to_game_data["oil_stations_info"] = [oil_station.get_data_from_obj_to_game() for oil_station in self.oil_stations if isinstance(oil_station, TankStation)]

        return to_game_data

    def get_other_result(self, origin_result):
        if origin_result["id"] == "1P":
            origin_result["score"] = self.player_1P._score + self.calculate_score()[0]
        else:
            origin_result["score"] = self.player_2P._score + self.calculate_score()[1]
        return origin_result

    def get_music_data(self):
        return [create_music_data("shoot", path.join(SOUND_DIR, "shoot.wav"))
                , create_music_data("touch", path.join(SOUND_DIR, "touch.wav"))]

    def draw_rect(self, sprite):
        all_line = []
        point = [(sprite.rect.x, sprite.rect.y), sprite.rect.topright, sprite.rect.bottomright, sprite.rect.bottomleft,
                 (sprite.rect.x, sprite.rect.y)]
        hit_point = [(sprite.hit_rect.x, sprite.hit_rect.y), sprite.hit_rect.topright, sprite.hit_rect.bottomright,
                     sprite.hit_rect.bottomleft, (sprite.hit_rect.x, sprite.hit_rect.y)]
        for i in range(4):
            all_line.append(
                create_line_view_data(f"{sprite.get_data_from_obj_to_game()['id']}", point[i][0], point[i][1],
                                      point[i + 1][0],
                                      point[i + 1][1], YELLOW, 2))
            all_line.append(create_line_view_data(f"hit_{sprite.get_data_from_obj_to_game()['id']}", hit_point[i][0],
                                                  hit_point[i][1],
                                                  hit_point[i + 1][0], hit_point[i + 1][1], RED, 2))
        return all_line
