import pygame.mixer


class SoundController:
    def play_music(self, music_path: str, volume: float) -> None:
        pygame.mixer.init()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

    def play_sound(self, music_path: str, volume: float, maz_time: int) -> None:
        pygame.mixer.init()
        pygame.mixer.Sound(music_path).play(maxtime=maz_time).set_volume(volume)


