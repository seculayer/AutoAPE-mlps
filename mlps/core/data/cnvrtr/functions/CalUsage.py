# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : bmg8551@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class CalDevUsage(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def apply(self, data):
        try:
            row = float(data) / 100
        except Exception as e:
            self.LOGGER.error(e)
            row = 0.0

        return [row]


if __name__ == "__main__":
    payload = "24.5753"
    tokenizer = CalDevUsage(stat_dict=None, arg_list=None)
    print(tokenizer.apply(payload))
