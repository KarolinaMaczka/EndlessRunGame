from data_manager import DataManager
from entities.camera import PlayerCamera
from physics_engine import PhysicsEngine
from entities.player import Player
from states.impl.game_over_state import GameOver
from states.impl.main_menu import MainMenu
from states.impl.running_state import RunningState
from camera_reading.read_camera import CameraReader

class GameManager:
    _state = None
    emotion_holder = None
    def __init__(self, player: Player, camera: PlayerCamera, camera_reader: CameraReader, data_manager: DataManager):
        self.player = player
        self.camera = camera
       
        self.data_manager = data_manager
        self.camera_reader = camera_reader
        self.physics_engine = PhysicsEngine(player, camera, self.data_manager)
        self._state = MainMenu(self)
        RunningState(self, camera_reader.emotion_holder).on_exit()
        self.data_manager.clean_data()

    def transition_to(self, state: str):
        self._state.on_exit()
        if state == "running_state":
            self.camera_reader.game_is_running = True # Start reading camera
            self._state = RunningState(self, self.emotion_holder)
        elif state == "game_over_state":
            self._state = GameOver(self)
            self.camera_reader.game_is_running = False
        elif state == "main_menu":
            self._state = MainMenu(self)
        elif state == "change_settings":
            print("change settings")

    def update(self):
        self._state.update()

    def on_exit(self):
        print('exiting')
        self._state.on_exit()
