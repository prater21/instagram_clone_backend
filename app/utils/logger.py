import logging
import sys
from typing import Optional

# loggin setting
logger = logging.getLogger("main")

# create format
formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s\n")

# create handler
steam_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("app.log")

# set log-level
logger.setLevel(logging.INFO)
file_handler.setLevel(logging.ERROR)

# set formatters
steam_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)


# add handler to the logger
logger.handlers = [steam_handler, file_handler]


def log_request(url, method, parmas):
    log_dict = f"{method} - {url} - [REQUEST]"

    if parmas:
        log_dict += f"\n{parmas}"

    logger.info(log_dict)


def log_request_auth(url, method, user_info, parmas):
    log_dict = f"{method} - {url} - [REQUEST]"

    log_dict += f"\nuser_info:{user_info},"
    if parmas:
        log_dict += f"{parmas}"

    logger.info(log_dict)


def log_error(url, method, status_code, error_msg):
    log_dict = f"{method} - {url} - [ERROR]\n[{status_code}]{error_msg}"

    logger.error(log_dict)
