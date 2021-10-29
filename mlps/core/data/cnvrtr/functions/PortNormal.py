# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : bmg8551@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class PortNormal(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max = 65535
        self.min = 0

    def apply(self, data):
        norm = self.max - self.min
        temp_result = None
        try:
            # Normalization
            temp_result = (float(data) - self.min) / norm
            # temp_result = float(data) / 65535
        except Exception as e:
            # print log for error
            self.LOGGER.error(str(e))

        # List return
        result = list()
        result.append(temp_result)
        return result


if __name__ == "__main__":
    port_num = '8080'
    port_normal = PortNormal()
    print(port_normal.apply(data = port_num))
