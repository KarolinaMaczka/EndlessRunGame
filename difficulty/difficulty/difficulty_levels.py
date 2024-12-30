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
from entities.obstacles.impl.board_obstacle import ObstacleBoard
from entities.obstacles.impl.cube_obstacle import ObstacleCube
from entities.obstacles.impl.fence_obstacle import ObstacleFence
from entities.obstacles.impl.horizontal_pole_obstacle import ObstaclePoleGate
from entities.obstacles.impl.long_cube import ObstacleLongCube
from entities.obstacles.impl.train_obstacle import ObstacleTrain
from entities.obstacles.obstacle_metadata_factory import ObstacleMetadataFactory


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
            ThirdObstacleMap(lane_change_const=0.85, small_obstacle_const=0.8, gate_generation_const=0.05, obstacle_generation_distance=250),
            FifthObstacleMap(lane_change_const=0.8, small_obstacle_const=0.8, gate_generation_const=0.05, obstacle_generation_distance=250),
        ]

class DifficultyEasyHiddenMinus1(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        self.maps = [
            SecondObstacleMap(lane_change_const=0.6, small_obstacle_const=0.5, big_obstacle_const=0.8, gate_generation_const=0.1, obstacle_generation_distance=250, color_theme=ColorTheme.COLOR_THEME_COLORFULL),
            ThirdObstacleMap(lane_change_const=0.85, small_obstacle_const=0.9, gate_generation_const=0.05, obstacle_generation_distance=250),
            FifthObstacleMap(lane_change_const=0.8, small_obstacle_const=0.9, gate_generation_const=0.05, obstacle_generation_distance=250),
        ]

class DifficultyEasy(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        self.maps = [      
            FirstObstacleMap(lane_change_const=0.7, small_obstacle_const=0.6, big_obstacle_const=0.6, gate_generation_const=0.05, obstacle_generation_distance=250, color_theme=ColorTheme.COLOR_THEME_COLORFULL),
            SecondObstacleMap(lane_change_const=0.7, small_obstacle_const=0.7, big_obstacle_const=0.7, gate_generation_const=0.1, obstacle_generation_distance=250, color_theme=ColorTheme.COLOR_THEME_COLORFULL),
            ThirdObstacleMap(lane_change_const=0.95, small_obstacle_const=1, gate_generation_const=0.05, obstacle_generation_distance=250),
            FifthObstacleMap(lane_change_const=0.9, small_obstacle_const=1, gate_generation_const=0.05, obstacle_generation_distance=250),
        ]

class DifficultyEasyMedium1(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        self.maps = [
            FirstObstacleMap(lane_change_const=0.7, small_obstacle_const=0.7, big_obstacle_const=0.6, gate_generation_const=0.05, obstacle_generation_distance=250, color_theme=ColorTheme.COLOR_THEME_COLORFULL),
            SecondObstacleMap(lane_change_const=0.7, small_obstacle_const=0.7, big_obstacle_const=0.7, gate_generation_const=0.1, obstacle_generation_distance=250, color_theme=ColorTheme.COLOR_THEME_COLORFULL),
            FourthObstacleMap(lane_change_const=0.95, small_obstacle_const=0.9, gate_generation_const=0.05, obstacle_generation_distance=250),
            FifthObstacleMap(lane_change_const=0.9, small_obstacle_const=1, gate_generation_const=0.05, obstacle_generation_distance=250),        
        ]

class DifficultyEasyMedium2(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        self.maps = [
            FirstObstacleMap(lane_change_const=0.8, small_obstacle_const=0.8, big_obstacle_const=0.5, gate_generation_const=0.05, obstacle_generation_distance=250, color_theme=ColorTheme.COLOR_THEME_COLORFULL),
            FourthObstacleMap(lane_change_const=0.95, small_obstacle_const=0.9, gate_generation_const=0.05, obstacle_generation_distance=250),
            FifthObstacleMap(lane_change_const=0.9, small_obstacle_const=1, gate_generation_const=0.05, obstacle_generation_distance=250),        
        ]

class DifficultyMedium(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        self.maps = [
            FirstObstacleMap(lane_change_const=0.8, small_obstacle_const=0.8, big_obstacle_const=0.5, gate_generation_const=0.05, obstacle_generation_distance=200, color_theme=ColorTheme.COLOR_THEME_COLORFULL),
            FourthObstacleMap(lane_change_const=0.95, small_obstacle_const=0.9, gate_generation_const=0.05, obstacle_generation_distance=200),
            SixthObstacleMap(lane_change_const=0.5, small_obstacle_const=0.9, gate_generation_const=0.05, obstacle_generation_distance=200, color_theme=ColorTheme.COLOR_THEME_COLORFULL),
            ]

class DifficultyMediumHard1(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        self.maps = [
            SeventhObstacleMap(small_obstacle_const=0.5, gate_generation_const=0.1, lane_change_const=0.3, obstacle_generation_distance=250),
        ]

class DifficultyMediumHard2(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        self.maps = [
            FirstObstacleMap(lane_change_const=0.3, small_obstacle_const=0.3, gate_generation_const=0.05, obstacle_generation_distance=250, color_theme=ColorTheme.COLOR_THEME_COLORFULL),
        ]

class DifficultyHard(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        big_obstacles = ObstacleMetadataFactory([
            {"obstacle": ObstacleLongCube, 'difficulty': 1, 'probability': 0.2, "has_ladder": 0.2},
            {"obstacle": ObstacleTrain, 'difficulty': 1, 'probability': 0.8}],
            4)
        small_obstacles = ObstacleMetadataFactory([
            {"obstacle": ObstacleFence, 'difficulty': 1, 'probability': 0.4},
            {"obstacle": ObstacleBoard, 'difficulty': 1, 'probability': 0.2},
            {"obstacle": ObstacleCube, 'difficulty': 1, 'probability': 0.3},
            {"obstacle": ObstaclePoleGate, 'difficulty': 1, 'probability': 0.1}],
            4)
        small_obstacles_difficult = ObstacleMetadataFactory([
            {"obstacle": ObstacleFence, 'difficulty': 1, 'probability': 0.4},
            {"obstacle": ObstacleBoard, 'difficulty': 1, 'probability': 0.3},
            {"obstacle": ObstacleCube, 'difficulty': 1, 'probability': 0.2},
            {"obstacle": ObstaclePoleGate, 'difficulty': 1, 'probability': 0.1}],
            4)

        map7 = SeventhObstacleMap(lane_change_const=0.75, small_obstacle_const=1, gate_generation_const=0.05,
                                  obstacle_generation_distance=400, color_theme=ColorTheme.COLOR_THEME_DARK)
        map7.set_big_obstacles(big_obstacles)
        map7.set_small_obstacles(small_obstacles)

        map1 = FirstObstacleMap(lane_change_const=0.75, small_obstacle_const=1, gate_generation_const=0.05,
                                obstacle_generation_distance=400, color_theme=ColorTheme.COLOR_THEME_GREEN)
        map1.set_big_obstacles(big_obstacles)
        map1.set_small_obstacles(small_obstacles)

        map2 = SecondObstacleMap(lane_change_const=0.75, small_obstacle_const=1, gate_generation_const=0.05,
                                obstacle_generation_distance=400, color_theme=ColorTheme.COLOR_THEME_GREEN)
        map2.set_big_obstacles(big_obstacles)
        map2.set_small_obstacles(small_obstacles)

        map6 = SixthObstacleMap(lane_change_const=1, small_obstacle_const=1, gate_generation_const=0,
                                obstacle_generation_distance=300, color_theme=ColorTheme.COLOR_THEME_GREEN)
        map6.set_big_obstacles(big_obstacles)
        map6.set_small_obstacles(small_obstacles_difficult)

        self.maps = [
            map1,
            map2,
            map6,
            map7
        ]

class DifficultyHardHiddenPlus1(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        big_obstacles = ObstacleMetadataFactory([
            {"obstacle": ObstacleLongCube, 'difficulty': 1, 'probability': 0.2, "has_ladder": 0.2},
            {"obstacle": ObstacleTrain, 'difficulty': 1, 'probability': 0.8}],
            4)
        small_obstacles = ObstacleMetadataFactory([
            {"obstacle": ObstacleFence, 'difficulty': 1, 'probability': 0.4},
            {"obstacle": ObstacleBoard, 'difficulty': 1, 'probability': 0.2},
            {"obstacle": ObstacleCube, 'difficulty': 1, 'probability': 0.3},
            {"obstacle": ObstaclePoleGate, 'difficulty': 1, 'probability': 0.1}],
            4)
        small_obstacles_difficult = ObstacleMetadataFactory([
            {"obstacle": ObstacleFence, 'difficulty': 1, 'probability': 0.4},
            {"obstacle": ObstacleBoard, 'difficulty': 1, 'probability': 0.5},
            {"obstacle": ObstacleCube, 'difficulty': 1, 'probability': 0.05},
            {"obstacle": ObstaclePoleGate, 'difficulty': 1, 'probability': 0.05}],
            4)

        map7 = SeventhObstacleMap(lane_change_const=0.75, small_obstacle_const=1, gate_generation_const=0.05,
                                  obstacle_generation_distance=400, color_theme=ColorTheme.COLOR_THEME_DARK)
        map7.set_big_obstacles(big_obstacles)
        map7.set_small_obstacles(small_obstacles)

        map1 = FirstObstacleMap(lane_change_const=0.75, small_obstacle_const=1, gate_generation_const=0.05,
                                obstacle_generation_distance=400, color_theme=ColorTheme.COLOR_THEME_GREEN)
        map1.set_big_obstacles(big_obstacles)
        map1.set_small_obstacles(small_obstacles)

        map6 = SixthObstacleMap(lane_change_const=1, small_obstacle_const=1, gate_generation_const=0,
                                obstacle_generation_distance=300, color_theme=ColorTheme.COLOR_THEME_GREEN)
        map6.set_big_obstacles(big_obstacles)
        map6.set_small_obstacles(small_obstacles_difficult)

        self.maps = [
            map1,
            map6,
            map7
        ]

class DifficultyHardHiddenPlus2(Difficulty):
    def __init__(self, first_obstacle=INITIAL_FIRST_OBSTACLE_Z_POS, last_obstacle_z=INITIAL_LAST_OBSTACLE_Z_POS, **kwargs):
        super().__init__(first_obstacle, last_obstacle_z, **kwargs)
        big_obstacles = ObstacleMetadataFactory([
            {"obstacle": ObstacleLongCube, 'difficulty': 1, 'probability': 0.2, "has_ladder": 0.1},
            {"obstacle": ObstacleTrain, 'difficulty': 1, 'probability': 0.8}],
            4)
        small_obstacles = ObstacleMetadataFactory([
            {"obstacle": ObstacleFence, 'difficulty': 1, 'probability': 0.4},
            {"obstacle": ObstacleBoard, 'difficulty': 1, 'probability': 0.2},
            {"obstacle": ObstacleCube, 'difficulty': 1, 'probability': 0.3},
            {"obstacle": ObstaclePoleGate, 'difficulty': 1, 'probability': 0.1}],
            4)
        small_obstacles_difficult = ObstacleMetadataFactory([
            {"obstacle": ObstacleFence, 'difficulty': 1, 'probability': 0.4},
            {"obstacle": ObstacleBoard, 'difficulty': 1, 'probability': 0.5},
            {"obstacle": ObstacleCube, 'difficulty': 1, 'probability': 0.05},
            {"obstacle": ObstaclePoleGate, 'difficulty': 1, 'probability': 0.05}],
            4)

        map7 = SeventhObstacleMap(lane_change_const=0.75, small_obstacle_const=1, gate_generation_const=0.05,
                                  obstacle_generation_distance=400, color_theme=ColorTheme.COLOR_THEME_DARK)
        map7.set_big_obstacles(big_obstacles)
        map7.set_small_obstacles(small_obstacles)

        map1 = FirstObstacleMap(lane_change_const=0.75, small_obstacle_const=1, gate_generation_const=0.05,
                                obstacle_generation_distance=400, color_theme=ColorTheme.COLOR_THEME_GREEN)
        map1.set_big_obstacles(big_obstacles)
        map1.set_small_obstacles(small_obstacles)

        map6 = SixthObstacleMap(lane_change_const=1, small_obstacle_const=1, gate_generation_const=0,
                                obstacle_generation_distance=300, color_theme=ColorTheme.COLOR_THEME_GREEN)
        map6.set_big_obstacles(big_obstacles)
        map6.set_small_obstacles(small_obstacles_difficult)

        self.maps = [
            map1,
            map6,
            map7,
            map6,
            map7
        ]
