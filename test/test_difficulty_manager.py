import unittest
from unittest.mock import MagicMock, patch
from config.logger import get_game_logger
from difficulty.difficulty.difficulty_level import Difficulty
from difficulty.difficulty.difficulty_levels import DifficultyTest1, DifficultyTest2, DifficultyTest3, \
    DifficultyEasyHiddenMinus1
from difficulty.difficulty_manager import DifficultyManager


class TestDifficultyManager(unittest.TestCase):

    def setUp(self):
        self.difficulty_manager = DifficultyManager()
        self.player = MagicMock()
        self.difficulty_test_1 = DifficultyTest1()

    @patch.object(DifficultyManager, 'get_player_settings', return_value={"speed": 300, "jump_height": 0.50, "gravity": -1, "velocity_x": 30,"prev_speed": 200, "bouncing_dist": 5
    })
    def test_set_player_settings(self, mock_get_player_settings):
        self.difficulty_manager.set_player_settings(1, self.player)

        self.assertEqual(self.player.speed, 300)
        self.assertEqual(self.player.jump_height, 0.50)
        self.assertEqual(self.player.gravity, -1)
        self.assertEqual(self.player.velocity_x, 30)
        self.assertEqual(self.player.prev_speed, 200)
        self.assertEqual(self.player.bouncing_dist, 5)

    def test_change_level_class(self):
        prev_difficulty = self.difficulty_test_1
        new_difficulty = 2
        difficulty_object = self.difficulty_manager.change_level_class(new_difficulty, prev_difficulty)

        self.assertIsInstance(difficulty_object, DifficultyEasyHiddenMinus1)

