from config.logger import get_game_logger
import traceback


def catch_exceptions(func):
    logger = get_game_logger()

    def wrapped_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logger.error(traceback.format_exc())
            return None

    return wrapped_func

import pygetwindow as gw

def set_window_on_top(window_title):
    try:
        win = gw.getWindowsWithTitle(window_title)[0]
        win.activate()
        win.alwaysOnTop = True
    except Exception:
        print(f"No window with name: {window_title}")

import ctypes
import time

# def set_window_on_top(window_name):
#     """
#     Set an OpenCV window on top (Windows only).
#     """
#     hwnd = ctypes.windll.user32.FindWindowW(None, window_name)
#     if hwnd:
#         ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 3)
#     else:
#         print(f"Window '{window_name}' not found.")