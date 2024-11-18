from config.logger import get_game_logger
from difficulty.difficulty.difficulty_level import Difficulty
from difficulty.difficulty.difficulty_levels import Difficulty1, Difficulty2, Difficulty3, Difficulty4, Difficulty5, \
    Difficulty6, Difficulty7, Difficulty8, Difficulty9, Difficulty10, DifficultyTest1, DifficultyTest2, DifficultyTest3

logger = get_game_logger()
class DifficultyManager:
    def __init__(self):
        self.player_settings = {
            1: {"speed": 200, "jump_height": 0.50, "gravity": -1, "velocity_x": 30, "prev_speed": 100, "bouncing_dist": 1},
            2: {"speed": 275, "jump_height": 0.60, "gravity": -2, "velocity_x": 50, "prev_speed": 275, "bouncing_dist": 2},
            3: {"speed": 350, "jump_height": 0.65, "gravity": -3, "velocity_x": 70, "prev_speed": 350, "bouncing_dist": 3},
            4: {"speed": 200, "jump_height": 0.55, "gravity": -1, "velocity_x": 30, "prev_speed": 200, "bouncing_dist": 3},
            5: {"speed": 200, "jump_height": 0.55, "gravity": -1, "velocity_x": 30, "prev_speed": 200, "bouncing_dist": 3},
            6: {"speed": 200, "jump_height": 0.55, "gravity": -1, "velocity_x": 30, "prev_speed": 200, "bouncing_dist": 3},
            7: {"speed": 250, "jump_height": 0.55, "gravity": -1, "velocity_x": 30, "prev_speed": 250, "bouncing_dist": 3},
            8: {"speed": 200, "jump_height": 0.55, "gravity": -1, "velocity_x": 30, "prev_speed": 200, "bouncing_dist": 3.5},
            9: {"speed": 300, "jump_height": 0.7, "gravity": -2, "velocity_x": 30, "prev_speed": 300, "bouncing_dist": 4},
            10: {"speed": 400, "jump_height": 1, "gravity": -3, "velocity_x": 30, "prev_speed": 400, "bouncing_dist": 5},
        }
        self.difficulties = {
            1: DifficultyTest1(),
            2: DifficultyTest2(),
            3: DifficultyTest3(),
            4: Difficulty4(),
            5: Difficulty5(),
            6: Difficulty6(),
            7: Difficulty7(),
            8: Difficulty8(),
            9: Difficulty9(),
            10: Difficulty10(),
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
4