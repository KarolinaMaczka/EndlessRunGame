import unittest
from unittest.mock import MagicMock, patch
from config.logger import get_game_logger
from multiprocessing import Queue
import time

from difficulty.difficulty_logic import DifficultyLogic

class TestDifficultyLogic(unittest.TestCase):

    def setUp(self):
        self.difficulty_logic = DifficultyLogic(MagicMock(), MagicMock())
        self.context = MagicMock()
        self.difficulty_logic.change_difficulty = 'emotions'
        self.difficulty_logic.update_difficulty = MagicMock()
        self.queue = Queue()
        
        # for example, emotions = (('happy', 88.21), ('neutral', 10.002), 1.0)
        self.queue.put((('happy', 88.21), ('neutral', 10.002), 1.0))
        self.queue.put((('sad', 75.0), ('fear', 25.0), 1.0))
        self.queue.put((('angry', 60.0), ('neutral', 40.0), 1.0))
        self.queue.put((('happy', 90.0), ('sad', 10.0), 1.0))
        self.queue.put((('fear', 50.0), ('angry', 50.0), 1.0))
        self.queue.put((('happy', 85.0), ('neutral', 15.0), 1.0))

    def test_update(self):
        for _ in range(5):
            self.difficulty_logic.update(1.0, self.queue)
            time.sleep(0.2)
            self.assertEqual(self.difficulty_logic.counter, (_ + 1) % 5)
        self.difficulty_logic.update_difficulty.assert_called()
        
        self.difficulty_logic.update(1.0, self.queue)
        self.assertEqual(self.difficulty_logic.counter, 1)



