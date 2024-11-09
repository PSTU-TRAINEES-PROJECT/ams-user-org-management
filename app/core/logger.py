from colorlog import ColoredFormatter
import logging

custom_logger = logging.getLogger("custom_logger")
custom_logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
formatter = ColoredFormatter(
    "%(log_color)s[%(asctime)s] - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    reset=True,
    log_colors={
        "DEBUG": "green",
        "INFO": "cyan",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
)
handler.setFormatter(formatter)
custom_logger.addHandler(handler)

logger = custom_logger