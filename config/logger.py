import logging
import sys

class LogPrints:
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level

    def write(self, message):
        if message.strip():
            self.logger.log(self.log_level, message.strip())

    def flush(self):
        pass

def get_game_logger():
    if 'game_logger' in logging.Logger.manager.loggerDict:
        return logging.getLogger('game_logger')

    logger = logging.getLogger('game_logger')
    logger.setLevel(logging.DEBUG)

    if not logger.hasHandlers():
        file_handler = logging.FileHandler('output.log', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    try:
        # nie przekierowuje się przy aplikacji z samym gui
        if hasattr(sys.stdout, "write") and hasattr(sys.stderr, "write"):
            sys.stdout = LogPrints(logger, logging.INFO)
            sys.stderr = LogPrints(logger, logging.ERROR)
    except Exception as e:
        logger.error(f"Error redirecting stdout, stderr: {e}")

    return logger


