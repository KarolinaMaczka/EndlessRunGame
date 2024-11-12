from config.logger import get_game_logger
from data_manager import DataManager
from entities.camera import PlayerCamera
from physics_engine import PhysicsEngine
from entities.player import Player
from states.impl.game_over_state import GameOver
from states.impl.main_menu import MainMenu
from states.impl.running_state import RunningState
from states.impl.change_settings import SettingsMenu
from camera_reading.read_camera import CameraReader
from multiprocessing import Queue

import time
logger = get_game_logger()
class GameManager:
    camera = None
    _state = None
    def __init__(self, player: Player, camera: PlayerCamera, data_manager: DataManager, queue: Queue, camera_reader: CameraReader):
        self.player = player
        self.camera = camera
        self.time_playing = 0

        self.data_manager = data_manager
        self.camera_reader = camera_reader
        self.queue = queue
        self.physics_engine = PhysicsEngine(player, camera, self.data_manager)
        self._state = MainMenu(self)
        RunningState(self).on_exit()

    def transition_to(self, state: str):
        logger.info(f'Transitioning to {state}')
        self._state.on_exit()
        if state == "running_state":
            self.time_playing = time.time()
            self.queue.put(True)
            self._state = RunningState(self)
        elif state == "game_over_state":
            self.time_playing = time.time() - self.time_playing
            self.data_manager.playing_time = self.time_playing
            self.queue.put(False)
            logger.info(f'game over, score: {self.player.Z}')
            self.data_manager.score = self.player.Z
            self._state = GameOver(self)
        elif state == "main_menu":
            self._state = MainMenu(self)
        elif state == "change_settings":
            self._state = SettingsMenu(self, self.camera_reader.cameras)

    def update(self):
        self._state.update()

    def on_exit(self):
        logger.info(f'Exiting game manager {self.player.Z}')
        self._state.on_exit()
