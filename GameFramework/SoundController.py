from os import path

import pygame.mixer


def create_sounds_data(id: str, name: str):
    return {
        "_id": id
        , "_name": name
    }


def create_bgm_data(name: str, volume: float):
    return {
        "_name": name
        , "_volume": volume
    }


class SoundController:
    def __init__(self, sound_path: str, sounds_data_list: list):
        self._sound_path = sound_path
        if not self._sound_path:
            return
        self._sounds_obj = {}
        pygame.mixer.init()
        for sounds_data in sounds_data_list:
            sound_data = path.join(self._sound_path, sounds_data["_name"])
            self._sounds_obj[sounds_data["_id"]] = pygame.mixer.Sound(sound_data)

    def play_music(self, bgm_data: dict) -> None:
        if not self._sound_path:
            return
        pygame.mixer.init()
        pygame.mixer.music.load(path.join(self._sound_path, bgm_data["_name"]))
        pygame.mixer.music.set_volume(bgm_data["_volume"])
        pygame.mixer.music.play(-1)

    def play_sound(self, id: str, volume: float, maz_time: int) -> None:
        if not self._sound_path:
            return
        sound_obj = self._sounds_obj[id]
        sound_obj.set_volume(volume)
        sound_obj.play(maxtime=maz_time)
