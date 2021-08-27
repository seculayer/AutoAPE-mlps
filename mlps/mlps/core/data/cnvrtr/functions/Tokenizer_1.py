# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : bmg8551@seculayer.co.kr
# Powered by Seculayer © 2017 AI-TF Team

import urllib.parse as decode
import re

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class Tokenizer_1(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_len = int(self.arg_list[0])
        self.num_feat = self.max_len

    # 토크나이징 하는곳
    def apply(self, data):

        # URL Decode
        try:
            data = data.replace("\r\n", " ").replace("\n", " ").replace("\t", " ").replace("  ", " ").replace("  ", " ")

            _input = data
            _input = _input.replace("CCOMMAA", ",")

            try:
                iLoopCnt = 0
                val = ""
                while val != _input or iLoopCnt <= 5:
                    val = _input
                    iLoopCnt += 1
                    _input = decode.unquote(_input.upper())
                dec_data = _input.lower()
            except:
                dec_data = str(_input).lower()
        except:
            dec_data = data
            if dec_data == None:
                dec_data = ""

        rep_data = dec_data.replace('#CRLF#', '')  # CRLF가 붙어 올 경우 삭제
        rep_data = re.sub(r'\s+', " ", re.sub(r'[\W_]', " \g<0> ", re.sub(r'[^0-9a-zA-Z\W_]', "", rep_data)))

        result = rep_data.split(" ")
        result_len = len(result)

        # padding
        if result_len < self.max_len:
            padding = ['#PADDING#'] * (self.max_len - result_len)
            # padding = ['#PADDING#' for _ in range(self.max_len - result_len)]
            result.extend(padding)
        else:
            result = result[:self.max_len]
            # print(len(result))

        # print(result)
        return result

    def get_num_feat(self):
        return self.max_len


if __name__ == "__main__":
    payload = "GET /shop/ProdSearch.php?Ccode1=0&Ccode2=&Ccode3=&SrpriceS=&SrpriceE=&SearchType=All&word_blank=and&word=&width=5&height=16&orderType=high&BrandID=&page=14&Ccode4=%20AND%201=1 HTTP/1.1#CRLF#Host: 222.239.87.76#CRLF#"
    tokenizer = Tokenizer_1(stat_dict=None, arg_list=[20])
    print(tokenizer.apply(payload))
