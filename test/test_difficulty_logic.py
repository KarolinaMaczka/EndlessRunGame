import unittest
from unittest.mock import MagicMock, patch
from config.logger import get_game_logger
from multiprocessing import Queue
import time

from difficulty.difficulty_logic import DifficultyLogic

class TestDifficultyLogic(unittest.TestCase):

    def setUp(self):
        self.difficulty_logic = DifficultyLogic(MagicMock(), 1)

    @patch.object(DifficultyLogic, 'update_difficulty')
    def test_update(self, mock_update_difficulty):

        print('Testing update method of DifficultyLogic')
        queue = Queue()
        
        queue.put(('happy', 'neutral'))
        queue.put(('sad', 'fear'))
        queue.put(('angry', 'neutral'))
        queue.put(('happy', 'sad'))
        queue.put(('fear', 'angry'))
        queue.put(('happy', 'neutral'))
        queue.put(('sad', 'fear'))
        queue.put(('angry', 'neutral'))
        queue.put(('happy', 'sad'))
        queue.put(('neutral', 'angry'))

        for _ in range(9):
            self.difficulty_logic.update(1.0, queue)
            time.sleep(0.2)
            self.assertEqual(self.difficulty_logic.counter, _ + 1)
            mock_update_difficulty.assert_not_called()
        
        self.difficulty_logic.update(1.0, queue)
        self.assertEqual(self.difficulty_logic.counter, 0)
        mock_update_difficulty.assert_called_once()

        # test if emotions are added to the data manager and the emotions count is updated
        print('Testing if emotions are added to the data manager and the emotions count is updated')
         
        self.assertEqual(self.difficulty_logic.data_manager.add_emotion.call_count, 10)
        self.assertEqual(self.difficulty_logic.emotions_count, {'happy': 4, 'neutral': 1, 'sad': 2, 'angry': 2, 'fear': 1})



