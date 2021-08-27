# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import requests as rq
from mlps.common.Singleton import Singleton


class RestManager(object, metaclass=Singleton):
    def __init__(self, url):
        self.url = url

    @staticmethod
    def get(url):
        response = rq.get(url)

        return response

    @staticmethod
    def post(url: str, data: dict) -> rq.Response:
        response = rq.post(url, json=data)

        return response

    @staticmethod
    def make_post_data(status: str, message: str) -> dict:
        return {
            "status": status,
            "message": message
        }
