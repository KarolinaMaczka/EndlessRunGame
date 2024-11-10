from difficulty.difficulty.difficulty_levels import *

class DifficultyManager:
    def __init__(self):
        self.player_settings = {
            1: {"speed": 100, "jump_height": 0.55, "gravity": -1, "velocity_x": 30, "prev_speed": 100, "bouncing_dist": 1},
            2: {"speed": 150, "jump_height": 0.55, "gravity": -1, "velocity_x": 30, "prev_speed": 150, "bouncing_dist": 2},
            3: {"speed": 150, "jump_height": 0.55, "gravity": -1, "velocity_x": 30, "prev_speed": 150, "bouncing_dist": 3},
            4: {"speed": 200, "jump_height": 0.55, "gravity": -1, "velocity_x": 30, "prev_speed": 200, "bouncing_dist": 3},
            5: {"speed": 200, "jump_height": 0.55, "gravity": -1, "velocity_x": 30, "prev_speed": 200, "bouncing_dist": 3},
            6: {"speed": 200, "jump_height": 0.55, "gravity": -1, "velocity_x": 30, "prev_speed": 200, "bouncing_dist": 3},
            7: {"speed": 250, "jump_height": 0.55, "gravity": -1, "velocity_x": 30, "prev_speed": 250, "bouncing_dist": 3},
            8: {"speed": 200, "jump_height": 0.55, "gravity": -1, "velocity_x": 30, "prev_speed": 200, "bouncing_dist": 3.5},
            9: {"speed": 300, "jump_height": 0.7, "gravity": -2, "velocity_x": 30, "prev_speed": 300, "bouncing_dist": 4},
            10: {"speed": 400, "jump_height": 1, "gravity": -3, "velocity_x": 30, "prev_speed": 400, "bouncing_dist": 5},
        }
        self.difficulties = {
            1: Difficulty1(),
            2: Difficulty2(),
            3: Difficulty3(),
            4: Difficulty4(),
            5: Difficulty5(),
            6: Difficulty6(),
            7: Difficulty7(),
            8: Difficulty8(),
            9: Difficulty9(),
            10: Difficulty10()
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
