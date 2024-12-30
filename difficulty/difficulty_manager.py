from config.logger import get_game_logger
from difficulty.difficulty.difficulty_level import Difficulty
import difficulty.difficulty.difficulty_levels as dl

logger = get_game_logger()


class DifficultyManager:
    def __init__(self):

        #before stats
        # self.player_settings = {
        #     1: {"speed": 200, "jump_height": 0.5, "gravity": -1, "velocity_x": 30, "prev_speed": 200, bouncing_dist: 2},
        #     2: {"speed": 275, "jump_height": 0.55, "gravity": -1.7, "velocity_x": 35, "prev_speed": 275, bouncing_dist: 3},
        #     3: {"speed": 350, "jump_height": 0.7, "gravity": -2.3, "velocity_x": 40, "prev_speed": 350, bouncing_dist: 4}
        # }
        
        self.player_settings = {
            1: {"speed": 195, "jump_height": 0.65, "gravity": -1.5, "velocity_x": 30, "prev_speed": 195,
                "bouncing_dist": 2},
            2: {"speed": 210, "jump_height": 0.65, "gravity": -1.5, "velocity_x": 30, "prev_speed": 210,
                "bouncing_dist": 3},
            3: {"speed": 225, "jump_height": 0.65, "gravity": -1.5, "velocity_x": 30, "prev_speed": 225,
                "bouncing_dist": 4},
            4: {"speed": 240, "jump_height": 0.65, "gravity": -1.5, "velocity_x": 30, "prev_speed": 240,
                "bouncing_dist": 3},
            5: {"speed": 260, "jump_height": 0.65, "gravity": -1.5, "velocity_x": 30, "prev_speed": 260,
                "bouncing_dist": 3},
            6: {"speed": 275, "jump_height": 0.65, "gravity": -1.5, "velocity_x": 30, "prev_speed": 275,
                "bouncing_dist": 3},
            7: {"speed": 300, "jump_height": 0.65, "gravity": -1.5, "velocity_x": 30, "prev_speed": 300,
                "bouncing_dist": 3},
            8: {"speed": 325, "jump_height": 0.65, "gravity": -1.5, "velocity_x": 30, "prev_speed": 325,
                "bouncing_dist": 3.5},
            9: {"speed": 350, "jump_height": 0.65, "gravity": -1.5, "velocity_x": 30, "prev_speed": 350,
                "bouncing_dist": 4},
            10: {"speed": 375, "jump_height": 0.65, "gravity": -1.5, "velocity_x": 30, "prev_speed": 375,
                 "bouncing_dist": 5},
            11: {"speed": 400, "jump_height": 0.65, "gravity": -1.5, "velocity_x": 30, "prev_speed": 400,
                    "bouncing_dist": 5},
        }

        self.difficulties = {
            1: dl.DifficultyEasyHiddenMinus2(),
            2: dl.DifficultyEasyHiddenMinus1(),
            3: dl.DifficultyEasy(),
            4: dl.DifficultyEasyMedium1(),
            5: dl.DifficultyEasyMedium2(),
            6: dl.DifficultyMedium(),
            7: dl.DifficultyMediumHard1(),
            8: dl.DifficultyMediumHard2(),
            9: dl.DifficultyHard(),
            10: dl.DifficultyHardHiddenPlus1(),
            11: dl.DifficultyHardHiddenPlus2()
            }

    def get_player_settings(self, difficulty_level: int):
        return self.player_settings.get(difficulty_level)

    def set_player_settings(self, difficulty_level: int, player):
        settings = self.get_player_settings(difficulty_level)
        logger.info(f'Setting player settings to {settings}')
        for attribute, value in settings.items():
            setattr(player, attribute, value)

    def change_level_class(self, difficulty_level: int, prev_difficulty: Difficulty):
        difficulty_object = self.difficulties.get(difficulty_level)
        difficulty_object.switch(prev_difficulty.first_obstacle, prev_difficulty.last_obstacle_z)
        logger.info(f'Changing difficulty object to {difficulty_object}')
        return difficulty_object
