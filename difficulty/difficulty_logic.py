from multiprocessing import Queue

from data_manager import DataManager
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
        'neutral': 0,
        'none': 0
    }

    def __init__(self, data_manager: DataManager, context):
        self.counter = 0
        self.context = context
        self.data_manager = data_manager
        # self.change_difficulty = bool(random.randint(0, 1))
        self.change_difficulty = True
        logger.info('Modification type: ' + str(self.change_difficulty))
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
            emotions = emotion_queue.get() # emotions = (('happy', 90), ('neutral', 10.002), 1.0)
            # for emotion in emotions:
            if emotions[1][0] == 'sad' and emotions[1][1] < 10:
                second_emotion = 'sad_low'
            elif emotions[1][0] == 'sad' and emotions[1][1] >= 10:
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
        self.emotions_count_percentage = {k: v / sum(self.emotions_count.values()) for k, v in self.emotions_count.items()}
        logger.info(f'Emotions count: {self.emotions_count}')
        logger.info(f'Emotions count percentage: {self.emotions_count_percentage}')

        logger.info(f'Second emotions count one round: {self.second_emotions_count_one_round}')
        self.second_emotions_count = {k: v + self.second_emotions_count_one_round[k] for k, v in self.second_emotions_count.items()}
        self.second_emotions_count_percentage = {k: v / sum(self.second_emotions_count.values()) for k, v in self.second_emotions_count.items()}
        logger.info(f'Second emotions count: {self.second_emotions_count}')
        logger.info(f'Second emotions count percentage: {self.second_emotions_count_percentage}')


        # Instructions for changing difficulty based on emotions
        # ------------------------------------------------------
        # If there are any other emotions than neutral, apply the change for the one with the most appearances
        # If there is only neutral emotion, check second emotion
            # If there is anger or happy/fear, apply the change for the one with the most appearances
            # If there is only neutral and sad, check further
                # For sadness which has confidence less than 10 assume that it's focus (level up)
                # For sadness which has confidence more than 10 assume that it is sadness (level down)
                # apply the change for the one with the most appearances

        if self.emotions_count['neutral'] != 10:
            list_of_emotions = list(self.emotions_count_one_round.items())
            list_of_emotions = [emotion for emotion in list_of_emotions if emotion[0] != 'neutral']
            dominant_emotion = max(list_of_emotions, key=lambda x: x[1])[0]
            logger.info('Changing difficulty based on: ' + dominant_emotion + ' | change: ' + str(self.DIFFICULTY_CHANGE[dominant_emotion]))
            self.context.change_difficulty(self.DIFFICULTY_CHANGE[dominant_emotion])
        else:
            logger.info('Neutral emotion is prevailing, checking further')
            if self.second_emotions_count['angry'] + self.second_emotions_count['happy'] + self.second_emotions_count['fear'] + self.second_emotions_count['sad_high'] > 0:
                list_of_emotions = list(self.second_emotions_count_one_round.items())
                list_of_emotions = [emotion for emotion in list_of_emotions if emotion[0] in ['angry', 'happy', 'fear', 'sad_high']]
                dominant_emotion = max(list_of_emotions, key=lambda x: x[1])[0]
                logger.info('Changing difficulty based on: ' + dominant_emotion + ' | change: ' + str(self.DIFFICULTY_CHANGE[dominant_emotion]))
                self.context.change_difficulty(self.DIFFICULTY_CHANGE[dominant_emotion])
            else:
                if self.second_emotions_count['sad_low'] > 0:
                    dominant_emotion = 'sad_low'
                    if random.random() < 0.5:
                        logger.info('Changing difficulty based on: ' + dominant_emotion + ' | change: ' + str(self.DIFFICULTY_CHANGE[dominant_emotion]))
                        self.context.change_difficulty(self.DIFFICULTY_CHANGE[dominant_emotion])
                    else:
                        logger.info('No change in difficulty')
                else:
                    logger.info('No change in difficulty')
                    dominant_emotion = 'none' 
        
        # Reset emotions count for the next round
        self.emotions_count_one_round = self.create_emotion_count_dict() 
        self.second_emotions_count_one_round = self.create_emotion_count_dict()