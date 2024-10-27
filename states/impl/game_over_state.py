from ursina import destroy, color, WindowPanel, Button, application

from states.state import GameState


class GameOver(GameState):
    def __init__(self, context):
        self.context = context
        self.create_window()

    def handle_input(self):
        pass

    def update(self):
        pass

    def on_exit(self):
        pass

    def start(self):
        destroy(self.context.window_panel)
        self.context.window_panel = None
        self.context.transition_to('running_state')

    def create_window(self):
        self.context.window_panel = WindowPanel(
            title='Game Over :(',
            content=(
                Button('Try Again', color=color.gray, on_click=self.start),
                Button('Quit', color=color.red, on_click=application.quit)
            ),
            position=(0, 0)
        )

