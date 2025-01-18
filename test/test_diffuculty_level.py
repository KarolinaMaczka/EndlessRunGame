import unittest
from unittest.mock import patch
from difficulty.difficulty.difficulty_level import Difficulty
from difficulty.difficulty.difficulty_levels import DifficultyEasyHiddenMinus1
from difficulty.maps.map import ObstacleMap, MapMetadata
from config.constants import INITIAL_FIRST_OBSTACLE_Z_POS, INITIAL_LAST_OBSTACLE_Z_POS

class TestDifficulty(unittest.TestCase):
    def setUp(self):
        self.difficulty = DifficultyEasyHiddenMinus1()

    def test_switch(self):
        self.difficulty.switch(1000, 2000)

        self.assertEqual(self.difficulty.first_obstacle, 1000)
        self.assertEqual(self.difficulty.last_obstacle_z, 2000)

    def test_generate_obstacle(self):
        self.difficulty.first_obstacle = 500
        self.difficulty.last_obstacle_z = 1000
        obstacles, metadata = self.difficulty.generate_obstacle(700)

        self.assertGreater(len(obstacles), 0)
        self.assertIsInstance(metadata, MapMetadata)

    def not_test_generate_obstacle(self):
        self.difficulty.first_obstacle = 500
        obstacles, metadata = self.difficulty.generate_obstacle(400)

        self.assertEqual(len(obstacles), 0)
        self.assertIsNone(metadata)

    def test_initialize_obstacles(self):
        obstacles, metadata = self.difficulty.initialize_obstacles()

        self.assertGreater(len(obstacles), 0)
        self.assertIsInstance(metadata, MapMetadata)
