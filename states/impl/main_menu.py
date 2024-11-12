from ursina import destroy, color, WindowPanel, Button, application, Text

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

    def toggle_send_data(self):
        self.context.data_manager.send_data_enabled = not self.context.data_manager.send_data_enabled
        self.toggle_button.text = "Don't send data" if self.context.data_manager.send_data_enabled else "Send Data"
        temp_text = Text(
            text="Sending data is enabled" if self.context.data_manager.send_data_enabled else "Sending data is disabled",
            position=(0, 0.4),
            origin=(0, 0),
            color=color.black
        )
        destroy(temp_text, delay=1.5)

    def create_window(self):
        self.toggle_button = Button(
            text="Don't send data" if self.context.data_manager.send_data_enabled else "Send Data",
            color=color.gray,
            on_click=self.toggle_send_data
        )

        self.context.window_panel = WindowPanel(
            title='Main Menu',
            content=(
                Button('Play the Game', color=color.gray, on_click=self.start),
                self.toggle_button,
                Button('Change Settings', color=color.gray, on_click=self.change_settings),
                Button('Quit', color=color.red, on_click=application.quit)
            ),
            position=(0, 0)
        )