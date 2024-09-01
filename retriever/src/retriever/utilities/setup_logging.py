import logging
import os
from datetime import datetime

from .config import config


def setup_logging():
    logging.basicConfig(
        filename=os.path.join(
            config.logs_dir_path, f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
        ),
        level=logging.INFO,
    )
