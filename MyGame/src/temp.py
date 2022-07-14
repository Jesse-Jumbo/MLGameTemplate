import random

import pygame

from mlgame.game.paia_game import PaiaGame, GameStatus, GameResultState
from mlgame.utils.enum import get_ai_name
from mlgame.view.decorator import check_game_progress, check_game_result
from mlgame.view.view_model import create_text_view_data, Scene, create_scene_progress_data

DRAW_BALL_SPEED = 40


class PingPong(PaiaGame):

    def __init__(self, difficulty, game_over_score,user_num=2,*args,**kwargs):
        super().__init__(user_num=user_num)
        self._difficulty = difficulty
        self._score = [0, 0]
        self._game_over_score = game_over_score
        self._frame_count = 0
        self._game_status = GameStatus.GAME_ALIVE
        self._ball_served = False
        self._ball_served_frame = 0
        self.scene = Scene(width=200, height=500, color="#000000", bias_x=0, bias_y=0)
        self._create_init_scene()

    def _create_init_scene(self):
        self._draw_group = pygame.sprite.RenderPlain()

        enable_slice_ball = False if self._difficulty == "EASY" else True
        self._ball = Ball(pygame.Rect(0, 0, 200, 500), enable_slice_ball, self._draw_group)
        self._platform_1P = Platform((80, 420),
                                     pygame.Rect(0, 0, 200, 500), "1P", self._draw_group)
        self._platform_2P = Platform((80, 70),
                                     pygame.Rect(0, 0, 200, 500), "2P", self._draw_group)

        if self._difficulty != "HARD":
            # Put the blocker at the end of the world
            self._blocker = Blocker(1000, pygame.Rect(0, 0, 200, 500), self._draw_group)
        else:
            self._blocker = Blocker(240, pygame.Rect(0, 0, 200, 500), self._draw_group)

        # Initialize the position of the ball
        self._ball.stick_on_platform(self._platform_1P.rect, self._platform_2P.rect)

    def update(self, commands):
        ai_1p_cmd = commands[get_ai_name(0)]
        ai_2p_cmd = commands[get_ai_name(1)]
        command_1P = (PlatformAction(ai_1p_cmd)
                      if ai_1p_cmd in PlatformAction.__members__ else PlatformAction.NONE)
        command_2P = (PlatformAction(ai_2p_cmd)
                      if ai_2p_cmd in PlatformAction.__members__ else PlatformAction.NONE)

        self._frame_count += 1
        self._platform_1P.move(command_1P)
        self._platform_2P.move(command_2P)
        self._blocker.move()

        if not self._ball_served:
            self._wait_for_serving_ball(command_1P, command_2P)
        else:
            self._ball_moving()

        if self.get_game_status() != GameStatus.GAME_ALIVE:
            if self._game_over(self.get_game_status()):
                self._print_result()
                self._game_status = GameStatus.GAME_OVER
                return "QUIT"
            return "RESET"

        if not self.is_running:
            return "QUIT"

    def _game_over(self, status):
        """
        Check if the game is over
        """
        if status == GameStatus.GAME_1P_WIN:
            self._score[0] += 1
        elif status == GameStatus.GAME_2P_WIN:
            self._score[1] += 1
        else:  # Draw game
            self._score[0] += 1
            self._score[1] += 1

        is_game_over = (self._score[0] == self._game_over_score or
                        self._score[1] == self._game_over_score)

        return is_game_over

    def _print_result(self):
        """
        Print the result
        """
        if self._score[0] > self._score[1]:
            win_side = "1P"
        elif self._score[0] == self._score[1]:
            win_side = "No one"
        else:
            win_side = "2P"

        print("{} wins! Final score: {}-{}".format(win_side, *self._score))

    def _wait_for_serving_ball(self, action_1P: PlatformAction, action_2P: PlatformAction):
        self._ball.stick_on_platform(self._platform_1P.rect, self._platform_2P.rect)

        target_action = action_1P if self._ball.serve_from_1P else action_2P

        # Force to serve the ball after 150 frames
        if (self._frame_count >= 150 and
                target_action not in SERVE_BALL_ACTIONS):
            target_action = random.choice(SERVE_BALL_ACTIONS)

        if target_action in SERVE_BALL_ACTIONS:
            self._ball.serve(target_action)
            self._ball_served = True
            self._ball_served_frame = self._frame_count

    def _ball_moving(self):
        # Speed up the ball every 200 frames
        if (self._frame_count - self._ball_served_frame) % 100 == 0:
            # speed up per 100 frames
            self._ball.speed_up()

        self._ball.move()
        self._ball.check_bouncing(self._platform_1P, self._platform_2P, self._blocker)

    def get_data_from_game_to_player(self) -> dict:
        to_players_data = {}
        scene_info = {
            "frame": self._frame_count,
            "status": self.get_game_status(),
            "ball": self._ball.pos,
            "ball_speed": self._ball.speed,
            "ball_served":self._ball_served,
            "serving_side":"1P" if self._ball.serve_from_1P else "2P",
            "platform_1P": self._platform_1P.pos,
            "platform_2P": self._platform_2P.pos
        }

        if self._difficulty == "HARD":
            scene_info["blocker"] = self._blocker.pos
        else:
            scene_info["blocker"] = (0, 0)

        to_players_data[get_ai_name(0)] = scene_info
        to_players_data[get_ai_name(1)] = scene_info

        return to_players_data

    def get_game_status(self):
        if self._ball.rect.top > self._platform_1P.rect.bottom:
            self._game_status = GameStatus.GAME_2P_WIN
        elif self._ball.rect.bottom < self._platform_2P.rect.top:
            self._game_status = GameStatus.GAME_1P_WIN
        elif abs(min(self._ball.speed, key=abs)) > DRAW_BALL_SPEED:
            self._game_status = GameStatus.GAME_DRAW
        else:
            self._game_status = GameStatus.GAME_ALIVE

        return self._game_status

    def reset(self):
        print("reset pingpong")
        self._frame_count = 0
        self._game_status = GameStatus.GAME_ALIVE
        self._ball_served = False
        self._ball_served_frame = 0
        self._ball.reset()
        self._platform_1P.reset()
        self._platform_2P.reset()
        self._blocker.reset()

        # Initialize the position of the ball
        self._ball.stick_on_platform(self._platform_1P.rect, self._platform_2P.rect)

    @property
    def is_running(self):
        # print(self.get_game_status())
        return self._game_status != GameStatus.GAME_OVER

    def get_scene_init_data(self) -> dict:
        scene_init_data = {"scene": self.scene.__dict__, "assets": [

        ]}
        return scene_init_data

    @check_game_progress
    def get_scene_progress_data(self) -> dict:
        game_obj_list = [obj.get_object_data for obj in self._draw_group]

        create_1p_score = create_text_view_data("1P: " + str(self._score[0]),
                                                1,
                                                self.scene.height - 21,
                                                Platform.COLOR_1P,
                                                "18px Arial BOLD"
                                                )
        create_2p_score = create_text_view_data("2P: " + str(self._score[1]),
                                                1,
                                                4,
                                                Platform.COLOR_2P,
                                                "18px Arial BOLD"
                                                )
        create_speed_text = create_text_view_data("Speed: " + str(self._ball.speed),
                                                  self.scene.width - 120,
                                                  self.scene.height - 21,
                                                  "#FFFFFF",
                                                  "18px Arial BOLD"
                                                  )
        foreground = [create_1p_score, create_2p_score, create_speed_text]

        scene_progress = create_scene_progress_data(frame=self._frame_count, object_list=game_obj_list,
                                                    foreground=foreground)
        return scene_progress

    @check_game_result
    def get_game_result(self) -> dict:
        attachment = []
        if self._score[0] > self._score[1]:
            attachment = [
                {
                    "player": get_ai_name(0),
                    "rank": 1,
                    "score": self._score[0],
                    "status": "GAME_PASS",
                    "ball_speed": self._ball.speed,
                },
                {
                    "player": get_ai_name(1),
                    "rank": 2,
                    "score": self._score[1],
                    "status": "GAME_OVER",
                    "ball_speed": self._ball.speed,
                },

            ]
        elif self._score[0] < self._score[1]:
            attachment = [
                {
                    "player": get_ai_name(0),
                    "rank": 2,
                    "score": self._score[0],
                    "status": "GAME_OVER",
                    "ball_speed": self._ball.speed,
                },
                {
                    "player": get_ai_name(1),
                    "rank": 1,
                    "score": self._score[1],
                    "status": "GAME_PASS",
                    "ball_speed": self._ball.speed,

                },
            ]
        else:
            attachment = [
                {
                    "player": get_ai_name(0),
                    "rank": 1,
                    "score": self._score[0],
                    "status": "GAME_DRAW",
                    "ball_speed": self._ball.speed,
                },
                {
                    "player": get_ai_name(1),
                    "rank": 1,
                    "score": self._score[1],
                    "status": "GAME_DRAW",
                    "ball_speed": self._ball.speed,
                },
            ]
        return {
            "frame_used": self._frame_count,
            "state": GameResultState.FINISH,
            "attachment": attachment

        }

    def get_keyboard_command(self) -> dict:
        cmd_1P = ""
        cmd_2P = ""

        key_pressed_list = pygame.key.get_pressed()

        if key_pressed_list[pygame.K_PERIOD]:
            cmd_1P = PlatformAction.SERVE_TO_LEFT
        elif key_pressed_list[pygame.K_SLASH]:
            cmd_1P = PlatformAction.SERVE_TO_RIGHT
        elif key_pressed_list[pygame.K_LEFT]:
            cmd_1P = PlatformAction.MOVE_LEFT
        elif key_pressed_list[pygame.K_RIGHT]:
            cmd_1P = PlatformAction.MOVE_RIGHT
        else:
            cmd_1P = PlatformAction.NONE

        if key_pressed_list[pygame.K_q]:
            cmd_2P = PlatformAction.SERVE_TO_LEFT
        elif key_pressed_list[pygame.K_e]:
            cmd_2P = PlatformAction.SERVE_TO_RIGHT
        elif key_pressed_list[pygame.K_a]:
            cmd_2P = PlatformAction.MOVE_LEFT
        elif key_pressed_list[pygame.K_d]:
            cmd_2P = PlatformAction.MOVE_RIGHT
        else:
            cmd_2P = PlatformAction.NONE

        ai_1p = get_ai_name(0)
        ai_2p = get_ai_name(1)

        return {ai_1p: cmd_1P, ai_2p: cmd_2P}


