import sys
from os import path

sys.path.append(path.dirname(__file__))
from src.SampleGame import SampleGame

GAME_SETUP = {
    "game": SampleGame,
}
