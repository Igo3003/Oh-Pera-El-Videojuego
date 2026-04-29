import os
import sys

def get_base_path():
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = get_base_path()

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")

DATA_DIR = os.path.join(BASE_DIR, "data")
ARCHIVO_LOGROS = os.path.join(DATA_DIR, "logros.txt")