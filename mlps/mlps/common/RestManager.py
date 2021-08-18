# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import requests as rq
from pycmmn.common.Singleton import Singleton


class RestManager(object, metaclass=Singleton):
    def __init__(self, url):
        self.response = None
        self.url = url

    def rest_init(self):
        self.response = rq.get(self.url)

    def post(self, data) -> rq.Response:
        response = rq.post(self.url, data=data)

        return response

