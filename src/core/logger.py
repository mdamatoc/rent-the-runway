from decouple import config
import logging


class Logger:
    def __init__(self, name: str):
        self.instance = logging.getLogger(name)
        self.instance.setLevel(config('LOG_LEVEL'))
