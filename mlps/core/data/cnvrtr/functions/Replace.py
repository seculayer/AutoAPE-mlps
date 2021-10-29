# -*- coding: utf-8 -*-
# Author : Seungyeon Jo
# e-mail : syjo@seculayer.co.kr
# Powered by Seculayer © 2018 AI-Core Team

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class Replace(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def apply(self, data):
        result = ''
        
        # check blank
        if self._isBlank(data):
            return [result]
        
        strOld = ''
        strNew = ''
        if len(self.arg_list) >= 2 :
            strOld = self.arg_list[0]
            strNew = self.arg_list[1]
        else:
            return [result]
                
        result = data.replace(strOld, strNew)
        
        return [result]


if __name__ == "__main__":
    _str = "Korea"
    print(Replace(stat_dict=None, arg_list=["K", "C"]).apply(_str))
