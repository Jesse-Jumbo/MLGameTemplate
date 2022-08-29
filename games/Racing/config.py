import sys
from os import path
sys.path.append(path.dirname(__file__))

from src.MyGame import MyGame

GAME_SETUP = {
    "game": MyGame,
}
