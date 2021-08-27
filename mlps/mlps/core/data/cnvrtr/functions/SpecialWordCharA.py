# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : manki.baek@seculayer.com
# Powered by Seculayer © 2017-2018 AI Core Team, Intelligence R&D Center.

import re
import urllib.parse
import json

from mlps.common.Constants import Constants
from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class SpecialWordCharA(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_len = int(self.arg_list[0])
        self.preprocessing_type = str(self.arg_list[1])
        self.dec_op = int(self.arg_list[2])
        self.num_feat = self.max_len
        # self.FilterFunc = FilterFunc()

        with open(Constants.DIR_RESOURCES_CNVRTR + "/special_word_char_dict.json", "r") as f:
            self.special_word_dict = json.load(f)

        self.SWtoken_Arr = self.special_word_dict["SWtoken_Arr"]

        try:
            self.SWtoken = self.SWtoken_Arr[self.preprocessing_type]
        except:
            # print("################### No existed Attack Type")
            self.LOGGER.warn("No existed Attack Type")
            self.SWtoken = self.SWtoken_Arr["SQL"]

    def apply(self, data):
        try:
            # URL Decode
            data = data.replace("\\/", "/")
            _input = data

            if self.preprocessing_type == 'RCE':
                for rce in self.special_word_dict["SWupper_arr"]:
                    if rce[0] != " ":
                        _input = _input.replace(str(rce[0]), ' ' + str(rce[0]) + ' ')
                        _input = _input.replace("  ", " ")

            _input = _input.replace("#COMMA#", ",")
            _input = _input.replace("#CRLF#", " ")

            if self.dec_op == 1:
                try:
                    iLoopCnt = 0
                    val = ""
                    while val != _input or iLoopCnt <= 5:
                        val = _input
                        iLoopCnt += 1
                        _input = urllib.parse.unquote(_input.upper())
                    dec_data = _input.lower()
                except:
                    dec_data = str(_input).lower()
                # print(dec_data)
            else:
                dec_data = _input

            rep_data = re.sub(r'\s+', " ", dec_data)
            rep_data = re.sub(r'[\W_]', " \g<0> ", rep_data)
            # rep_data = re.sub(r'% [\d\w]{2}', " \g<0> ", rep_data)
            rep_data = re.sub(r' +', " ", rep_data)

            # rep_data = re.sub(r'% ', "%", rep_data)
            rep_data = re.sub(r'[^0-9a-zA-Z\W_]', "", rep_data)

            rep_data_list = rep_data.split(" ")
            # print(rep_data_list)
            result_list = list()

            # val_list = self.SWtoken.values()
            # max_val = max(val_list)

            for token in rep_data_list:
                try:
                    result_list.append(float(self.SWtoken[token]))
                except:
                    pass
            result_len = len(result_list)
            if result_len < self.max_len:
                padding = [0.] * (self.max_len - result_len)
                result_list.extend(padding)
                return result_list
            else:
                return result_list[:self.max_len]

        except Exception as e:
            # print(e)
            # self.LOGGER.error(e, exc_info=True)
            return [0.] * self.max_len

    def get_num_feat(self):
        return self.max_len


if __name__ == '__main__':
    # data = "hjg yjhg 6ug679t g6guy g321%!#% $^$Fgsdfha"
    _data = "adsfafeafeGET /postal/mobile/popup/comm_newzipcd_mobileweb.jsp? classloader form_nameZGlzcGF0Y2hlci5IdHRwU2VydmxldFJlcXVlc3Q=sendForm&zip_name=tReceiverZipcode1&areacd_name=%7Ccat%20%2Fetc%2Fservices&addr1_name=tReceiverAddr1&addr2_name=tReceiverAddr2&addr3_name= HTTP/1.0 Accept-Language: ko Host: m.epost.go.kr Cookie: PCID=15236078361977256000040; serviceGbn=null; JSESSIONID=FF6slK0TNgixI03d9pS1Wvsxl8VA8hqcXDVo0Irc4G3z3fILMbpraEYRVhpRhfN5.epost3_servlet_parcel; mdt=ios; PHAROS_VISITOR=000000000162c2d79b0e529c0ade2518; cookieSequence=01382387; postname=%40%40%40%40%40%40abc%40%40%40%40%40%40abc%40%40%40%40%40%40abc; myquery=SCANW3B%0D%0ASPLITTING%2F%EB%93%B1%EA%B8%B0%EC%A1%B0%ED%9A%8C%2F%EB%82%B4%EC%9A%A9%EC%A6%9D%EB%AA%85%2F%EC%9A%B0%ED%8E%B8%EB%B2%88%ED%98%B8%EA%B2%80%EC%83%89%2F%EC%95%8C%EB%9C%B0%ED%8F%B0%2F%EB%8C%80%EC%B2%9C%EA%B9%80%2F%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EB%8C%80%EC%B2%9C%EA%B9%80%2F%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EC%95%8C%EB%9C%B0%ED%8F%B0%2F%EB%8C%80%EC%B2%9C%EA%B9%80%2F%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%9A%94%EA%B8%88%2F%EC%9A%B0%ED%8E%B8%EC%|"

    from datetime import datetime
    start = datetime.now()
    cvt_fn = SpecialWordCharA(stat_dict=None, arg_list=[500, 'SQL', 1])  # 스테이트딕이 민맥스가 있을경우 넣어줘야함, 아규리스트가 4인데 원소를 4개로 잘라서 몇개만 쓸껀지

    for i in range(1000):
        rst = cvt_fn.apply(data=_data)
    end = datetime.now()

