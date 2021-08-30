from datetime import datetime
import logging


class CalTimeDecorator:
    LOGGER = logging.getLogger()

    def __init__(self, func_name):
        self.func_name = func_name

    def __call__(self, func):
        def wrapper():
            start_time = datetime.now()
            func()
            self.LOGGER.info("{} ran during [{}]".format(self.func_name, start_time - datetime.now()))

        return wrapper