from mlgame.game import physics
from mlgame.utils.enum import StringEnum, auto

from pygame.math import Vector2
import pygame
import random

PLATFORM_W = 40
PLATFORM_H = 10


class PlatformAction(StringEnum):
    SERVE_TO_LEFT = auto()
    SERVE_TO_RIGHT = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    NONE = auto()


SERVE_BALL_ACTIONS = (PlatformAction.SERVE_TO_LEFT, PlatformAction.SERVE_TO_RIGHT)


class Platform(pygame.sprite.Sprite):
    COLOR_1P = "#D6465C"  # Red
    COLOR_2P = "#5495FF"  # Blue

    def __init__(self, init_pos: tuple, play_area_rect: pygame.Rect,
                 side, *groups):
        super().__init__(*groups)

        self._play_area_rect = play_area_rect
        self._shift_speed = 5
        self._speed = [0, 0]
        self._init_pos = init_pos

        self.rect = pygame.Rect(*init_pos, PLATFORM_W, PLATFORM_H)

        if side == "1P":
            self._color = Platform.COLOR_1P
        elif side == "2P":
            self._color = Platform.COLOR_2P
            # self.rect.move_ip(0, -PLATFORM_H)
        else:
            self._color = Platform.COLOR_1P

    @property
    def pos(self):
        return self.rect.topleft

    def reset(self):
        self.rect.x, self.rect.y = self._init_pos

    def move(self, move_action: PlatformAction):
        if (move_action == PlatformAction.MOVE_LEFT and
                self.rect.left > self._play_area_rect.left):
            self._speed[0] = -self._shift_speed
        elif (move_action == PlatformAction.MOVE_RIGHT and
              self.rect.right < self._play_area_rect.right):
            self._speed[0] = self._shift_speed
        else:
            self._speed[0] = 0

        self.rect.move_ip(*self._speed)

    @property
    def get_object_data(self):
        return {"type": "rect",
                "name": "platform",
                "x": self.rect.x,
                "y": self.rect.y,
                "width": self.rect.width,
                "height": self.rect.height,
                "color": self._color}


