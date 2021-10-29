# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team, Intelligence R&D Center.

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class MinMaxNormal(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.max = float(self.stat_dict["max"])
            self.min = float(self.stat_dict["min"])
        except:
            self.max = 0
            self.min = 0

    def apply(self, data):
        norm = self.max - self.min
        temp_result = -1.0
        # zero-division protection
        if norm == 0:
            # self.LOGGER.warn("Min val is same Max val (Min val == Max val)")
            norm = 1
        try:
            # temp_result = float(data) / 255
            # temp_result = (float(data) - self.min) / (self.max - self.min)
            temp_result = (float(data) - self.min) / (norm)
        except Exception as e:
            # print log for error
            self.LOGGER.error("[MinMaxNormal] Convert error !!! self.min : {}, self.max : {}, data : {}".format(self.min, self.max, data))
            self.LOGGER.error(str(e))
        # List return
        result = list()
        result.append(temp_result)
        return result


if __name__ == '__main__':
    minmax_normalization = MinMaxNormal(
        stat_dict={"min": 0, "max": 255}, arg_list=None
    )
    ip = "192.168.2.236"
    ip_split = ip.split(".")

    for data in ip_split:
        print(minmax_normalization.apply(data=data))
