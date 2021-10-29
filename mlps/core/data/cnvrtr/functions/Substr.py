# -*- coding: utf-8 -*-
# Author : Seungyeon Jo
# e-mail : syjo@seculayer.co.kr
# Powered by Seculayer © 2018 AI-Core Team

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class Substr(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def apply(self, data):
        result = ''
        
        # check blank
        if self._isBlank(data) :
            return [result]
        
        s_idx = 0
        e_idx = 0
        if len(self.arg_list) >= 2 :
            s_idx = int(self.arg_list[0])
            e_idx = int(self.arg_list[1])
        else:
            return [result]
        
        if s_idx > len(data):
            s_idx = 0
        if e_idx > len(data):
            e_idx = len(data)
        
        if e_idx == 0:
            result = data[s_idx:]
        else:
            result = data[s_idx:e_idx]
        
        return [result]


if __name__ == "__main__":
    _str = "Korea"
    print(Substr(arg_list=[0, 1]).apply(_str))
