from config.logger import get_game_logger
import traceback
import pygetwindow as gw

def catch_exceptions(func):
    logger = get_game_logger()

    def wrapped_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logger.error(traceback.format_exc())
            return None

    return wrapped_func

def set_window_on_top(window_title):
    try:
        win = gw.getWindowsWithTitle(window_title)[0]
        win.activate()
        win.alwaysOnTop = True
    except Exception:
        print(f"No window with name: {window_title}")
