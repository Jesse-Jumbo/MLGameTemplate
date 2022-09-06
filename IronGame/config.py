import sys
from os import path

sys.path.append(path.dirname(__file__))
from src.IronGame import IronGame

GAME_SETUP = {
    "game": IronGame,
}
