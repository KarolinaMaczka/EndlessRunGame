import os
from datetime import datetime
import json

from config.config import config

from multiprocessing import Manager

class DataManager:
    def __init__(self, list_manager: Manager): # type: ignore
        self.obstacle_data = []
        self.hit_obstacles = []
        self.player_satisfaction = -1
        self.player_emotions = list_manager.list()
        self.__folder = config['player_data']['player_data.folder']
        os.makedirs(self.__folder, exist_ok=True)

    def save(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_path = os.path.join(self.__folder, f'game_data_{timestamp}.json')

        data = {
            "obstacle_data": self.obstacle_data,
            "hit_obstacles": self.hit_obstacles,
            "player_satisfaction": self.player_satisfaction,
            "player_emotions": list(self.player_emotions),
        }

        with open(file_path, 'w') as f:
            json.dump(data, f)

        print(f"saved  data {file_path}")

    def add_emotion(self, dominant_emotion, second_dominant_emotion):
        self.player_emotions.append((dominant_emotion, second_dominant_emotion))
