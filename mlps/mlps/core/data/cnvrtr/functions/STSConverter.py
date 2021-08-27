# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2017-2018 AI Core Team, Intelligence R&D Center.

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class STSConverter(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.num_feat = 1

    def apply(self, data):
        result = list()
        try:
            res_str = data[0]
            for _data in data[1:]:
                res_str += "|" + _data
            result.append(res_str)

        except Exception as e:
            self.LOGGER.error(e)

        return result


if __name__ == "__main__":
    data = ["192.168.1.1", "192.168.2.1", "8080", "tcp"]
    not_nor = STSConverter(stat_dict=None, arg_list=None)
    _str = not_nor.apply(data=data)
    print(_str)
