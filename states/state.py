from abc import ABC, abstractmethod


class GameState(ABC):


    @abstractmethod
    def handle_input(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def update(self):
        pass