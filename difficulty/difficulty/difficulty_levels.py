from config.constants import INITIAL_FIRST_OBSTACLE_Z_POS, INITIAL_LAST_OBSTACLE_Z_POS
from difficulty.difficulty.difficulty_level import Difficulty
from difficulty.maps.color_themes import ColorTheme
from difficulty.maps.impl.map1 import FirstObstacleMap
from difficulty.maps.impl.map2 import SecondObstacleMap
from difficulty.maps.impl.map3 import ThirdObstacleMap
from difficulty.maps.impl.map4 import FourthObstacleMap
from difficulty.maps.impl.map5 import FifthObstacleMap
from difficulty.maps.impl.map6 import SixthObstacleMap
from difficulty.maps.impl.map7 import SeventhObstacleMap

class DifficultyTest1(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        # Include all maps here to test
        self.maps = [
            FirstObstacleMap(lane_change_const=0.3, small_obstacle_const=0.3, gate_generation_const=0.05, obstacle_generation_distance=250,
                             color_theme=ColorTheme.COLOR_THEME_COLORFULL),
            SecondObstacleMap(lane_change_const=0.3, small_obstacle_const=0.3, gate_generation_const=0.1, obstacle_generation_distance=250,
                              color_theme=ColorTheme.COLOR_THEME_COLORFULL),
            ThirdObstacleMap(lane_change_const=0.3, small_obstacle_const=0.3, gate_generation_const=0.1, obstacle_generation_distance=250),
            FourthObstacleMap(lane_change_const=0.3, small_obstacle_const=0.3, gate_generation_const=0.2, obstacle_generation_distance=250),
            FifthObstacleMap(small_obstacle_const=0.6, gate_generation_const=0.1, lane_change_const=0.3, obstacle_generation_distance=250),
            SixthObstacleMap(small_obstacle_const=0.5, gate_generation_const=0.2, lane_change_const=0.3, obstacle_generation_distance=250),
            SeventhObstacleMap(small_obstacle_const=0.5, gate_generation_const=0.1, lane_change_const=0.3, obstacle_generation_distance=250)
        ]

class DifficultyTest2(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        # Include all maps here to test
        self.maps = [
            FirstObstacleMap(lane_change_const=0.5, small_obstacle_const=0.5, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_COLORFULL, obstacle_generation_distance=200),
            SecondObstacleMap(lane_change_const=0.5, small_obstacle_const=0.5, gate_generation_const=0.1,
                              color_theme=ColorTheme.COLOR_THEME_COLORFULL, obstacle_generation_distance=200),
            ThirdObstacleMap(lane_change_const=0.5, small_obstacle_const=0.5, gate_generation_const=0.1, obstacle_generation_distance=200),
            FourthObstacleMap(lane_change_const=0.5, small_obstacle_const=0.5, gate_generation_const=0.05, obstacle_generation_distance=200),
            FifthObstacleMap(small_obstacle_const=0.7, gate_generation_const=0.1, lane_change_const=0.5, obstacle_generation_distance=200),
            SixthObstacleMap(small_obstacle_const=0.6, gate_generation_const=0.1, lane_change_const=0.5, obstacle_generation_distance=200),
            SeventhObstacleMap(small_obstacle_const=0.5, gate_generation_const=0.05, lane_change_const=0.5,
                               obstacle_generation_distance=250)
        ]

class DifficultyTest3(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        # Include all maps here to test
        self.maps = [
            FirstObstacleMap(lane_change_const=0.75, small_obstacle_const=0.7, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_COLORFULL, obstacle_generation_distance=150),
            SecondObstacleMap(lane_change_const=0.75, small_obstacle_const=0.7, gate_generation_const=0.1,
                              color_theme=ColorTheme.COLOR_THEME_COLORFULL, obstacle_generation_distance=150),
            ThirdObstacleMap(lane_change_const=0.75, small_obstacle_const=0.7, gate_generation_const=0.05, obstacle_generation_distance=150),
            FourthObstacleMap(lane_change_const=0.75, small_obstacle_const=0.7, gate_generation_const=0.05, obstacle_generation_distance=150),
            FifthObstacleMap(small_obstacle_const=0.9, gate_generation_const=0.1, lane_change_const=0.75, obstacle_generation_distance=150),
            SixthObstacleMap(small_obstacle_const=0.8, gate_generation_const=0.1, lane_change_const=0.75, obstacle_generation_distance=150),
            SeventhObstacleMap(small_obstacle_const=0.7, gate_generation_const=0.05, lane_change_const=0.75,
                               obstacle_generation_distance=300)
        ]


# Stworzyć poziomy wg schematu: łatwy_ukryty(-2), łatwy_ukryty(-1), łatwy, łatwo-średni(1), łatwo-średni(2), średni, średnio-trudny(1), średnio-trudny(2), trudny, trudny_ukryty(+1), trudny_ukryty(+2)

class DifficultyEasyHiddenMinus2(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        self.maps = [
            FirstObstacleMap(lane_change_const=0.3, small_obstacle_const=0.3, gate_generation_const=0.05, obstacle_generation_distance=250, color_theme=ColorTheme.COLOR_THEME_COLORFULL),
        ]

class DifficultyEasyHiddenMinus1(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        self.maps = [
            SecondObstacleMap(lane_change_const=0.3, small_obstacle_const=0.3, gate_generation_const=0.1, obstacle_generation_distance=250, color_theme=ColorTheme.COLOR_THEME_COLORFULL),
        ]

class DifficultyEasy(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        self.maps = [
            ThirdObstacleMap(lane_change_const=0.3, small_obstacle_const=0.3, gate_generation_const=0.1, obstacle_generation_distance=250),
        ]

class DifficultyEasyMedium1(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        self.maps = [
            FourthObstacleMap(lane_change_const=0.3, small_obstacle_const=0.3, gate_generation_const=0.2, obstacle_generation_distance=250),
        ]

class DifficultyEasyMedium2(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        self.maps = [
            FifthObstacleMap(small_obstacle_const=0.6, gate_generation_const=0.1, lane_change_const=0.3, obstacle_generation_distance=250),
        ]

class DifficultyMedium(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        self.maps = [
            SixthObstacleMap(small_obstacle_const=0.5, gate_generation_const=0.2, lane_change_const=0.3, obstacle_generation_distance=250),
        ]

class DifficultyMediumHard1(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        self.maps = [
            SeventhObstacleMap(small_obstacle_const=0.5, gate_generation_const=0.1, lane_change_const=0.3, obstacle_generation_distance=250),
        ]

class DifficultyMediumHard2(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        self.maps = [
            FirstObstacleMap(lane_change_const=0.3, small_obstacle_const=0.3, gate_generation_const=0.05, obstacle_generation_distance=250, color_theme=ColorTheme.COLOR_THEME_COLORFULL),
        ]

class DifficultyHard(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        self.maps = [
            SecondObstacleMap(lane_change_const=0.3, small_obstacle_const=0.3, gate_generation_const=0.1, obstacle_generation_distance=250, color_theme=ColorTheme.COLOR_THEME_COLORFULL),
        ]

class DifficultyHardHiddenPlus1(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        self.maps = [
            ThirdObstacleMap(lane_change_const=0.3, small_obstacle_const=0.3, gate_generation_const=0.1, obstacle_generation_distance=250),
        ]

class DifficultyHardHiddenPlus2(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        self.maps = [
            FourthObstacleMap(lane_change_const=0.3, small_obstacle_const=0.3, gate_generation_const=0.2, obstacle_generation_distance=250),
        ]