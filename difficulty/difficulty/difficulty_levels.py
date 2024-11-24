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


class Difficulty1(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS,
                 **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        self.maps = [
            FirstObstacleMap(lane_change_const=0.2, small_obstacle_const=0.2, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_COLORFULL),
            FirstObstacleMap(lane_change_const=0.1, small_obstacle_const=0.3, gate_generation_const=0.3,
                             color_theme=ColorTheme.COLOR_THEME_BASIC),
            SecondObstacleMap(lane_change_const=0.2, small_obstacle_const=0.3, gate_generation_const=0.1,
                              color_theme=ColorTheme.COLOR_THEME_COLORFULL),
            SecondObstacleMap(lane_change_const=0.2, small_obstacle_const=0.3, gate_generation_const=0.1),
            ThirdObstacleMap(lane_change_const=0.2, small_obstacle_const=0.4, gate_generation_const=0.3)
        ]


class Difficulty2(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS,
                 **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        self.maps = [
            FirstObstacleMap(lane_change_const=0.4, small_obstacle_const=0.5, gate_generation_const=0.2),
            FirstObstacleMap(lane_change_const=0.4, small_obstacle_const=0.5, gate_generation_const=0.2,
                             color_theme=ColorTheme.COLOR_THEME_BASIC),
            SecondObstacleMap(lane_change_const=0.4, small_obstacle_const=0.4, gate_generation_const=0.2),
            ThirdObstacleMap(lane_change_const=0.5, small_obstacle_const=0.7, gate_generation_const=0.1),
            FourthObstacleMap(lane_change_const=0.4, small_obstacle_const=0.5, gate_generation_const=0.2),
            FifthObstacleMap(small_obstacle_const=0.5, gate_generation_const=0.1),
            SixthObstacleMap(small_obstacle_const=0.5, gate_generation_const=0.2)
        ]


class Difficulty3(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS,
                 **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        self.maps = [
            FirstObstacleMap(lane_change_const=0.6, small_obstacle_const=0.7, gate_generation_const=0.1,
                             color_theme=ColorTheme.COLOR_THEME_BASIC),
            FirstObstacleMap(lane_change_const=0.6, small_obstacle_const=0.7, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_COLORFULL),
            SecondObstacleMap(lane_change_const=0.6, small_obstacle_const=0.7, gate_generation_const=0.1,
                              color_theme=ColorTheme.COLOR_THEME_BASIC),
            SecondObstacleMap(lane_change_const=0.6, small_obstacle_const=0.7, gate_generation_const=0.1,
                              color_theme=ColorTheme.COLOR_THEME_BASIC),
            ThirdObstacleMap(lane_change_const=0.6, small_obstacle_const=0.7, gate_generation_const=0.1,
                             color_theme=ColorTheme.COLOR_THEME_BASIC),
            FourthObstacleMap(lane_change_const=0.6, small_obstacle_const=0.7, gate_generation_const=0.1,
                              color_theme=ColorTheme.COLOR_THEME_BASIC),
            FifthObstacleMap(small_obstacle_const=0.7, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_COLORFULL, lane_change_const=0.6),
        ]


class Difficulty4(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS,
                 **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        self.maps = [
            FirstObstacleMap(lane_change_const=0.6, small_obstacle_const=0.7, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_BASIC),
            FirstObstacleMap(lane_change_const=0.6, small_obstacle_const=0.7, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_GREEN),
            SecondObstacleMap(lane_change_const=0.6, small_obstacle_const=0.7, gate_generation_const=0.1,
                              color_theme=ColorTheme.COLOR_THEME_DARK),
            SecondObstacleMap(lane_change_const=0.6, small_obstacle_const=0.7, gate_generation_const=0.05,
                              color_theme=ColorTheme.COLOR_THEME_BASIC),
            ThirdObstacleMap(lane_change_const=0.6, small_obstacle_const=0.7, gate_generation_const=0.1,
                             color_theme=ColorTheme.COLOR_THEME_DARK),
            FourthObstacleMap(lane_change_const=0.6, small_obstacle_const=0.7, gate_generation_const=0.1,
                              color_theme=ColorTheme.COLOR_THEME_BASIC),
            FifthObstacleMap(small_obstacle_const=0.7, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_GREEN, lane_change_const=0.6),
            SixthObstacleMap(small_obstacle_const=0.5, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_DARK)
        ]


class Difficulty5(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS,
                 **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        self.maps = [
            FirstObstacleMap(lane_change_const=0.7, small_obstacle_const=0.7, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_DARK),
            FirstObstacleMap(lane_change_const=0.7, small_obstacle_const=0.7, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_GREEN),
            SecondObstacleMap(lane_change_const=0.7, small_obstacle_const=0.7, gate_generation_const=0.1,
                              color_theme=ColorTheme.COLOR_THEME_DARK),
            SecondObstacleMap(lane_change_const=0.7, small_obstacle_const=0.7, gate_generation_const=0.05,
                              color_theme=ColorTheme.COLOR_THEME_GREEN),
            ThirdObstacleMap(lane_change_const=0.7, small_obstacle_const=0.7, gate_generation_const=0.1,
                             color_theme=ColorTheme.COLOR_THEME_DARK, change_obstacle_type_cons=0.7),
            FourthObstacleMap(lane_change_const=0.7, small_obstacle_const=0.7, gate_generation_const=0.1,
                              color_theme=ColorTheme.COLOR_THEME_GREEN, change_obstacle_type_cons=0.7),
            FifthObstacleMap(small_obstacle_const=0.7, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_GREEN, lane_change_const=0.7),
            SixthObstacleMap(small_obstacle_const=0.6, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_DARK)

        ]


class Difficulty6(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS,
                 **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        self.maps = [
            FirstObstacleMap(lane_change_const=0.7, small_obstacle_const=0.7, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_DARK),
            FirstObstacleMap(lane_change_const=0.7, small_obstacle_const=0.7, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_GREEN),
            SecondObstacleMap(lane_change_const=0.7, small_obstacle_const=0.7, gate_generation_const=0.1,
                              color_theme=ColorTheme.COLOR_THEME_DARK),
            SecondObstacleMap(lane_change_const=0.7, small_obstacle_const=0.7, gate_generation_const=0.05,
                              color_theme=ColorTheme.COLOR_THEME_GREEN),
            ThirdObstacleMap(lane_change_const=0.7, small_obstacle_const=0.7, gate_generation_const=0.1,
                             color_theme=ColorTheme.COLOR_THEME_DARK, change_obstacle_type_cons=0.7),
            FourthObstacleMap(lane_change_const=0.7, small_obstacle_const=0.7, gate_generation_const=0.1,
                              color_theme=ColorTheme.COLOR_THEME_GREEN, change_obstacle_type_cons=0.7),
        ]


class Difficulty7(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS,
                 **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        self.maps = [
            FirstObstacleMap(lane_change_const=0.7, small_obstacle_const=0.8, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_DARK),
            FirstObstacleMap(lane_change_const=0.7, small_obstacle_const=0.8, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_GREEN),
            SecondObstacleMap(lane_change_const=0.7, small_obstacle_const=0.8, gate_generation_const=0.1,
                              color_theme=ColorTheme.COLOR_THEME_DARK),
            ThirdObstacleMap(lane_change_const=0.7, small_obstacle_const=0.8, gate_generation_const=0.1,
                             color_theme=ColorTheme.COLOR_THEME_DARK, change_obstacle_type_cons=1),
            FourthObstacleMap(lane_change_const=0.7, small_obstacle_const=0.8, gate_generation_const=0.1,
                              color_theme=ColorTheme.COLOR_THEME_GREEN, change_obstacle_type_cons=1),
            FifthObstacleMap(small_obstacle_const=0.8, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_GREEN, lane_change_const=0.7)
        ]


class Difficulty8(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS,
                 **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        self.maps = [FifthObstacleMap(small_obstacle_const=1, gate_generation_const=0.1,
                                      color_theme=ColorTheme.COLOR_THEME_GREEN, lane_change_const=0.9),
                     SixthObstacleMap(small_obstacle_const=1, gate_generation_const=0.1,
                                      color_theme=ColorTheme.COLOR_THEME_DARK)]


class Difficulty9(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS,
                 **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        self.maps = [
            FirstObstacleMap(lane_change_const=0.9, small_obstacle_const=0.8, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_DARK),
            FirstObstacleMap(lane_change_const=0.9, small_obstacle_const=0.9, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_GREEN),
            ThirdObstacleMap(lane_change_const=0.9, small_obstacle_const=0.9, gate_generation_const=0.1, color_theme=ColorTheme.COLOR_THEME_DARK, change_obstacle_type_cons=1),
            FourthObstacleMap(lane_change_const=0.9, small_obstacle_const=0.9, gate_generation_const=0.1,color_theme=ColorTheme.COLOR_THEME_GREEN, change_obstacle_type_cons=1),
            FifthObstacleMap(small_obstacle_const=0.9, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_GREEN, lane_change_const=0.9)
        ]


class Difficulty10(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS,
                 **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        self.maps = [FifthObstacleMap(small_obstacle_const=1, gate_generation_const=0.02, color_theme=ColorTheme.COLOR_THEME_GREEN, lane_change_const=0.9),
            SixthObstacleMap(small_obstacle_const=1, gate_generation_const=0.02, color_theme=ColorTheme.COLOR_THEME_DARK)
        ]

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

class DifficultyTestOneMap(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        self.maps = [
            SixthObstacleMap(lane_change_const=0.5, small_obstacle_const=0.75, gate_generation_const=0.05,
                             color_theme=ColorTheme.COLOR_THEME_COLORFULL, obstacle_generation_distance=150),
        ]