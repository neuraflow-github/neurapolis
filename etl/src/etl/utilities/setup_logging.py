import logging
import os
from datetime import datetime

from .config import config


def setup_logging():
    log_file_path = os.path.join(
        config.logs_dir_path, f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file_path), logging.StreamHandler()],
    )
