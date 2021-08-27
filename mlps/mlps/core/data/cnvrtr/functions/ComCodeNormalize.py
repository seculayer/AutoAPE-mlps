# -*- coding: utf-8 -*-
# Author : Seungyeon Jo
# e-mail : syjo@seculayer.co.kr
# Powered by Seculayer © 2018 AI-Core Team

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class ComCodeNormalize(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def apply(self, data):
        result = ''
        
        # check blank
        if self._isBlank(data) :
            return [result]
        
        # Not supported.
        
        return [result]


if __name__ == "__main__":
    _str = "KR"
    print(ComCodeNormalize(arg_list=["CS0022"]).apply(_str))
