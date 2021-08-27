# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : bmg8551@seculayer.co.kr
# Powered by Seculayer © 2017 AI-TF Team

import json
import re

from mlps.common.Constants import Constants
from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract
from mlps.common.utils.FileUtils import FileUtils


class URLToRegex(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # input data dimension
        self.num_feat = 1
        f = None
        total_dict = None

        try:
            f = FileUtils.file_pointer(Constants.DIR_RESOURCES_CNVRTR + "/web_access_dic.json", "r")
            total_dict = json.load(f)

            self.exclude_list = total_dict["exclude_list"]
            self.pattern_list = total_dict["pattern_list"]

        except Exception as e:
            self.LOGGER.error(e, exc_info=True)
        finally:
            f.close()

    def apply(self, data, reuse=False):
        result_list = list()
        result = data
        # pattern translation
        for pattern in self.pattern_list[:-1]:
            result = re.sub(pattern=pattern[0], repl=pattern[1], string=result)

        # exclude data in parameter -> pass
        # not in parameter -> apply regex that is last of pattern list
        split_uri_parameter = result.split("?")
        if len(split_uri_parameter) >= 2:
            exclude_flag = False
            parameter = split_uri_parameter[1]
            for exclude in self.exclude_list:
                if exclude in parameter:
                    exclude_flag = True
                else:
                    pass
            if exclude_flag == False:
                result = re.sub(pattern=self.pattern_list[-1][0], repl=self.pattern_list[-1][1], string=result)
            else:
                pass
        else:
            result = re.sub(pattern=self.pattern_list[-1][0], repl=self.pattern_list[-1][1], string=result)

        result_list.append(result)
        return result_list


if __name__ == '__main__':
    url_list = [
        "http://www.abc.com/abe/index.html/",
        "http://www.abc.com/abe/index.html",
        "http://www.abc.com/abe/index.html?param1=val1&param2=val2",
        "https://search.shopping.naver.com/search/category.nhn?cat_id=50000784",
        "www.insiderhk.com/Acoustic/?idx=572&NaPm=ct%3Dk3pdq53k%7Cci%3D96e38693f734d92ac75ac6d9259d6243467ad6a8%7Ctr%3Dsls%7Csn%3D933270%7Chk%3D76a97cf7cad00ca1785f2d5933edf5d061ba4aa0",
        "www.insiderhk.com/Acoustic/?idx=572&str=select+*+from+table",
        "www.insiderhk.com/Acoustic/?idx=572&str=1=1",
        "/search.shopping.naver.com/search/all.nhn?query=asdf+asd&cat_id=&frm=NVSHATC",
        "https://search.shopping.naver.com/search/all.nhn?query=asdf+asd&cat_id=&frm=NVSHATC&password=1234",
    ]

    temp_cls = URLToRegex(stat_dict=None, arg_list=[])
    for url in url_list:
        _result = temp_cls.apply(url)
        print(_result)
