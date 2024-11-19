from abc import ABC, abstractmethod
from ursina import Text, destroy


class GameState(ABC):

    def __init__(self):
        self.score_tracker = Text(text=f'0', position=(-0.8, 0.5), scale=1.5)
        self.score_tracker.text = 'Score: 0'

    @abstractmethod
    def input(self, key):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def on_exit(self):
        destroy(self.score_tracker)