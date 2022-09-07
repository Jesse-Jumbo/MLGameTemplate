from GameFramework.SoundController import SoundController


class TankSoundController(SoundController):
    def __init__(self, is_sound, music_data_list):
        super().__init__(is_sound, music_data_list)

    def play_shoot_sound(self):
        self.play_sound("shoot", 0.03, -1)

    def play_touch_sound(self):
        self.play_sound("touch", 0.1, -1)


