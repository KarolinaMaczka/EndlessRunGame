from multiprocessing import Queue

from data_manager import DataManager
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
        self.change_difficulty = str(np.random.choice(['emotions', 'random', 'no', 'faster']))
        # self.change_difficulty = 'faster'
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
        return dict.fromkeys(['happy', 'neutral', 'sad', 'angry', 'fear','surprise', 'disgust'], 0)

    def update(self, player_z: float, emotion_queue: Queue):
        # logger.info('Updating difficulty based on emotions')
        if not emotion_queue.empty():
            emotions = emotion_queue.get() # emotions = (('happy', 88.21), ('neutral', 10.002), 1.0)
            
            # Add raw emotions to data manager
            emotions_and_position = (*emotions, player_z)
            self.data_manager.add_emotion(emotions_and_position)
            # if we detect sad as main but there is fear or angry as second, we should consider fear or angry as main
            # (assummed after testing emotion detection)
            if emotions[0][0] == 'sad' and emotions[1][0] == 'fear' and emotions[1][1] > 25.0:
                logger.info(f'Changing main emotion from sad to fear {emotions[1][1]}')
                first_emotion = ('fear', emotions[1][1])
            elif emotions[0][0] == 'sad' and emotions[1][0] == 'angry' and emotions[1][1] > 25.0:
                logger.info(f'Changing main emotion from sad to angry {emotions[1][1]}')
                first_emotion = ('angry', emotions[1][1])
            else:
                first_emotion = emotions[0]
            
            emotions = (first_emotion, emotions[1], emotions[2])
            self.emotions_count_one_round[emotions[0][0]] += 1
            self.second_emotions_count_one_round[emotions[1][0]] += 1
            self.counter += 1
            if self.change_difficulty == 'emotions':
                if self.counter == 5:
                    self.update_difficulty()
                    self.counter = 0
            elif self.change_difficulty == 'random':  # change difficulty level at random every 5 rounds
                if self.counter == 5:
                    self.context.change_difficulty(random.choice([-1, 0, 0, 1]), allow_overheating=False)
                    self.counter = 0
            elif self.change_difficulty == 'faster':
                if self.counter == 5:
                    self.context.change_difficulty(1, allow_overheating=False)
                    self.counter = 0
        # time.sleep(0.1)

    def update_difficulty(self):
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

        if not self.context.overheating_state:
            # Instructions for changing difficulty based on emotions
            # ------------------------------------------------------
            # If at least one happy is prevailing, increase difficulty
            if self.emotions_count_one_round['happy'] > 0:
                change = int(np.random.choice([1, 2], p=[0.7, 0.3]))
                logger.info('Changing difficulty based on: happy | change: ' + str(change))
                self.context.change_difficulty(change)
            # If at least one angry or fear is prevailing, decrease difficulty
            elif self.emotions_count_one_round['angry'] > 0 or self.emotions_count_one_round['fear'] > 0:
                dominant_emotion = 'angry' if self.emotions_count_one_round['angry'] > 0 else 'fear'
                logger.info(f'Changing difficulty based on: {dominant_emotion} | change: -1')
                self.context.change_difficulty(-1)
            # If saddness has most appearances assume it is deep focus, try to preserve difficulty but can change with probability 0.4
            elif dominant_emotion := max(self.emotions_count_one_round, key=self.emotions_count_one_round.get) == 'sad':
                change = int(np.random.choice([0, 1], p=[0.6, 0.4]))
                logger.info(f'Changing difficulty based on: sad | change: {change}')
                self.context.change_difficulty(change)
            # Prevailing emotion is neutral, check further
            else:
                logger.info('Neutral emotion is prevailing, checking further')
                # 1-2 same as above but with second_emotion
                if self.second_emotions_count_one_round['angry'] + self.second_emotions_count_one_round['fear'] >= self.counter//2:
                    dominant_emotion = 'angry' if self.second_emotions_count_one_round['angry'] > self.second_emotions_count_one_round['fear'] else 'fear'
                    logger.info(f'Changing difficulty based on: {dominant_emotion} (second emotion) | change: -1')
                    self.context.change_difficulty(-1)
                elif self.second_emotions_count_one_round['happy'] > 0:
                    change = int(np.random.choice([1, 2], p=[0.7, 0.3]))
                    logger.info('Changing difficulty based on: happy (second emotion) | change: ' + str(change))
                    self.context.change_difficulty(change)
                # If sadness or neutral is dominant in second emotion count increase difficulty with probability 0.5
                elif self.second_emotions_count_one_round['sad'] > 0 or self.second_emotions_count_one_round['neutral'] > 0:
                    change = int(np.random.choice([0, 1], p=[0.5, 0.5]))
                    dominant_emotion = 'sad' if self.second_emotions_count_one_round['sad'] > 0 else 'neutral'
                    logger.info(f'Changing difficulty based on: {dominant_emotion} (second emotion) | change: {change}')
                    self.context.change_difficulty(change)
                # Otherwise no change in difficulty
                else:
                    logger.info('No change in difficulty')
        else:
            logger.info('Overheating state, lowering difficulty')
            self.context.change_difficulty(-2)

        # Reset emotions count for the next round
        self.emotions_count_one_round = self.create_emotion_count_dict() 
        self.second_emotions_count_one_round = self.create_emotion_count_dict()