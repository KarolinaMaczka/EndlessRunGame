from abc import ABC, abstractmethod
from ursina import Text, destroy


class GameState(ABC):

    def __init__(self):
        self.window_panel = None

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
        pass