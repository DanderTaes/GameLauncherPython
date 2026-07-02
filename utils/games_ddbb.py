import os
import json

from utils.ddbb import DDBBParent
from pages.game import Game
from cfg import app_config as conf

class GamesDDBB(DDBBParent):
    def __init__(self):
        super().__init__()
        self.path = conf.SAVEFILE_PATH
        self.data_list = self.get_list_from_ddbb()
    