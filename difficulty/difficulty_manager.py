from difficulty.difficulty.difficulty_level import Difficulty
from difficulty.difficulty.impl.difficulty_level1 import Difficulty1
from difficulty.difficulty.impl.difficulty_level2 import Difficulty2
from camera_reading.read_camera import EmotionHolder

class DifficultyManager:
    def __init__(self, emotion_holder: EmotionHolder):
        self.player_settings = {
            1: {"speed": 100, "jump_height": 0.3, "gravity": 10},
            2: {"speed": 200, "jump_height": 0.5, "gravity": 7},
        }
        self.difficulties = {
            1: Difficulty1(),
            2: Difficulty2()
        }

    def get_player_settings(self, difficulty_level: int):
        return self.player_settings.get(difficulty_level)

    def set_player_settings(self, difficulty_level: int, player):
        settings = self.get_player_settings(difficulty_level)
        for attribute, value in settings.items():
            setattr(player, attribute, value)

    def change_level_class(self, difficulty_level: int, prev_difficulty: Difficulty):
        difficulty_object = self.difficulties.get(difficulty_level)
        difficulty_object.switch(prev_difficulty.first_obstacle, prev_difficulty.last_obstacle_z)
        return difficulty_object
        # if difficulty_level == 1:
        #     return Difficulty1(prev_difficulty.first_obstacle, prev_difficulty.last_obstacle_z)
        # elif difficulty_level == 2:
        #     return Difficulty2(prev_difficulty.first_obstacle, prev_difficulty.last_obstacle_z)