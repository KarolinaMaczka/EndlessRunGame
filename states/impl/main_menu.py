from ursina import destroy, color, WindowPanel, Button, application

from config.logger import get_game_logger
from states.state import GameState

logger = get_game_logger()

class MainMenu(GameState):
    def __init__(self, context):
        self.context = context
        self.create_window()

    def handle_input(self):
        pass

    def update(self):
        pass

    def on_exit(self):
        logger.info(f'Exiting main menu')
        destroy(self.context.window_panel)
        self.context.window_panel = None

    def start(self):
        self.on_exit()
        self.context.transition_to('running_state')

    def change_settings(self):
        self.on_exit()
        self.context.transition_to('change_settings')

    def create_window(self):
        self.context.window_panel = WindowPanel(
            title='Main Menu',
            content=(
                Button('Play the Game', color=color.gray, on_click=self.start),
                Button('Change Settings', color=color.gray, on_click=self.change_settings),
                Button('Quit', color=color.red, on_click=application.quit)
            ),
            position=(0, 0)
        )