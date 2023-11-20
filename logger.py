import logging
from config import LOGFILE


class Logger:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filename=f"logs/{LOGFILE}")
        self.logger = logging.getLogger(__name__)
        self.logger.info("Logger created")

    def log(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)
