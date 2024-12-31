from multiprocessing import Queue
from data_manager import DataManager
import time
import random
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
        return dict.fromkeys(['happy', 'neutral', 'sad', 'angry', 'fear','surprise', 'disgust'], 0)

    def update(self, player_z: float, emotion_queue: Queue):
        # logger.info('Updating difficulty based on emotions')
        if not emotion_queue.empty():
            emotions = emotion_queue.get() # emotions = (('happy', 0.9), ('neutral', 0.1), 1.0)
            # for emotion in emotions:
            self.emotions_count_one_round[emotions[0][0]] += 1
            self.second_emotions_count_one_round[emotions[1][0]] += 1
            emotions_and_position = (*emotions, player_z)
            self.data_manager.add_emotion(emotions_and_position)

            self.counter += 1
            if self.counter == 10:
                self.update_difficulty(emotions)
                self.counter = 0
        # time.sleep(0.1) for testing purposes (because otherwise tests wont work)
        
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


        # TODO: Implement logic based on instructions below
        # If there are any other emotions than neutral, apply the change for the one with the most appearances
        # If there is only neutral emotion, check second emotion
            # If there is anger or happy/fear, apply the change for the one with the most appearances
            # If there is only neutral and sad, check further
                # For sadness which has confidence less than 0.1 assume that it's focus (level up)
                # For sadness which has confidence more than 0.1 assume that it is sadness (level down)
                # apply the change for the one with the most appearances



        # dominant_emotion = emotions[0]
        # second_dominant_emotion = emotions[1]
        # logger.info(f'Logic change: Dominant emotion: {dominant_emotion}, second dominant emotion: {second_dominant_emotion}')
        # if str(dominant_emotion[0]) == 'happy' or str(second_dominant_emotion[0]) == 'happy':
        #     print(f'Detected dominant happy emotion. Leveling Up. Emotions: {dominant_emotion}, {second_dominant_emotion}')
        #     self.context.change_difficulty(1)
        # elif str(dominant_emotion[0]) == 'sad':
        #     logger.info(f'Detected dominant sad emotion. Leveling Down. Emotions: {dominant_emotion}, {second_dominant_emotion}')
        #     self.context.change_difficulty(-1)
        # elif str(dominant_emotion[0]) == 'angry':
        #     logger.info(f'Detected dominant angry emotion. Leveling Down. Emotions: {dominant_emotion}, {second_dominant_emotion}')
        #     self.context.change_difficulty(-2)
        # elif str(dominant_emotion[0]) == 'neutral':
        #     logger.info(f'Detected dominant neutral emotion. Looking for 2nd emotion. Emotions: {dominant_emotion}, {second_dominant_emotion}')
        #     if str(second_dominant_emotion[0])== 'happy':
        #         logger.info(f'Detected second dominant happy emotion. Leveling Up. Emotions: {dominant_emotion}, {second_dominant_emotion}')
        #         self.context.change_difficulty(1)
        #     if str(second_dominant_emotion[0])== 'angry':
        #         logger.info(f'Detected second dominant angry emotion. Leveling Down. Emotions: {dominant_emotion}, {second_dominant_emotion}')
        #         self.context.change_difficulty(-2)
        #     if str(second_dominant_emotion[0])== 'sad':
        #         logger.info(f'Detected second dominant sad emotion. Leveling up with random probability. Emotions: {dominant_emotion}, {second_dominant_emotion}')
        #         if random.random() < 0.5:
        #             self.context.change_difficulty(1)
        # else:
        #     logger.info(f'No importatnt emotion detected. Skip changing. Emotions: {dominant_emotion}, {second_dominant_emotion}')
        #     pass

