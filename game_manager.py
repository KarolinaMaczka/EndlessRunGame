from entities.camera import PlayerCamera
from physics_engine import PhysicsEngine
from entities.player import Player
from states.impl.game_over_state import GameOver
from states.impl.running_state import RunningState


class GameManager:
    _state = None

    def __init__(self, player: Player, camera: PlayerCamera):
        self.player = player
        self.camera = camera

        self.physics_engine = PhysicsEngine(player, camera)
        self._state = RunningState(self)

    def transition_to(self, state: str):
        self._state.on_exit()
        if state == "running_state":
            self._state = RunningState(self)
        elif state == "game_over_state":
            self._state = GameOver(self)

    def update(self):
        self._state.update()

    def on_exit(self):
        print('exiting')
        self._state.on_exit()
