import unittest
from unittest.mock import Mock
from entities.obstacles.lane_obstacle import LaneObstacle
from config.constants import ROAD_WIDTH, LANE_WIDTH


class LaneObstacleTest(unittest.TestCase):

    def setUp(self):
        models = Mock()
        self.lane_obstacle = LaneObstacle(models, position_z=0, difficulty=1,lane=1, height=10, width=8, depth=10)
        self.child1 = Mock()
        self.child2 = Mock()
        self.lane_obstacle.children = [self.child1, self.child2]

    def test_set_fixed_lane(self):
        lane = 1
        expected_x = -ROAD_WIDTH / 2 + LANE_WIDTH / 2 + lane * LANE_WIDTH
        LaneObstacle.set_fixed_lane(self.child1, lane)

        self.assertEqual(self.child1.x, expected_x)

    def test_set_lane_calls(self):
        new_lane = 2
        with unittest.mock.patch('entities.obstacles.lane_obstacle.invoke') as mock_invoke:
            self.lane_obstacle.set_lane(new_lane)

            self.assertEqual(mock_invoke.call_count, 2)
            mock_invoke.assert_any_call(LaneObstacle.set_fixed_lane, self.child1, new_lane)
            mock_invoke.assert_any_call(LaneObstacle.set_fixed_lane, self.child2, new_lane)

    def test_set_lane(self):
        self.lane_obstacle.set_lane(2)
        self.assertEqual(self.lane_obstacle.lane, 2)
