from os import path

import pygame.mixer


def create_music_data(id: str, name: str):
    return {
        "_id": id
        , "_name": name
    }


class SoundController:
    def __init__(self, sound_path: str, music_data_list: list):
        self._sound_path = sound_path
        if not self._sound_path:
            return
        self._music_obj = {}
        pygame.mixer.init()
        for music_data in music_data_list:
            sound_data = path.join(self._sound_path, music_data["_name"])
            self._music_obj[music_data["_id"]] = pygame.mixer.Sound(sound_data)

    def play_music(self, bgm_path: str, volume: float) -> None:
        if not self._sound_path:
            return
        pygame.mixer.init()
        pygame.mixer.music.load(path.join(self._sound_path, bgm_path))
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

    def play_sound(self, id: str, volume: float, maz_time: int) -> None:
        if not self._sound_path:
            return
        sound_obj = self._music_obj[id]
        sound_obj.set_volume(volume)
        sound_obj.play(maxtime=maz_time)
