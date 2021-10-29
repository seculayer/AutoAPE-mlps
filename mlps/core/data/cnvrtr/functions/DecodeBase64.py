# -*- coding: utf-8 -*-
# Author : Seungyeon Jo
# e-mail : syjo@seculayer.co.kr
# Powered by Seculayer © 2018 AI-Core Team

import base64
from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class DecodeBase64(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def apply(self, data):
        result = ''
        
        # check blank
        if self._isBlank(data):
            return result
        
        # check string
        if isinstance(data, str):
            data = data.encode('UTF-8')
        
        try:
            result = base64.b64decode(data)
        except Exception as e:
            self.LOGGER.error(e)

        return result.decode('UTF-8')


if __name__ == "__main__":
    _str = "Hello World"
    str_encode = base64.b64encode(str.encode('UTF-8'))
    print(str_encode)
    print(DecodeBase64(stat_dict=None, arg_list=None).apply(str_encode))
