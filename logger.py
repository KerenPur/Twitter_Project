"""
This file is responsible for creating th log file
"""
import json
import logging


def create_log():
    """
    This function creates logging object
    :return: logging object
    """
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)
    except FileNotFoundError as e:
        print(f"configuration config_file is missing, error: {e}")

    logger = logging.getLogger(config["LOG_NAME"])
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(config["LOG_NAME"] + '.log')
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s -%(levelname)s -%(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger

