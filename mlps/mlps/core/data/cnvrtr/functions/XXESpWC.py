# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import json
from typing import Tuple

from mlps.common.Constants import Constants
from mlps.core.data.cnvrtr.functions.SpWCAbstract import SpWCAbstract


class XXESpWC(SpWCAbstract):
    @staticmethod
    def _load_special_word_dict() -> Tuple[dict, dict]:
        keyword_map_path = "{}/{}".format(Constants.DIR_RESOURCES_CNVRTR, "XXE_keywords_map.json")
        f = open(keyword_map_path, "r")
        data_dict = json.loads(f.read())
        special_dict = data_dict["special_keyword"]
        regex_dict = data_dict["special_regex"]
        f.close()
        return special_dict, regex_dict

    def processConvert(self, data):
        return self.apply(data)


if __name__ == '__main__':
    str_data = "/main/product/product_view.asp %00--%3E%3C/script%3E%3Cscript%3Ealert(313)%3C/script%3E?seq=87 Mozilla/5.0+(Windows+NT+6.1;+WOW64;+Trident/7.0;+rv:11.0)+like+Gecko"
    cvt_fn = XXESpWC(arg_list=[50, 255], stat_dict=dict())
    print(cvt_fn.apply(str_data))
    print("".join(cvt_fn.remove_common_word(str_data)))

