import unittest
from unittest.mock import MagicMock, patch
from collections import deque
from entities.obstacles.impl.board_obstacle import ObstacleBoard
from entities.obstacles.impl.long_cube import ObstacleLongCube
from entities.obstacles.impl.horizontal_pole_obstacle import ObstaclePoleGate
from entities.obstacles.obstacle_pool import ObstaclePool
from entities.obstacles.obstacle import Obstacle

class ObstaclePoolTest(unittest.TestCase):

    def setUp(self):
        self.models = MagicMock()
        self.obstacle_types = [ObstacleLongCube, ObstaclePoleGate, ObstacleBoard]
        self.pool = ObstaclePool(self.models, self.obstacle_types, max_size_per_type=2)

    @patch('entities.obstacles.impl.long_cube.Entity')
    def test_acquire_new_obstacle(self, MockEntity):
        MockEntity.return_value = MagicMock()
        metadata = {}
        position_z = 10
        lane = 2
        difficulty = 1
        obstacle = self.pool.acquire(ObstacleLongCube, position_z, difficulty, lane, metadata)

        self.assertIsInstance(obstacle, ObstacleLongCube)
        self.assertEqual(obstacle.position_z, position_z)
        self.assertEqual(obstacle.lane, lane)
        self.assertEqual(obstacle.difficulty, difficulty)

