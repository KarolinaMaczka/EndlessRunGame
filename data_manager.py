import os
from datetime import datetime
import json

from config.config import config
from config.constants import CollisionSide, CollisionType
from entities.obstacles.obstacle import Obstacle
from entities.player import Player

from multiprocessing import Manager

class DataManager:
    def __init__(self, list_manager: Manager): # type: ignore
        self.obstacle_data = []
        self.hit_obstacles = []
        self.player_satisfaction = -1
        self.player_emotions = []
        self.map_data = []
        self.player_emotions = list_manager.list()
        self.score = 0
        self.playing_time = 0
        self.difficulties = []
        self.__folder = config['player_data']['player_data.folder']
        os.makedirs(self.__folder, exist_ok=True)

    def save(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_path = os.path.join(self.__folder, f'game_data_{timestamp}.json')

        data_to_save = {
            "obstacle_data": self.obstacle_data,
            "hit_obstacles": self.hit_obstacles,
            "player_satisfaction": self.player_satisfaction,
            "map_data": self.map_data,
            "player_emotions": list(self.player_emotions),
            'score': self.score,
            'playing_time': self.playing_time,
            'difficulties': self.difficulties,
        }

        try:
            with open(file_path, 'w') as f:
                json.dump(data_to_save, f, indent=1)
            print(f"saved data {file_path}")
        except Exception as e:
            print(f"error saving data: {e}")
            return

    def clean_data(self):
        self.obstacle_data = []
        self.hit_obstacles = []
        self.player_satisfaction = -1
        self.player_emotions[:] = []
        self.map_data = []
        self.score = 0
        self.playing_time = 0
        self.difficulties = []

    def add_collision(self, side: CollisionSide, collision_type: CollisionType, obstacle: Obstacle, player: Player):
        self.hit_obstacles.append(
            (str(type(obstacle.parentt).__name__), str(side.value), str(collision_type.value),
             obstacle.parentt.position_z, obstacle.parentt.lane,
             player.position.z, player.position.x,
             player.position.y))

    def add_obstacle_data(self, obstacle_type):
        self.obstacle_data.append((str(obstacle_type.obstacle.__name__), obstacle_type.position_z, obstacle_type.lane))

    def add_emotion(self, dominant_emotion, second_dominant_emotion):
        self.player_emotions.append((dominant_emotion, second_dominant_emotion))

    def add_map_data(self, mapp_data: tuple):
        self.map_data.append(mapp_data)

    def add_player_satisfaction(self, satisfaction):
        self.player_satisfaction = satisfaction