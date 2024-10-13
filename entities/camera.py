import random
from ursina import SmoothFollow, Vec3, invoke, camera

from entities.player import Player


class PlayerCamera:
    def __init__(self, player: Player, *args, **kwargs):
        self.camera = camera
        self.player = player
        self.camera.z = -15
        self.camera.add_script(SmoothFollow(target=player, offset=(0, 5, -30)))

    def shake_camera(self, duration=0.2, magnitude=0.05):
        original_position = self.camera.position

        def shake():
            self.camera.position = Vec3(
                original_position.x + random.uniform(-magnitude, magnitude),
                original_position.y + random.uniform(-magnitude, magnitude),
                original_position.z
            )

        for _ in range(int(duration * 100)):
            invoke(shake, delay=random.uniform(0, duration))

        invoke(lambda: setattr(self.camera, 'position', original_position), delay=duration)
