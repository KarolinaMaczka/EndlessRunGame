import unittest
from unittest.mock import Mock
from ursina import Entity

from config.constants import CollisionType, CollisionSide
from entities.obstacles.obstacle import Obstacle


class ObstacleTest(unittest.TestCase):
    def setUp(self):
        self.obstacle = Obstacle(position_z=0, difficulty=1, lane=1, height=10, width=8, depth=10)

    def test_set_fixed_width(self):
        obstacle = Mock(bounds=Mock(size=(1, 1, 1)), scale_x=1)
        Obstacle.set_fixed_width(obstacle, 2)
        self.assertAlmostEqual(obstacle.scale_x, 2)

    def test_set_fixed_depth(self):
        obstacle = Mock(bounds=Mock(size=(1, 1, 1)), scale_z=1)
        Obstacle.set_fixed_depth(obstacle, 2)
        self.assertAlmostEqual(obstacle.scale_z, 2)

    def test_set_fixed_height(self):
        obstacle = Mock(bounds=Mock(size=(1, 1, 1)), scale_y=1)
        Obstacle.set_fixed_height(obstacle, 2)
        self.assertAlmostEqual(obstacle.scale_y, 2)

    def test_set_y_position(self):
        obstacle = Mock(bounds=Mock(start=(0, 3, 0)), y=2)
        Obstacle.set_y_position(obstacle)
        self.assertAlmostEqual(obstacle.y, -2)

    def test_set_pos_z(self):
        child = Entity()
        self.obstacle.children = [child]

        self.obstacle.set_position_z(1)
        self.assertAlmostEqual(child.z, 1)
        self.assertAlmostEqual(self.obstacle.position_z, 1)
        self.assertAlmostEqual(self.obstacle.z, 1)

    def test_set_colorr(self):
        child = Mock()
        self.obstacle.children = [child]
        self.obstacle.set_colorr("grey")
        self.assertEqual(child.color, "grey")

    def test_check_collision_type_full(self):
        player_x, player_y, player_z = 0, 0, 0
        child = Mock(x=3)

        collision_type = self.obstacle.check_collision_type(player_x, player_y, player_z, child)

        self.assertEqual(collision_type, CollisionType.FULL)

    def test_check_collision_type_light(self):
        player_x, player_y, player_z = 0, 0, 0
        child = Mock(x=4)

        collision_type = self.obstacle.check_collision_type(player_x, player_y, player_z, child)
        self.assertEqual(collision_type, CollisionType.LIGHT)

    def test_check_collision_side_up(self):
        player_x, player_y = 0, 11
        child = Mock(y=4, bounds=Mock(start=(0, 0, 0)))
        self.obstacle.children = [child]
        collision_side = self.obstacle.check_collision_side(player_x, player_y, child)
        self.assertEqual(collision_side, CollisionSide.UP)

    def test_check_collision_side_down(self):
        player_x, player_y = 0, 3
        child = Mock(y=4, x=0, bounds=Mock(start=(0, 0, 0)))
        self.obstacle.children = [child]
        collision_side = self.obstacle.check_collision_side(player_x, player_y, child)
        self.assertEqual(collision_side, CollisionSide.DOWN)

    def test_check_collision_side_left(self):
        player_x, player_y = -5, 4
        child = Mock(y=4, x=0, bounds=Mock(start=(0, 0, 0)))
        self.obstacle.children = [child]
        collision_side = self.obstacle.check_collision_side(player_x, player_y, child)
        self.assertEqual(collision_side, CollisionSide.LEFT)

    def test_check_collision_side_right(self):
        player_x, player_y = 5, 4
        child = Mock(y=4, x=0, bounds=Mock(start=(0, 0, 0)))
        self.obstacle.children = [child]
        collision_side = self.obstacle.check_collision_side(player_x, player_y, child)
        self.assertEqual(collision_side, CollisionSide.RIGHT)
