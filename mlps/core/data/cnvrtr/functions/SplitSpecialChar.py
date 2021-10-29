# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : bmg8551@seculayer.co.kr
# Powered by Seculayer © 2017 AI-TF Team

import urllib.parse as decode
import re

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class SplitSpecialChar(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_len = int(self.arg_list[0])
        self.reg = re.compile("[~!#$%^&*|;,?/\n\r\s]")
        self.num_feat = self.max_len

    # 토크나이징 하는곳
    def apply(self, data):

        try:
            for _ in range(2):
                data = decode.unquote(data)
            row = data.lower()
            row = self.reg.split(row)
            row = list(filter(bool, row))

            result_len = len(row)
            # padding
            if result_len < self.max_len:
                padding = ['#PADDING#'] * (self.max_len - result_len)
                # padding = ['#PADDING#' for _ in range(self.max_len - result_len)]
                row.extend(padding)
            else:
                row = row[:self.max_len]

            return row
        except Exception as e:
            self.LOGGER.error(e)
            return ["#PADDING#"] * self.max_len

    def get_num_feat(self):
        return self.max_len


if __name__ == "__main__":
    payload = "GET\n/shop/ProdSearch.php?Ccode1=0&Ccode2=&Ccode3=&SearchType=All&word_blank=and&word=&width=5 HTTP/1.1#CRLF#Host: 1.1.1.1"
    tokenizer = SplitSpecialChar(stat_dict=None, arg_list=[20])
    print(tokenizer.apply(payload))
