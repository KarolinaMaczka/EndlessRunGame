import os
from datetime import datetime
import json

from config.config import config


class DataManager:
    def __init__(self):
        self.obstacle_data = []
        self.hit_obstacles = []
        self.player_satisfaction = -1
        self.player_emotions = []
        self.__folder = config['player_data']['player_data.folder']
        os.makedirs(self.__folder, exist_ok=True)

    def save(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_path = os.path.join(self.__folder, f'game_data_{timestamp}.json')

        data = {
            "obstacle_data": self.obstacle_data,
            "hit_obstacles": self.hit_obstacles,
            "player_satisfaction": self.player_satisfaction,
            "player_emotions": self.player_emotions,
        }

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=1)

        print(f"saved  data {file_path}")
