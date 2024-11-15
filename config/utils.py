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
