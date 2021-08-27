# -*- coding: utf-8 -*-
# Author : Seungyeon Jo
# e-mail : syjo@seculayer.co.kr
# Powered by Seculayer © 2018 AI-Core Team
######################################################################################
###### import modules ######
### python basic
from datetime import datetime

### MLPS
from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract

######################################################################################
# class : Implement com.seculayer.ape.cnvrtr.function.logic.Trim.java as Python
class Trim(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def apply(self, data):
        result = ''
        
        # check blank
        if self._isBlank(data) :
            return [result]
        
        try:
            ts = int(data)
            result = datetime.utcfromtimestamp(ts).strftime('%Y%m%d%H%M%S')
        except Exception as e:
            self.LOGGER.getLogger().error(e)
        
        return [result]


if __name__ == "__main__":
    str = "Hello World"
    print(Trim().apply(str))