import sys
from os import path

sys.path.append(path.dirname(__file__))
from src.TankMan import TankMan

GAME_SETUP = {
    "game": TankMan,
}

