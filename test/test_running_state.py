import unittest
from unittest.mock import MagicMock, patch

from ursina import Ursina
from states.impl.running_state import RunningState


class TestRunningState(unittest.TestCase):

    @patch('states.impl.running_state.ObstacleProcesManager')
    @patch('states.impl.running_state.Scenery')
    @patch('states.impl.running_state.DifficultyManager')
    @patch('states.impl.running_state.DifficultyLogic')
    @patch('states.impl.running_state.ObstaclePool')
    @patch('states.impl.running_state.WindowPanel')
    @patch('states.impl.running_state.application')
    def setUp(self, mock_application, mock_window_panel, mock_obstacle_pool, mock_difficulty_logic, mock_difficulty_manager, mock_scenery, mock_obstacle_process_manager):
        ursina = Ursina()

        self.mock_context = MagicMock()
        self.mock_context.data_manager.save_difficulty = MagicMock()
        self.mock_context.data_manager.add_playing_time = MagicMock()
        self.mock_context.player.z = 0
        self.mock_context.camera_reader.emotion_queue = MagicMock()
        self.mock_context.physics_engine.apply_gravity = MagicMock()
        self.mock_context.physics_engine.handle_player_collisions = MagicMock()
        self.mock_context.player.run = MagicMock()
        self.mock_context.player.reset = MagicMock()
        self.mock_context.player.enabled = True

        self.running_state = RunningState(self.mock_context, models=MagicMock(), camera_reader=MagicMock(), selected_difficulty_level=1)

    def test_handle_input(self):
        self.running_state.handle_input()
        self.running_state.context.player.reset.assert_called_once()

    def test_set_difficulty(self):
        new_level = 3
        self.running_state.set_difficulty(new_level)
        self.assertEqual(self.running_state.obstacle_generator.difficulty_level.value, new_level)
        self.running_state.difficulty_manager.set_player_settings.assert_called_with(new_level, self.running_state.context.player)

    def test_update_score(self):
        self.running_state.context.player.z = 250
        self.running_state._RunningState__update_score()
        self.assertEqual(self.running_state.score_tracker.text, 'Score:300')

    def test_cleanup_obstacles(self):
        self.running_state.active_obstacles = [MagicMock(z=100), MagicMock(z=50)]
        self.running_state.context.player.z = 1000
        self.running_state._RunningState__cleanup_obstacles()
        self.assertEqual(len(self.running_state.active_obstacles), 0)

    def test_toggle_paused(self):
        self.running_state._RunningState__toggle_paused()
        self.assertTrue(self.running_state.pause_panel.enabled)
        self.running_state._RunningState__toggle_paused()
        self.assertFalse(self.running_state.pause_panel.enabled)
