from multiprocessing import Queue
from data_manager import DataManager
import time
import pandas as pd
import numpy as np
from config.logger import get_game_logger
import os

logger = get_game_logger()


class DifficultyLogic:
    def __init__(self, data_manager: DataManager, difficulty_value):
        self.counter = 0
        self.data_manager = data_manager
        self.difficulty_value = difficulty_value
        if os.path.exists('difficulty\\first_emotion_percentage-satisfaction.csv'):
            self.emotion_distribution:pd.DataFrame = pd.read_csv('difficulty\\first_emotion_percentage-satisfaction.csv')
            self.emotion_distribution_1 = self.emotion_distribution[self.emotion_distribution['player_satisfaction_combined'] == 1].set_index('first_emotion')['percentage'].to_dict()
            self.emotion_distribution_3 = self.emotion_distribution[self.emotion_distribution['player_satisfaction_combined'] == 3].set_index('first_emotion')['percentage'].to_dict()
            self.emotion_distribution_5 = self.emotion_distribution[self.emotion_distribution['player_satisfaction_combined'] == 5].set_index('first_emotion')['percentage'].to_dict()
        self.emotions_count = dict.fromkeys(['happy', 'neutral', 'sad', 'angry', 'fear','surprise', 'disgust'], 0)
        self.emotions_count_percentage = dict()
        
    def update(self, player_z: float, emotion_queue: Queue):
        # logger.info('Updating difficulty based on emotions')
        # while True:
        if not emotion_queue.empty():
            emotions = emotion_queue.get() # emotions = (('happy', 0.9), ('neutral', 0.1))
            # for emotion in emotions:
            self.emotions_count[emotions[0][0]] += 1
            emotions_and_position = (*emotions, player_z)
            self.data_manager.add_emotion(emotions_and_position)

            self.counter += 1
            if self.counter == 10:
                self.update_difficulty()
                self.counter = 0
        # time.sleep(0.1)

    def update_difficulty(self):
        pass
        # Create distribution of emotions
        self.emotions_count_percentage = {k: v / sum(self.emotions_count.values()) for k, v in self.emotions_count.items()}
        logger.info(f'Emotions count: {self.emotions_count}')
        logger.info(f'Emotions count percentage: {self.emotions_count_percentage}')

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
