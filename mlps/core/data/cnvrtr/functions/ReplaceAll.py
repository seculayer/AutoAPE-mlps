# -*- coding: utf-8 -*-
# Author : Seungyeon Jo
# e-mail : syjo@seculayer.co.kr
# Powered by Seculayer © 2018 AI-Core Team

import re

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class ReplaceAll(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def apply(self, data):
        result = ''
        
        # check blank
        if self._isBlank(data):
            return [result]
        
        strReg = ''
        strNew = ''
        if len(self.arg_list) >= 2:
            strReg = self.arg_list[0]
            strNew = self.arg_list[1]
        else:
            return [result]
                
        result = re.sub(strReg, strNew, data)
        
        return [result]


if __name__ == "__main__":
    _str = "Korea"
    print(ReplaceAll(arg_list=["[a-z]", ""]).apply(_str))
