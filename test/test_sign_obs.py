import unittest
from unittest.mock import Mock
from ursina import Entity
from entities.obstacles.sign_obstacle import ObstacleSign
from config.constants import ROAD_WIDTH, LANE_WIDTH, CollisionType, CollisionSide
import random


class ObstacleSignTest(unittest.TestCase):
    def setUp(self):
        models = Mock()
        self.obstacle_sign = ObstacleSign(models, position_z=0, difficulty=1, lane=1, height=10, width=8, depth=10)
        self.child_1 = Mock()
        self.child_2 = Mock()
        self.obstacle_sign.children = [self.child_1, self.child_2]

    def test_set_fixed_lane(self):
        lane = 1
        expected_x = -ROAD_WIDTH / 2 + lane * LANE_WIDTH
        ObstacleSign.set_fixed_lane(self.child_1, lane)
        self.assertEqual(expected_x, self.child_1.x)

    def test_set_lane_calls(self):
        new_lane = 2
        with unittest.mock.patch('entities.obstacles.sign_obstacle.invoke') as mock_invoke:
            self.obstacle_sign.set_lane(new_lane)
            self.assertEqual(mock_invoke.call_count, 2)
            mock_invoke.assert_any_call(ObstacleSign.set_fixed_lane, self.child_1, new_lane)
            mock_invoke.assert_any_call(ObstacleSign.set_fixed_lane, self.child_2, new_lane)

    def test_check_collision_type(self):
        collision_type = self.obstacle_sign.check_collision_type()
        self.assertEqual(collision_type, CollisionType.LIGHT)

    def test_check_collision_side_left(self):
        with unittest.mock.patch('random.random', return_value=0.2):
            collision_side = self.obstacle_sign.check_collision_side()
            self.assertEqual(collision_side, CollisionSide.LEFT)

    def test_check_collision_side_right(self):
        with unittest.mock.patch('random.random', return_value=0.8):
            collision_side = self.obstacle_sign.check_collision_side()
            self.assertEqual(collision_side, CollisionSide.RIGHT)

    def test_change_lane(self):
        self.obstacle_sign.set_lane(2)
        self.assertEqual(self.obstacle_sign.lane, 2)

