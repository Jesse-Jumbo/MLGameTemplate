import pygame.mixer


def create_music_data(music_id: str, music_path: str):
    return {
        "music_id": music_id
        , "music_path": music_path
    }


class SoundController:
    def __init__(self, is_sound: bool, music_data_list: list):
        self._is_sound = is_sound
        if not self._is_sound:
            return
        pygame.mixer.init()
        self._music_obj = {}
        for music_data in music_data_list:
            self._music_obj[music_data["music_id"]] = pygame.mixer.Sound(music_data["music_path"])
        print(self._music_obj)

    def play_music(self, music_path: str, volume: float) -> None:
        if not self._is_sound:
            return
        pygame.mixer.init()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

    def play_sound(self, music_id: str, volume: float, maz_time: int) -> None:
        if not self._is_sound:
            return
        sound_obj = self._music_obj[music_id]
        sound_obj.set_volume(volume)
        sound_obj.play(maxtime=maz_time)
