import sys
from os import path

from Racing.src.MyGame import MyGame

sys.path.append(path.dirname(__file__))
GAME_SETUP = {
    "game": MyGame,
}
