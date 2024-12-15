import unittest
from unittest.mock import patch, Mock
from entities.obstacles.obstacle_metadata import ObstacleMetaData
from entities.obstacles.obstacle_metadata_factory import ObstacleMetadataFactory
from entities.obstacles.impl.board_obstacle import ObstacleBoard

class ObstacleMetadataFactoryTest(unittest.TestCase):

    def setUp(self):
        self.obstacle_1 = ObstacleMetaData(obstacle=Mock(), probability=0.7, difficulty=1)
        self.obstacle_2 = ObstacleMetaData(obstacle=Mock(), probability=0.3, difficulty=2)
        self.obstacle_1.obstacle.__name__ = 'MockObstacle1'
        self.obstacle_2.obstacle.__name__ = 'MockObstacle2'
        self.obstacle_1.entity_metadata = {}
        self.obstacle_2.entity_metadata = {}
        self.init_lane_obstacles = [{"obstacle": self.obstacle_1.obstacle, "probability": 0.7, "difficulty": 1},
            {"obstacle": self.obstacle_2.obstacle, "probability": 0.3, "difficulty": 2},
        ]
        self.factory = ObstacleMetadataFactory(self.init_lane_obstacles, lanes=3)

    def test_get_random(self):
        with patch('random.uniform') as mock_random:
            mock_random.return_value = 0.5
            selected_obstacle = self.factory.get_random()

            self.assertEqual(selected_obstacle.probability, self.obstacle_1.probability)
            self.assertEqual(selected_obstacle.difficulty, self.obstacle_1.difficulty)

            mock_random.return_value = 0.7
            selected_obstacle = self.factory.get_random()

            self.assertEqual(selected_obstacle.probability, self.obstacle_2.probability)
            self.assertEqual(selected_obstacle.difficulty, self.obstacle_2.difficulty)


    def test_apply_color_palette(self):
        palette = {'MockObstacle1': 'green', 'MockObstacle2': 'blue'}

        self.factory.apply_color_palette(palette)

        self.assertEqual(self.factory.get_obstacles()[0].entity_metadata['colorr'], 'green')
        self.assertEqual(self.factory.get_obstacles()[1].entity_metadata['colorr'], 'blue')

    def test_create_obstacle(self):
        position_z = 10
        lane = 1
        with patch.object(self.factory, 'get_random', return_value=self.obstacle_1):
            obstacle = self.factory.create_obstacle(position_z, lane)
            self.assertEqual(obstacle.position_z, position_z)
            self.assertEqual(obstacle.lane, lane)

    def test_create_obstacle_random_selection(self):
        with patch('random.uniform', return_value=0.5):
            with patch.object(self.factory, 'get_random', return_value=self.obstacle_1):
                obstacle = self.factory.create_obstacle(position_z=5, lane=2)
                self.assertEqual(obstacle.position_z, 5)
                self.assertEqual(obstacle.lane, 2)
            with patch.object(self.factory, 'get_random', return_value=self.obstacle_2):
                obstacle = self.factory.create_obstacle(position_z=5, lane=2)
                self.assertEqual(obstacle.position_z, 5)
                self.assertEqual(obstacle.lane, 2)


