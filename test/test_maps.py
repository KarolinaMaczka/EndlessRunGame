import unittest
from unittest.mock import MagicMock, patch
from difficulty.maps.map import ObstacleMap, MapMetadata
from entities.obstacles.obstacle_metadata_factory import ObstacleMetadataFactory

class ObstacleMapImpl(ObstacleMap):
    def generate_obstacles(self, start, length):
        pass

class TestObstacleMap(unittest.TestCase):
    def setUp(self):
        self.obstacle_map = ObstacleMapImpl()
        self.obstacle_map._create_factories()

    @patch.object(ObstacleMetadataFactory, 'create_obstacle')
    def test_create_trains(self, mock_create_obstacle):
        start_x = 0
        z_position = 1000

        self.obstacle_map._create_trains(start_x, z_position)

        self.assertTrue(mock_create_obstacle.called)
        self.assertGreater(len(self.obstacle_map.obstacles), 0)

    @patch.object(ObstacleMetadataFactory, 'create_obstacle')
    def test_create_signs(self, mock_create_obstacle):
        z_position = 1000
        self.obstacle_map._create_signs(z_position)

        mock_create_obstacle.assert_called_once()
        self.assertGreater(len(self.obstacle_map.obstacles), 0)

    @patch.object(ObstacleMetadataFactory, 'create_obstacle')
    def test_generate_gate(self, mock_create_obstacle):
        z_position = 1000
        new_position = self.obstacle_map._generate_gate(z_position)

        mock_create_obstacle.assert_called_once()
        self.assertGreater(len(self.obstacle_map.obstacles), 0)
        self.assertEqual(new_position, 1000)

    @patch.object(ObstacleMetadataFactory, 'create_obstacle')
    def test_create_small_obstacles(self, mock_create_obstacle):
        start_x = 0
        z_position = 1000
        small_obstacle_const =0.7

        self.obstacle_map._create_small_obstacles(start_x, z_position, small_obstacle_const)

        self.assertTrue(mock_create_obstacle.called)
        self.assertGreater(len(self.obstacle_map.obstacles), 0)

    def test_adjust_last_position(self):
        last_obstacle_z = 1000
        adjusted_z = self.obstacle_map._adjust_last_position(last_obstacle_z)

        if self.obstacle_map.obstacle_generation_distance <= 150:
            self.assertEqual(adjusted_z, last_obstacle_z + self.obstacle_map.obstacle_generation_distance)
        else:
            self.assertEqual(adjusted_z, last_obstacle_z)

    def test_create_factories(self):
        self.obstacle_map._create_factories()

        self.assertEqual(len(self.obstacle_map._factories), 4)
        self.assertIn(self.obstacle_map._big_obstacles, self.obstacle_map._factories)
        self.assertIn(self.obstacle_map._small_obstacles, self.obstacle_map._factories)
        self.assertIn(self.obstacle_map._signs, self.obstacle_map._factories)
        self.assertIn(self.obstacle_map._gates, self.obstacle_map._factories)