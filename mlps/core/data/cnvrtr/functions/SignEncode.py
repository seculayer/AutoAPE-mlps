# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : bmg8551@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class SignEncode(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max = 1
        self.min = 0

    def apply(self, data):
        if data != self.min and data !=self.max:
            self.LOGGER.error("invalid input value")
            return [None]

        if data == 0:
            result = -1
        else:
            result = 1

        return [result]
