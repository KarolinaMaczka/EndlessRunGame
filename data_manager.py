import os
import threading
from datetime import datetime
import json

from config.config import config
from config.constants import CollisionSide, CollisionType
from config.logger import get_game_logger
from config.utils import catch_exceptions
from entities.obstacles.obstacle import Obstacle
from entities.player import Player
from multiprocessing import Manager
logger = get_game_logger()
import os
import requests
from dotenv import load_dotenv
load_dotenv()

class DataManager:
    def __init__(self, list_manager: Manager):

        self.obstacle_data = []
        self.hit_obstacles = []
        self.player_satisfaction = -1
        self.player_emotions = []
        self.map_data = []
        self.player_emotions = list_manager.list()
        self.score = 0
        self.playing_time = 0
        self.difficulties = []
        self.send_data_enabled = True
        self.__folder = config['player_data']['player_data.folder']
        os.makedirs(self.__folder, exist_ok=True)

    def save(self):
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

        if self.send_data_enabled:
            try:
                thread = threading.Thread(target=self.send_data, args=(data_to_save,))
                thread.start()
            except Exception as e:
                try:
                    self.send_data(data_to_save)
                except Exception as e:
                    self.save_csv(data_to_save)
        else:
            self.save_csv(data_to_save)

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

    def add_emotion(self, emotions: tuple):
        self.player_emotions.append(emotions)

    def add_map_data(self, mapp_data: tuple):
        self.map_data.append(mapp_data)

    def add_player_satisfaction(self, satisfaction):
        self.player_satisfaction = satisfaction

    @catch_exceptions
    def save_csv(self, data_to_save):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_path = os.path.join(self.__folder, f'game_data_{timestamp}.json')

        try:
            with open(file_path, 'w') as f:
                json.dump(data_to_save, f, indent=1)
            logger.info(f"saved data {file_path}")
        except Exception as e:
            logger.error(f"error saving data: {e}")
            return

    @catch_exceptions
    def send_data(self, data_to_save):
        api_key = os.getenv("API_KEY")
        url = "https://karolinamaczka.pythonanywhere.com/player-data"

        try:
            response = requests.post(
                url,
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": api_key
                },
                json=data_to_save
            )

            if response.status_code == 200:
                logger.info(f"Data was send")
            else:
                self.save()
                logger.error(f"Error while sending data, code: {response.status_code}")
        except Exception as e:
            self.save()
            logger.error(f"Error sending data: {e}")
