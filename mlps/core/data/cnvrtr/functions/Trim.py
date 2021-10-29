# -*- coding: utf-8 -*-
# Author : Seungyeon Jo
# e-mail : syjo@seculayer.co.kr
# Powered by Seculayer © 2018 AI-Core Team

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class Trim(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def apply(self, data):
        result = ''
        
        # check blank
        if self._isBlank(data) :
            return [result]
        
        return [data.strip()]


if __name__ == "__main__":
    _str = " Aeye-2.0 "
    print(Trim(arg_list=None, stat_dict=None).apply(_str))
