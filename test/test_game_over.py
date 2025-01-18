import unittest
from unittest.mock import MagicMock, Mock
from ursina import Ursina, color

from states.impl.game_over_state import GameOver
class TestGameOver(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.context = MagicMock()
        ursina = Ursina()

    @classmethod
    def setUp(self):
        self.context.player.Z = 123
        self.context.data_manager.add_score = Mock()
        self.context.data_manager.add_player_satisfaction = Mock()
        self.context.data_manager.save = Mock()
        self.context.data_manager.clean_data = Mock()

        self.game_over = GameOver(self.context)

    def test_init(self):
        self.assertEqual(self.game_over.score, 123)
        self.context.data_manager.add_score.assert_called_with(123)

    def test_set_rating(self):
        self.game_over.set_rating( 'satisfaction', 3)
        for i, star in enumerate(self.game_over.stars_satisfaction):
            if i < 3:
                self.assertEqual(star.text_entity.color, color.yellow)
            else:
                self.assertEqual(star.text_entity.color, color.gray)

