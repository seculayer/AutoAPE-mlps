from datetime import datetime
from functools import wraps
from mlps.common.Common import Common


class CalTimeDecorator:
    LOGGER = Common.LOGGER.getLogger()

    def __init__(self, func_name):
        self.func_name = func_name

    def __call__(self, func):
        @wraps(func)
        def wrapper(_self, *args, **kwargs):
            start_time = datetime.now()
            func(_self, *args, **kwargs)
            self.LOGGER.info("{} ran during [{}]".format(self.func_name, datetime.now() - start_time))

        return wrapper
