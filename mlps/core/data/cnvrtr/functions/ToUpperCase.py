# -*- coding: utf-8 -*-
# Author : Seungyeon Jo
# e-mail : syjo@seculayer.co.kr
# Powered by Seculayer © 2018 AI-Core Team
######################################################################################
###### import modules ######
### python basic

### MLPS
from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract

######################################################################################
# class : Implement com.seculayer.ape.cnvrtr.function.logic.ToUpperCase.java as Python
class ToUpperCase(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def apply(self, data):
        result = ''
        
        # check blank
        if self._isBlank(data) :
            return [result]
        
        return [data.upper()]


if __name__ == "__main__":
    str = "Seculayer"
    print(ToUpperCase(stat_dict=None, arg_list=[]).apply(str))