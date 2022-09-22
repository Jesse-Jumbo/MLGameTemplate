import sys
from os import path

sys.path.append(path.dirname(__file__))
from src.Game import Game

GAME_SETUP = {
    "game": Game,
}

