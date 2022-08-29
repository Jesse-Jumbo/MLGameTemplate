import sys
from os import path

from src.MyGame import MyGame

sys.path.append(path.dirname(__file__))
GAME_SETUP = {
    "game": MyGame,
}
