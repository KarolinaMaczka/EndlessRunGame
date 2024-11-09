from data_manager import DataManager
from entities.camera import PlayerCamera
from physics_engine import PhysicsEngine
from entities.player import Player
from states.impl.game_over_state import GameOver
from states.impl.main_menu import MainMenu
from states.impl.running_state import RunningState
from camera_reading.read_camera import CameraReader
from multiprocessing import Queue

class GameManager:
    _state = None
    def __init__(self, player: Player, camera: PlayerCamera, data_manager: DataManager, queue: Queue, camera_reader: CameraReader):
        self.player = player
        self.camera = camera
       
        self.data_manager = data_manager
        self.camera_reader = camera_reader
        self.queue = queue
        self.physics_engine = PhysicsEngine(player, camera, self.data_manager)
        self._state = MainMenu(self)
        RunningState(self).on_exit()
        self.data_manager.clean_data()

    def transition_to(self, state: str):
        self._state.on_exit()
        if state == "running_state":
            self.queue.put(True)
            self._state = RunningState(self)
        elif state == "game_over_state":
            self.queue.put(False)
            self._state = GameOver(self)
        elif state == "main_menu":
            self._state = MainMenu(self)
        elif state == "change_settings":
            print("change settings")

    def update(self):
        self._state.update()

    def on_exit(self):
        print('exiting')
        self._state.on_exit()
