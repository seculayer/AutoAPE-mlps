# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team

from mlps.common.Common import Common


class ConvertAbstract(object):
    LOGGER = Common.LOGGER.getLogger()

    def __init__(self, arg_list: list, stat_dict: dict):
        self.num_feat = 1

        self.stat_dict = stat_dict
        self.arg_list = arg_list

        self.split_separator = ","
        self.max_len = 50
        self.padding_val = 255
        self.error_log_flag = False

    def processConvert(self, data):
        raise NotImplementedError

    def apply(self, data):
        arr_ret = list()

        try:
            arr_ret = self.processConvert(data=data)
            if -1 == self.max_len:
                return arr_ret

            if 1 == self.num_feat:
                self.num_feat = self.max_len

            res_val_lenth = len(arr_ret)

            if res_val_lenth < self.max_len:
                padding = [self.padding_val] * (self.max_len - res_val_lenth)
                arr_ret.extend(padding)
                return arr_ret

            return arr_ret[:self.max_len]

        except Exception as e:
            self.LOGGER.error("cvt Exception: {}".format(e))

        return arr_ret

    def get_num_feat(self):
        return self.num_feat

    @staticmethod
    def _isBlank(_str):
        return not (_str and _str.strip())
