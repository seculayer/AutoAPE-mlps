# -*- coding: utf-8 -*-
# Author : Seungyeon Jo
# e-mail : syjo@seculayer.co.kr
# Powered by Seculayer © 2018 AI-Core Team

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class IfNull(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.replace = self.arg_list[0]
        
    def apply(self, data):
        
        # check blank
        if self._isBlank(data) :
            return [self.replace]
        else:
            return [data]


if __name__ == "__main__":
    _str = ""
    print(IfNull(stat_dict=None, arg_list=["A"]).apply(_str))