class Blocker(pygame.sprite.Sprite):
    def __init__(self, init_pos_y, play_area_rect: pygame.Rect, *groups):
        super().__init__(*groups)

        self._play_area_rect = play_area_rect
        self._speed = [random.choice((5, -5)), 0]

        self.rect = pygame.Rect(
            random.randrange(0, play_area_rect.width - 10, 20), init_pos_y, 30, 20)
        # self.image = self._create_surface()
        self._color = "#D5E000"

    @property
    def pos(self):
        return self.rect.topleft

    def reset(self):
        self.rect.x = random.randrange(0, self._play_area_rect.width - 10, 20)
        self._speed = [random.choice((5, -5)), 0]

    def move(self):
        self.rect.move_ip(self._speed)

        if self.rect.left <= self._play_area_rect.left:
            self.rect.left = self._play_area_rect.left
            self._speed[0] *= -1
        elif self.rect.right >= self._play_area_rect.right:
            self.rect.right = self._play_area_rect.right
            self._speed[0] *= -1

    @property
    def get_object_data(self):
        return {"type": "rect",
                "name": "blocker",
                "x": self.rect.x,
                "y": self.rect.y,
                "width": self.rect.width,
                "height": self.rect.height,
                "color": self._color}


class Ball(pygame.sprite.Sprite):
    def __init__(self, play_area_rect: pygame.Rect, enable_slide_ball: bool, *groups):
        super().__init__(*groups)

        self._play_area_rect = play_area_rect
        self._speed = [0, 0]
        self._size = [5, 5]
        self._do_slide_ball = enable_slide_ball

        self.serve_from_1P = True

        self.rect = pygame.Rect(0, 0, *self._size)
        # self.image = self._create_surface()
        self._color = "#42E27E"
        # Used in additional collision detection
        self.last_pos = pygame.Rect(self.rect)

    @property
    def pos(self):
        return self.rect.topleft

    @property
    def speed(self):
        return tuple(self._speed)

    def reset(self):
        """
        Reset the ball status
        """
        self._speed = [0, 0]
        # Change side next time
        self.serve_from_1P = not self.serve_from_1P

    def stick_on_platform(self, platform_1P_rect, platform_2P_rect):
        """
        Stick on the either platform according to the status of `_serve_from_1P`
        """
        if self.serve_from_1P:
            self.rect.centerx = platform_1P_rect.centerx
            self.rect.y = platform_1P_rect.top - self.rect.height
        else:
            self.rect.centerx = platform_2P_rect.centerx
            self.rect.y = platform_2P_rect.bottom

    def serve(self, serve_ball_action: PlatformAction):
        """
        Set the ball speed according to the action of ball serving
        """
        self._speed[0] = {
            PlatformAction.SERVE_TO_LEFT: -7,
            PlatformAction.SERVE_TO_RIGHT: 7,
        }.get(serve_ball_action)

        self._speed[1] = -7 if self.serve_from_1P else 7

    def move(self):
        self.last_pos.topleft = self.rect.topleft
        self.rect.move_ip(self._speed)

    def speed_up(self):
        self._speed[0] += 1 if self._speed[0] > 0 else -1
        self._speed[1] += 1 if self._speed[1] > 0 else -1

    def check_bouncing(self, platform_1p: Platform, platform_2p: Platform,
                       blocker: Blocker):
        # If the ball hits the play_area, adjust the position first
        # and preserve the speed after bouncing.
        hit_box = physics.rect_break_or_contact_box(self.rect, self._play_area_rect)
        if hit_box:
            self.rect, speed_after_hit_box = (
                physics.bounce_in_box(self.rect, self._speed, self._play_area_rect))

        # If the ball hits the specified sprites, adjust the position again
        # and preserve the speed after bouncing.
        hit_sprite = self._check_ball_hit_sprites((platform_1p, platform_2p, blocker))
        if hit_sprite:
            self.rect, speed_after_bounce = physics.bounce_off(
                self.rect, self._speed,
                hit_sprite.rect, hit_sprite._speed)

            # Check slicing ball when the ball is caught by the platform
            if (self._do_slide_ball and
                    ((hit_sprite is platform_1p and speed_after_bounce[1] < 0) or
                     (hit_sprite is platform_2p and speed_after_bounce[1] > 0))):
                speed_after_bounce[0] = self._slice_ball(self._speed, hit_sprite._speed[0])

        # Decide the final speed
        if hit_box:
            self._speed[0] = speed_after_hit_box[0]
        if hit_sprite:
            self._speed[1] = speed_after_bounce[1]
            if not hit_box:
                self._speed[0] = speed_after_bounce[0]

    def _check_ball_hit_sprites(self, sprites):
        """
        Get the first sprite in the `sprites` that the ball hits

        @param sprites An iterable object that storing the target sprites
        @return The first sprite in the `sprites` that the ball hits.
                Return None, if none of them is hit by the ball.
        """
        for sprite in sprites:
            if physics.moving_collide_or_contact(self, sprite):
                return sprite

        return None

    def _slice_ball(self, ball_speed, platform_speed_x):
        """
        Check if the platform slices the ball, and modify the ball speed
        """
        # The y speed won't be changed after ball slicing.
        # It's good for determining the x speed.
        origin_ball_speed = abs(ball_speed[1])

        # If the platform moves at the same direction as the ball moving,
        # speed up the ball.
        if platform_speed_x * ball_speed[0] > 0:
            origin_ball_speed += 3
        # If they move to the different direction,
        # reverse the ball direction.
        elif platform_speed_x * ball_speed[0] < 0:
            origin_ball_speed *= -1

        return origin_ball_speed if ball_speed[0] > 0 else -origin_ball_speed

    @property
    def get_object_data(self):
        return {"type": "rect",
                "name": "ball",
                "x": self.rect.x,
                "y": self.rect.y,
                "width": self.rect.width,
                "height": self.rect.height,
                "color": self._color}