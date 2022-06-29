import pygame
import sys

from mlgame.game.generic import quit_or_esc

from FindTheWay.src.FindTheWay import FindTheWay

sys.path.append(r"../..")
from mlgame.view.view import PygameView

FPS = 30
if __name__ == '__main__':
    pygame.init()
    game = FindTheWay(time_limit=300, sound="off")
    scene_init_info_dict = game.get_scene_init_data()
    game_view = PygameView(scene_init_info_dict)
    frame_count = 0
    while game.is_running and not quit_or_esc():
        pygame.time.Clock().tick_busy_loop(FPS)
        commands = game.get_keyboard_command()
        game.update(commands)
        game_progress_data = game.get_scene_progress_data()
        game_view.draw(game_progress_data)
        frame_count += 1
        # print(frame_count)

    pygame.quit()