import os

BGCOLOR = "#18191A"
BGTOPBARCOLOR = "#242526"
BGOTHERCOLOR = "#404345"
HOVERCOLOR = "#3A3B3C"
FGCOLOR = "#E4E6EB"
FGSECONDARYCOLOR = "#B0B3B8"

PROYECT_DIR = os.path.dirname(os.path.dirname(__file__))

DEFAULT_IMAGES_PATH = os.path.join(PROYECT_DIR, "assets", "default_images")

GAME_IMAGES_PATH = os.path.join(PROYECT_DIR, "assets", "game_images")
HEART_ICON_PATH = os.path.join(DEFAULT_IMAGES_PATH, "fav.png")
ADD_ICON_PATH = os.path.join(DEFAULT_IMAGES_PATH, "add.png")
SAMPLE_GRID_IMAGE_PATH = os.path.join(DEFAULT_IMAGES_PATH, "sample_grid.jpg")

SAVEFILE_PATH = os.path.join(PROYECT_DIR, "data", "games.json")