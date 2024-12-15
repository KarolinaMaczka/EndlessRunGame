import unittest
from unittest.mock import MagicMock, patch
from entities.player import Player
from ursina import time
from config.constants import CollisionSide, CollisionType

class TestPlayer(unittest.TestCase):

    def setUp(self):
        # patch('entities.player.Entity', MagicMock())
        self.player = Player()

    def test_set_jump(self):
        self.player.set_jump()
        self.assertTrue(self.player.is_jumping)
        self.assertEqual(self.player.velocity_y, self.player.jump_height)

    def test_set_climb(self):
        climb_height = 5
        self.player.set_climb(climb_height)
        self.assertTrue(self.player.is_climbing)
        self.assertEqual(self.player.speed, 0)
        self.assertEqual(self.player.climb_height, climb_height)

    def test_stop_climb(self):
        climb_height = 5
        self.player.set_climb(climb_height)
        self.player.stop_climb()
        self.assertFalse(self.player.is_climbing)
        self.assertTrue(self.player.is_falling)
        self.assertEqual(self.player.y, climb_height + 1)

    def test_land(self):
        ground_y = 10
        self.player.land(ground_y)
        self.assertEqual(self.player.y, ground_y)
        self.assertFalse(self.player.is_jumping)
        self.assertFalse(self.player.is_falling)

    def test_crouch(self):
        self.player.crouch()
        self.assertTrue(self.player.is_crouching)

    def test_reset(self):
        self.player.crouch()
        self.player.reset()
        self.assertFalse(self.player.is_crouching)

    def test_bounce_left(self):
        self.player.bounce(side=CollisionSide.LEFT)
        self.assertEqual(self.player.x, -self.player.bouncing_dist)

    def test_bounce_down(self):
        self.player.bounce(side=CollisionSide.DOWN)
        self.assertEqual(self.player.z, -self.player.bouncing_dist)

