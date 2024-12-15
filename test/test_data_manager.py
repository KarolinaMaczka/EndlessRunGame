import unittest
from unittest.mock import MagicMock
from config.constants import CollisionSide, CollisionType
from data_manager import DataManager

class TestDataManager(unittest.TestCase):

    def setUp(self):
        self.data_manager = DataManager()
        self.player = MagicMock()
        self.obstacle = MagicMock()
        self.obstacle.parentt = MagicMock()
        self.obstacle.parentt.__name__ = 'ObstacleWoodenSign'
        self.obstacle.parentt.position_z = 625.0
        self.obstacle.parentt.lane = 0

    def test_add_collision(self):
        self.obstacle.parentt.__class__.__name__ = 'ObstacleLongCube'
        self.data_manager.add_collision(CollisionSide.LEFT, CollisionType.LIGHT, self.obstacle, self.player)
        self.assertEqual(len(self.data_manager.hit_obstacles), 1)
        collision = self.data_manager.hit_obstacles[0]
        self.assertEqual(collision[0], 'ObstacleLongCube')
        self.assertEqual(collision[1], 'left')
        self.assertEqual(collision[2], 'light')
        self.assertEqual(collision[3], 625.0)
        self.assertEqual(collision[4], 0)

    def test_add_obstacle_data(self):
        self.obstacle.obstacle = MagicMock()
        self.obstacle.obstacle.__name__ = 'ObstacleWoodenSign'
        self.obstacle.position_z = 625.0
        self.obstacle.lane = 0
        self.data_manager.add_obstacle_data(self.obstacle)
        self.assertEqual(len(self.data_manager.obstacle_data), 1)
        obstacle_data = self.data_manager.obstacle_data[0]
        self.assertEqual(obstacle_data[0], 'ObstacleWoodenSign')
        self.assertEqual(obstacle_data[1], 625.0)
        self.assertEqual(obstacle_data[2], 0)


    def test_add_emotion(self):
        emotions = [["neutral", 81.52543640136719],["angry", 17.092456817626953],1.0,4.52154016494751]
        self.data_manager.add_emotion(emotions)
        self.assertEqual(len(self.data_manager.player_emotions),1)
        self.assertEqual(self.data_manager.player_emotions[0], emotions)

    def test_add_player_satisfaction(self):
        self.data_manager.add_player_satisfaction(-1)
        self.assertEqual(self.data_manager.player_satisfaction, -1)

    def test_add_playing_time(self):
        self.data_manager.add_playing_time(13.679054975509644)
        self.assertEqual(self.data_manager.playing_time, 13.679054975509644)

    def test_add_score(self):
        self.data_manager.add_score(2740)
        self.assertEqual(self.data_manager.score, 2740)

    def test_save_pressed_key(self):
        self.data_manager.save_pressed_key(('space', 674.846923828125))
        self.assertEqual(len(self.data_manager.keys_pressed), 1)
        self.assertEqual(self.data_manager.keys_pressed[0], ('space', 674.846923828125))


    def test_add_map_data(self):
        map_data = MagicMock()
        map_data.name = "SixthObstacleMap"
        map_data.lane_change_const = 0.3
        map_data.small_obstacle_const = 0.5
        map_data.gate_generation_const = 0.2
        map_data.color_theme = "COLOR_THEME_BASIC"
        map_data.first_obstacle = 500
        map_data.last_obstacle = 2750
        map_data.obstacle_generation_distance = 250
        self.data_manager.add_map_data(map_data)
        self.assertEqual(len(self.data_manager.map_data), 1)
        map_data_added = self.data_manager.map_data[0]
        self.assertEqual(map_data_added[0], "SixthObstacleMap")
        self.assertEqual(map_data_added[1], 0.3)
        self.assertEqual(map_data_added[2], 0.5)
        self.assertEqual(map_data_added[3], 0.2)
        self.assertEqual(map_data_added[4], "COLOR_THEME_BASIC")
        self.assertEqual(map_data_added[5], 500)
        self.assertEqual(map_data_added[6], 2750)
        self.assertEqual(map_data_added[7], 250)

    def test_clean_data(self):
        self.data_manager.clean_data()

        self.assertEqual(self.data_manager.obstacle_data, [])
        self.assertEqual(self.data_manager.hit_obstacles, [])
        self.assertEqual(self.data_manager.player_satisfaction, -1)
        self.assertEqual(self.data_manager.player_emotions, [])
        self.assertEqual(self.data_manager.map_data, [])
        self.assertEqual(self.data_manager.score, 0)
        self.assertEqual(self.data_manager.playing_time, 0)
        self.assertEqual(self.data_manager.difficulties, [])
        self.assertEqual(self.data_manager.keys_pressed, [])


