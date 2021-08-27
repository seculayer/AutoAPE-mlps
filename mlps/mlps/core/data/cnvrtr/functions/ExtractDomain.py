# -*- coding: utf-8 -*-
# Author : Seungyeon Jo
# e-mail : syjo@seculayer.co.kr
# Powered by Seculayer © 2018 AI-Core Team

import re
from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class ExtractDomain(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def apply(self, data):
        result = ''
        
        # check blank
        if self._isBlank(data) :
            return [result]
        
        # 0. Cut Parameter
        _regex = '(\\?.+)|([hHtTpPsS]{4,5}://)'
        cutDomain = re.sub(_regex, '', data)
        # 1. IP is return
        if len(re.sub('[0-9.]', '', cutDomain)) == 0:
            return [cutDomain]
        
        # 2. if domain is .com/.net
        arr = []
        arr_len = 0
        try:
            arr = cutDomain.split('.')
            arr_len = len(arr)
            if cutDomain.endswith('.com') or cutDomain.endswith('.net'):
                return [arr[arr_len-2] + "." + arr[arr_len-1]]
        except Exception as e:
            self.LOGGER.error(e)
         
        # 3. if .(dot) is one
        if arr_len == 2:
            return [cutDomain]
        
        # 4. if .(dot) is two
        try:
            if arr_len == 3:
                return [arr[arr_len-2] + "." + arr[arr_len-1]]
        except Exception as e:
            self.LOGGER.error(e)
        
        # 5. if .(dot) is three more
        try:
            if arr_len >= 4:
                return [arr[arr_len-3] + "." + arr[arr_len-2] + "." + arr[arr_len-1]]
        except Exception as e:
            self.LOGGER.error(e)
        
        return [cutDomain]


if __name__ == "__main__":
    _str = "http://www.seculayer.com/index.html?arg1=0"
    print(ExtractDomain(stat_dict=None, arg_list=None).apply(_str))
