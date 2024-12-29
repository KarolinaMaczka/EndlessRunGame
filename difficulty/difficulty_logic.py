from multiprocessing import Queue
from data_manager import DataManager
import time
import pandas as pd
import numpy as np
from config.logger import get_game_logger
import os

logger = get_game_logger()


class DifficultyLogic:
    def __init__(self, data_manager: DataManager, context):
        self.counter = 0
        self.context = context
        self.data_manager = data_manager
        self.difficulty_value = self.context.obstacle_generator.difficulty_level.value
        self.starting_difficulty = self.context.difficulty_level_new

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
                self.update_difficulty(emotions)
                self.counter = 0
        # time.sleep(0.1)

    def update_difficulty(self, emotions):
        pass
        # Create distribution of emotions
        self.emotions_count_percentage = {k: v / sum(self.emotions_count.values()) for k, v in self.emotions_count.items()}
        logger.info(f'Emotions count: {self.emotions_count}')
        logger.info(f'Emotions count percentage: {self.emotions_count_percentage}')

        # TODO - change exact logic
        dominant_emotion = emotions[0]
        second_dominant_emotion = emotions[1]
        logger.info(f'Logic change: Dominant emotion: {dominant_emotion}, second dominant emotion: {second_dominant_emotion}')
        if str(dominant_emotion[0]) == 'happy' or str(second_dominant_emotion[0]) == 'happy':
            print(f'higher level {dominant_emotion}, {second_dominant_emotion}')
            self.context.change_difficulty(1)
        elif str(dominant_emotion[0]) == 'neutral':
            print(f'skip changing levels')
        elif str(dominant_emotion[0]) == 'sad':
            print(f'lower level {dominant_emotion}, {second_dominant_emotion}')
            self.context.change_difficulty(-1)

    def level_up_difficulty(self):
        final_difficulty = self.difficulty_value + 1
        if abs(final_difficulty - self.starting_difficulty) <= 2:
            self.difficulty_value += 1
            logger.info(f'Level up difficulty to {self.difficulty_value}')

    def level_down_difficulty(self):
        final_difficulty = self.difficulty_value - 1
        if abs(final_difficulty - self.starting_difficulty) <= 2:
            self.difficulty_value -= 1
            logger.info(f'Level down difficulty to {self.difficulty_value}')
