# -*- coding: utf-8 -*-
# Author : Seungyeon Jo
# e-mail : syjo@seculayer.co.kr
# Powered by Seculayer © 2018 AI-Core Team

import hashlib

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class StringToMD5(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def apply(self, data):
        result = ''
        
        # check blank
        if self._isBlank(data) :
            return [result]
        
        result = self._strToMD5hash(data)
         
        return [result]

    def _strToMD5hash(self, _str):
        try:
            m = hashlib.md5()
            m.update(_str.encode('UTF-8'))
            return m.hexdigest()
        except Exception as e:
            self.LOGGER.error(e)
            return _str


if __name__ == "__main__":
    str = "Korea"
    print(StringToMD5().apply(str))
