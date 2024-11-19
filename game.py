import multiprocessing

from ursina import Ursina, window, Sky, Text

from config.logger import get_game_logger
from entities.camera import PlayerCamera
from game_manager import GameManager
from entities.player import Player
import atexit

from multiprocessing import Process, Queue, Manager
from camera_reading.read_camera import CameraReader
from data_manager import DataManager


if __name__ == '__main__':
    logger = get_game_logger()
    logger.info('Starting game')

    list_manager = Manager()
    data_manager = DataManager(list_manager)

    emotion_queue = Queue()
    ready_queue = Queue()
    camera_ready_event = multiprocessing.Event()

    camera_reading = CameraReader(data_manager, list_manager)
    p = Process(target=camera_reading.run, args=(ready_queue,emotion_queue, camera_ready_event))
    p.start()

    def on_exit():
        p.terminate()
        p.join()
        logger.info('Closed camera process')
        
    atexit.register(on_exit)

    app = Ursina()

    window.fps_counter.enabled = True
    # window.exit_button.enabled = False
    #TODO fill
    window.title = 'Game'

    player = Player()

    camera = PlayerCamera(player)

    game_manager = GameManager(player, camera, data_manager, ready_queue, camera_reading, emotion_queue)
    atexit.register(game_manager.on_exit)

    camera_ready_event.wait()
    logger.info('Camera process started')

    score_tracker = Text(text=f'0', position=(-0.8, 0.5), scale=1.5)
    def update():
        game_manager.update()
        if game_manager._state.__class__.__name__ == 'RunningState':
            if int(game_manager._state.obstacle_generator.player_z.value) % 100 == 0:
                score_tracker.text = f'Score:{str(int(game_manager._state.obstacle_generator.player_z.value))}'
        else:
            score_tracker.text = 'Score: 0'

    def input(key):
        if game_manager._state.__class__.__name__ == 'RunningState':
            if key in ['w', 'a', 's', 'd', 'space', 'w up', 'a up', 's up', 'd up', 'space up']:
                data_manager.save_pressed_key((f'{key}', game_manager._state.obstacle_generator.player_z.value))

    sky = Sky()

    app.run()
