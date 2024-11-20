from config.logger import get_game_logger
from data_manager import DataManager
from entities.camera import PlayerCamera
from physics_engine import PhysicsEngine
from entities.player import Player
from states.impl.game_over_state import GameOver
from states.impl.main_menu import MainMenu
from states.impl.running_state import RunningState
from states.impl.level_select import LevelSelect
from states.impl.change_settings import SettingsMenu
from states.process_managers.impl.read_camera import CameraReader

import time
logger = get_game_logger()
class GameManager:
    camera = None
    _state = None
    def __init__(self, player: Player, camera: PlayerCamera, data_manager: DataManager,
                  camera_reader: CameraReader):
        self.player = player
        self.camera = camera
        self.time_playing = 0
        self.selected_level = 1

        self.data_manager = data_manager
        self.camera_reader = camera_reader
        self.physics_engine = PhysicsEngine(player, camera, self.data_manager)
        RunningState(self).on_exit()
        self.data_manager.clean_data()
        self._state = MainMenu(self)

    def transition_to(self, state: str):
        logger.info(f'Transitioning to {state}')
        self._state.on_exit()
        if state == "running_state":
            self.time_playing = time.time()
            self._state = RunningState(self, self.selected_level)
            self.camera_reader.toggle_run()
        elif state == "game_over_state":
            self.time_playing = time.time() - self.time_playing
            self.data_manager.playing_time = self.time_playing
            logger.info(f'game over, score: {self.player.Z}')
            self.data_manager.score = self.player.Z
            self._state = GameOver(self)
            self.camera_reader.toggle_run()
        elif state == "main_menu":
            self._state = MainMenu(self)
        elif state == "change_settings":
            self._state = SettingsMenu(self, self.camera_reader)
        elif state == "level_select":
            self._state = LevelSelect(self)

    def update(self):
        self._state.update()

    def input(self, key):
        self._state.input(key)

    def on_exit(self):
        logger.info(f'Exiting game manager {self.player.Z}')
        self._state.on_exit()

