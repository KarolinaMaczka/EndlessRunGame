from multiprocessing import Queue
from data_manager import DataManager
import time

class DifficultyLogic():
    def __init__(self, emotion_queue: Queue, data_manager: DataManager):
        self.emotion_queue = emotion_queue
        self.data_manager = data_manager

    def update(self, player_z: float):
        while True:
            if not self.emotion_queue.empty():
                emotions = self.emotion_queue.get()
                emotions_and_position = (emotions, player_z)
                self.data_manager.add_emotion(emotions_and_position)
                self.update_difficulty(emotions)
            time.sleep(0.1)

    def update_difficulty(self, emotions:tuple):
        pass


