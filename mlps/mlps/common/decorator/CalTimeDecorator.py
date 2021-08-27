from datetime import datetime
import logging


class CalTimeDecorator:
    LOGGER = logging.getLogger()

    def __init__(self, module_name):
        self.module_name = module_name

    def __call__(self, func):
        def wrapper():
            start_time = datetime.now()
            func()
            self.LOGGER.info("{} ran during [{}]".format(self.module_name, start_time - datetime.now()))

        return wrapper
