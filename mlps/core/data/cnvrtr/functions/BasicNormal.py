# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : bmg8551@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class BasicNormal(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max = 32767
        self.min = 0

    def apply(self, data):
        norm = self.max - self.min
        if data == None:
            data = "0"
        data = data.replace(" ", "")

        v = 0
        # string이 문자로만 구성되어 있는지 확인
        if data.isalpha():
            alpha = "abcdefghijklmnopqrstuvwxyz"
            temp = data.lower()
            for idx in range(len(temp)):
                v += alpha.find(temp[idx])
        temp_result = ""
        try:
            temp_result = (float(v) - self.min) / norm
        except Exception as e:
            self.LOGGER.error(e)

        # List return
        result = list()
        result.append(temp_result)
        return result


if __name__ == "__main__":
    _str = "Hello World"
    basic_normal = BasicNormal()
    print(basic_normal.apply(_str))
