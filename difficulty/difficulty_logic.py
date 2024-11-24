from multiprocessing import Queue
from data_manager import DataManager
import time
from config.logger import get_game_logger

logger = get_game_logger()


class DifficultyLogic:
    def __init__(self, data_manager: DataManager, difficulty_value):
        self.data_manager = data_manager
        self.difficulty_value = difficulty_value

    def update(self, player_z: float, emotion_queue: Queue):
        # logger.info('Updating difficulty based on emotions')
        # while True:
        if not emotion_queue.empty():
            emotions = emotion_queue.get()
            emotions_and_position = (*emotions, player_z)
            self.data_manager.add_emotion(emotions_and_position)
            self.update_difficulty(emotions)
        # time.sleep(0.1)

    def update_difficulty(self, emotions: tuple):
        pass
        # TODO - uncomment this code for changing difficulty based on emotions
        # dominant_emotion = emotions[0]
        # second_dominant_emotion = emotions[1]
        # logger.info(f'Logic change: Dominant emotion: {dominant_emotion}, second dominant emotion: {second_dominant_emotion}')
        # if dominant_emotion == 'happy':
        #     self.difficulty_value = 1
        #     logger.info('Difficulty set to 1 - difficulty logic')
        # elif dominant_emotion == 'neutral' or dominant_emotion == 'sad':
        #     if random() < 0.5:
        #         self.difficulty_value = 5
        #         logger.info('Difficulty set to 2 - difficulty logic')
        #     else:  
        #         self.difficulty_value = 9
        #         logger.info('Difficulty set to 9 - difficulty logic')
        # elif dominant_emotion == 'angry':
        #     self.difficulty_value = 10
        #     logger.info('Difficulty set to 10 - difficulty logic')
