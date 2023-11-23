import json
import os
import logging


def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger object with a given name.

    :param name: The name of the logger.
    :return: The logger object.
    """
    logger = logging.getLogger(name)
    logger.addHandler(logging.StreamHandler())
    return logger


def load_settings_file():
    """
    Load settings to the environment from the local.settings.json file.

    :return: None
    """
    with open("local.settings.json") as f:
        content = json.load(f)

    for key, value in content["Values"].items():
        os.environ[key] = str(value)
