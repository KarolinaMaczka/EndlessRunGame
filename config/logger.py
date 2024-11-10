import logging

def get_game_logger():
    if 'game_logger' in logging.Logger.manager.loggerDict:
        return logging.getLogger('game_logger')

    logger = logging.getLogger('game_logger')
    logger.setLevel(logging.DEBUG)

    if not logger.hasHandlers():
        file_handler = logging.FileHandler('output.log')
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

