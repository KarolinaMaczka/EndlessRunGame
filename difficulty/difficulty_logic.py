from multiprocessing import Queue
import random

from data_manager import DataManager
import time
import random
import pandas as pd
import numpy as np
from config.logger import get_game_logger
import os

logger = get_game_logger()


class DifficultyLogic:

    DIFFICULTY_CHANGE = {
        'happy': 1,
        'sad': -1,
        'sad_low': 1,
        'sad_high': -1,
        'angry': -2,
        'fear': -1,
        'surprise': 0,
        'disgust': 0,
        'neutral': 0
    }

    def __init__(self, data_manager: DataManager, context):
        self.counter = 0
        self.context = context
        self.data_manager = data_manager
        self.change_difficulty = bool(random.randint(0, 1))
        self.data_manager.add_change_difficulty(self.change_difficulty)

        if os.path.exists('difficulty\\first_emotion_percentage-satisfaction.csv'):
            self.emotion_distribution:pd.DataFrame = pd.read_csv('difficulty\\first_emotion_percentage-satisfaction.csv')
            self.emotion_distribution_1 = self.emotion_distribution[self.emotion_distribution['player_satisfaction_combined'] == 1].set_index('first_emotion')['percentage'].to_dict()
            self.emotion_distribution_3 = self.emotion_distribution[self.emotion_distribution['player_satisfaction_combined'] == 3].set_index('first_emotion')['percentage'].to_dict()
            self.emotion_distribution_5 = self.emotion_distribution[self.emotion_distribution['player_satisfaction_combined'] == 5].set_index('first_emotion')['percentage'].to_dict()
        self.emotions_count = self.create_emotion_count_dict()
        self.emotions_count_one_round = self.create_emotion_count_dict()
        self.emotions_count_percentage = dict()
        self.second_emotions_count = self.create_emotion_count_dict()
        self.second_emotions_count_one_round = self.create_emotion_count_dict()
        self.second_emotions_count_percentage = dict()

    def create_emotion_count_dict(self):
        return dict.fromkeys(['happy', 'neutral', 'sad', 'sad_low', 'sad_high', 'angry', 'fear','surprise', 'disgust'], 0)

    def update(self, player_z: float, emotion_queue: Queue):
        # logger.info('Updating difficulty based on emotions')
        if not emotion_queue.empty():
            emotions = emotion_queue.get() # emotions = (('happy', 0.9), ('neutral', 0.1), 1.0)
            # for emotion in emotions:
            if emotions[1][0] == 'sad' and emotions[1][1] < 0.1:
                second_emotion = 'sad_low'
            elif emotions[1][0] == 'sad' and emotions[1][1] >= 0.1:
                second_emotion = 'sad_high'
            else:
                second_emotion = emotions[1][0]
            self.emotions_count_one_round[emotions[0][0]] += 1
            self.second_emotions_count_one_round[second_emotion] += 1
            emotions_and_position = (*emotions, player_z)
            self.data_manager.add_emotion(emotions_and_position)

            if self.change_difficulty:
                self.counter += 1
                if self.counter == 10:
                    self.update_difficulty(emotions)
                    self.counter = 0
            else: # change difficulty level at random every 10 rounds
                self.counter += 1
                if self.counter == 10:
                    self.context.change_difficulty(random.choice([-1, 0, 1]))
                    self.counter = 0
        # time.sleep(0.1)

    def update_difficulty(self, emotions):
        # Create distribution of emotions based on emotion_count
        logger.info(f'Emotions count one round: {self.emotions_count_one_round}')
        self.emotions_count = {k: v + self.emotions_count_one_round[k] for k, v in self.emotions_count.items()}
        self.emotions_count_one_round = self.create_emotion_count_dict() 
        self.emotions_count_percentage = {k: v / sum(self.emotions_count.values()) for k, v in self.emotions_count.items()}
        logger.info(f'Emotions count: {self.emotions_count}')
        logger.info(f'Emotions count percentage: {self.emotions_count_percentage}')

        logger.info(f'Second emotions count one round: {self.second_emotions_count_one_round}')
        self.second_emotions_count = {k: v + self.second_emotions_count_one_round[k] for k, v in self.second_emotions_count.items()}
        self.second_emotions_count_one_round = self.create_emotion_count_dict()
        self.second_emotions_count_percentage = {k: v / sum(self.second_emotions_count.values()) for k, v in self.second_emotions_count.items()}
        logger.info(f'Second emotions count: {self.second_emotions_count}')
        logger.info(f'Second emotions count percentage: {self.second_emotions_count_percentage}')


        # Instructions for changing difficulty based on emotions
        # ------------------------------------------------------
        # If there are any other emotions than neutral, apply the change for the one with the most appearances
        # If there is only neutral emotion, check second emotion
            # If there is anger or happy/fear, apply the change for the one with the most appearances
            # If there is only neutral and sad, check further
                # For sadness which has confidence less than 0.1 assume that it's focus (level up)
                # For sadness which has confidence more than 0.1 assume that it is sadness (level down)
                # apply the change for the one with the most appearances

        if self.emotions_count['neutral'] == 10:
            logger.info('Neutral emotion is prevailing, checking further')
            self.check_dominant_emotion(self.second_emotions_count_one_round)
        else:
            self.check_dominant_emotion(self.emotions_count_one_round)

    def check_dominant_emotion(self, emotions_count_dict):
        dominant_emotion = max(emotions_count_dict, key=emotions_count_dict.get)
        logger.info('Changing difficulty based on: ' + dominant_emotion + ' | change: ' + str(self.DIFFICULTY_CHANGE[dominant_emotion]))
        self.context.change_difficulty(self.DIFFICULTY_CHANGE[dominant_emotion])