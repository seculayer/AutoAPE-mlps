# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : bmg8551@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class IPNormal(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max = 255
        self.min = 0
        self.num_feat = 4

    def apply(self, data):
        ip_split = data.split(".")
        if len(ip_split) != self.num_feat:
            return [0.0, 0.0, 0.0, 0.0]

        norm = self.max - self.min
        result = list()
        try:
            for ip in ip_split:
                # Normalization
                result.append((float(ip) - self.min) / norm)
                # result.append(float(ip) / 255)
        except Exception as e:
            # print log for error
            self.LOGGER.error(str(e))
            result = [0.0, 0.0, 0.0, 0.0]

        # List return
        return result


if __name__ == "__main__":
    ip_arr = "192.168.2.236"
    ipnormal = IPNormal()
    print(ipnormal.apply(ip_arr))
