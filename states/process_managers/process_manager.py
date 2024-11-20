from abc import abstractmethod, ABC

from config.logger import get_game_logger

logger = get_game_logger()


class ProcessManager(ABC):
    def __init__(self):
        self.process = None

    @abstractmethod
    def on_exit(self):
        if hasattr(self, "process") and self.process is not None:
            self.process.terminate()
            self.process.join()
            del self.process
            logger.info(f'Deleted obstacle process')