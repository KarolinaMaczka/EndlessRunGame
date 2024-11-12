from ursina import destroy, color, WindowPanel, Button, Text, Func
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from camera_reading.read_camera import CameraReader

from config.logger import get_game_logger
from states.state import GameState

logger = get_game_logger()

class SettingsMenu(GameState):
    def __init__(self, context,  camera_reader: CameraReader):
        self.context = context
        self.create_window(len(camera_reader.cameras))

    def handle_input(self):
        pass

    def update(self):
        pass

    def start(self):
        pass

    def on_exit(self):
        logger.info(f'Exiting settings')
        destroy(self.context.window_panel)
        destroy(self.context.menu)
        self.context.window_panel = None
        self.context.menu = None

    def main_menu(self):
        self.context.transition_to('main_menu')

    def pass_camera(self, camera_number):
        print(f'Camera {camera_number} clicked')
        self.context.camera_reader.change_camera(camera_number-1)

    def create_window(self, camera_count):
        self.context.window_panel = WindowPanel(
            title='Settings',
            content=(
                Text('Choose appropriate camera in the upper left corner', color=color.gray, wordwrap=40),
                Button('Go back', color=color.red,
                        on_click=self.main_menu),
                
            ),        
            position=(0, 0.25),
        )
        self.context.menu = DropdownMenu(
                    text = "Cameras",
                    buttons = [DropdownMenuButton(f"Camera {i}", on_click = Func(self.pass_camera, i)) for i in range(1, camera_count+1)]
        )   