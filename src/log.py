import logging
from pathlib import Path
from typing import Union


def configure_logging(log_file: Union[str, Path]):
    """Configuring logger"""

    logging_format = "[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(message)s]"
    formatter = logging.Formatter(logging_format)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logging.root.setLevel(logging.DEBUG)
    logging.root.addHandler(console_handler)
    logging.root.addHandler(file_handler)
