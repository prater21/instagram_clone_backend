import logging
import sys

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


def log_request(url, method, path={}, query={}, body={}):
    log_dict = f"{method} - {url} - [REQUEST]"
    if path:
        log_dict += f"\n(path){path}"
    if query:
        log_dict += f"\n(query){query}"
    if body:
        log_dict += f"\n(body){body}"

    logger.info(log_dict)


def log_error(url, method, status_code, error_msg):
    log_dict = f"{method} - {url} - [ERROR]\n[{status_code}]{error_msg}"

    logger.error(log_dict)
