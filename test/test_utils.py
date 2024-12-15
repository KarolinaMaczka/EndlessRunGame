import unittest
from entities.obstacles.utils import left_outer_border_lane, left_inner_border_lane, right_inner_border_lane, \
    right_outer_border_lane, right_border_lane, left_border_lane


class TestUtils(unittest.TestCase):

    def test_left_outer_border_lane(self):
        lane = 2
        result = left_outer_border_lane(lane)
        self.assertEqual(result, 4)

    def test_left_inner_border_lane(self):
        lane = 1
        result = left_inner_border_lane(lane)
        self.assertEqual(result, -4)

    def test_right_inner_border_lane(self):
        lane = 2
        result = right_inner_border_lane(lane)
        # expected = -ROAD_WIDTH / 2 + LANE_WIDTH * (lane + 1) - 1
        self.assertEqual(result, 14)

    def test_right_outer_border_lane(self):
        lane = 2
        result = right_outer_border_lane(lane)
        self.assertEqual(result, 16)

    def test_right_border_lane(self):
        lane = 0
        result = right_border_lane(lane)
        self.assertEqual(result, -5)

    def test_left_border_lane(self):
        lane = 2
        result = left_border_lane(lane)
        self.assertEqual(result, 5)
