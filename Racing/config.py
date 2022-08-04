import sys
from os import path

from MyGame.src.MyGame import MyGame

sys.path.append(path.dirname(__file__))
GAME_SETUP = {
    "game": MyGame,
}
