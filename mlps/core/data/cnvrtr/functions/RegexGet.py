# -*- coding: utf-8 -*-
# Author : Seungyeon Jo
# e-mail : syjo@seculayer.co.kr
# Powered by Seculayer © 2018 AI-Core Team

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract
import re


class RegexGet(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reg = re.compile(self.arg_list[0])
        
    def apply(self, data):
        result = ''
        
        # check blank
        if self._isBlank(data):
            return [result]
        
        try:
            result = self.reg.match(data).groups()
            if len(result) > 0:
                result = result[0]
        except Exception as e:
            self.LOGGER.error(str(e))
            result = ''
        
        return [result]


if __name__ == "__main__":
    _str = "prefix_123_suffix"
    print(RegexGet(arg_list=["[a-z]+_(\\d+)_[a-z]+"]).apply(_str))
