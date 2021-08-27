# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2017-2018 AI Core Team, Intelligence R&D Center. 

import re
import urllib.parse as decode

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class SpecialCharExtract(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_len = int(self.arg_list[0])
        self.num_feat = self.max_len

    def apply(self, data):
        # URL Decode
        try:
            data = data.replace("\\/", "/")
            dec_data = decode.unquote(data)
        except:
            dec_data = data

        # replace
        try:
            rep_data = re.findall(r'[\W_]', dec_data)
        except:
            rep_data = dec_data

        result = list()
        for i, ch in enumerate(rep_data):
            if i >= self.max_len:
                break
            try:
                result.append(float(ord(ch)))
            except:
                result.append(255.)

        result_len = len(result)
        # padding
        if result_len < self.max_len :
            padding = [255.]*(self.max_len - result_len)
            result.extend(padding)
            return result
        else:
            return result[:self.max_len]

    def get_num_feat(self):
        return self.max_len


if __name__ == '__main__':
    _data = "https://stackoverflow.com/questions/16566069/url-decode-utf-8-in-python白萬基"
    cvt_fn = SpecialCharExtract(stat_dict=None, arg_list=[1000])

    print(cvt_fn.apply(data=_data))
