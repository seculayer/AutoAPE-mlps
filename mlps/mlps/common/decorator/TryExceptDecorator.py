import traceback
from mlps.core.RestManager import RestManager


class TryExceptDecorator:
    def __init__(self, status, url):
        self.status = status
        self.url = url

    def __call__(self, func):
        def wrapper(arg1):
            try:
                func(arg1)
            except:
                message = RestManager.make_post_data(self.status, traceback.format_exc())
                RestManager.post(self.url, message)

        return wrapper
