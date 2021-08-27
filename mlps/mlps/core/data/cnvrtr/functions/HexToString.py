# -*- coding: utf-8 -*-
# Author : Seungyeon Jo
# e-mail : syjo@seculayer.co.kr
# Powered by Seculayer © 2018 AI-Core Team

import binascii

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class HexToString(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.charSet = self.arg_list[0]
        
    def apply(self, data):
        # check blank
        result = ''
        if self._isBlank(data):
            return [result]
        
        # init charset
        if self._isBlank(self.charSet):
            self.charSet = 'UTF-8'
            
        # check string
        if type(data) == type(''):
            data = data.encode(self.charSet)
            
        try:
            result = binascii.unhexlify(data)
            result = result.decode(self.charSet)
        except Exception as e:
            self.LOGGER.error(e)
        
        return [result]


if __name__ == "__main__":
    _str = "68656c6c6f"  # hello to hex
    print(HexToString(stat_dict=None, arg_list=["UTF-8"]).apply(_str))
