from entities.camera import PlayerCamera
from physics_engine import PhysicsEngine
from entities.player import Player
from states.impl.game_over_state import GameOver
from states.impl.running_state import RunningState
from camera_reading.read_camera import CameraReader

class GameManager:
    _state = None
    emotion_holder = None
    def __init__(self, player: Player, camera: PlayerCamera, camera_reader: CameraReader):
        self.player = player
        self.camera = camera
        self.camera_reader = camera_reader

        self.physics_engine = PhysicsEngine(player, camera)
        self._state = RunningState(self, camera_reader.emotion_holder)

    def transition_to(self, state: str):
        self._state.on_exit()
        if state == "running_state":
            self.camera_reader.game_is_running = True # Start reading camera
            self._state = RunningState(self, self.emotion_holder)
        elif state == "game_over_state":
            self._state = GameOver(self)
            self.camera_reader.game_is_running = False

    def update(self):
        self._state.update()

    def on_exit(self):
        print('exiting')
        self._state.on_exit()
