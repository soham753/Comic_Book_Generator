# logger_config.py

import logging

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if not logger.handlers:  # جلوگیری duplicate
        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger