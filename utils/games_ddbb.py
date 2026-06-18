import os
import json

from pages.game import Game
from cfg import app_config as conf

class GamesDDBB:
    def __init__(self):
        self.games = self.get_games_from_file(conf.SAVEFILE_PATH)
    
    def get_games_from_file(self, file_path):
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as file:
                json.dump([], file)
            return []

        with open(file_path, "r") as file:
            data = json.load(file)
            self.games = [Game.from_json(game_data) for game_data in data]
        return self.games
    
    def save_games_to_file(self, file_path):
        with open(file_path, "w") as file:
            data = [game.to_json() for game in self.games]
            json.dump(data, file, indent=4)

    def add_game(self, game):
        self.games.append(game)
        self.save_games_to_file(conf.SAVEFILE_PATH)
    def remove_game(self, game):
        self.games.remove(game)
        self.save_games_to_file(conf.SAVEFILE_PATH)

    def modify_game(self, old_game, new_game):
        index = self.games.index(old_game)
        self.games[index] = new_game
        self.save_games_to_file(conf.SAVEFILE_PATH)
        
    def get_games(self):
        return self.games