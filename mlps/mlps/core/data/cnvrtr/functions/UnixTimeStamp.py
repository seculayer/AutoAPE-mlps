# -*- coding: utf-8 -*-
# Author : Seungyeon Jo
# e-mail : syjo@seculayer.co.kr
# Powered by Seculayer © 2018 AI-Core Team
from datetime import datetime
from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class UnixTimeStamp(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def apply(self, data):
        result = ''
        
        # check blank
        if self._isBlank(data):
            return [result]
        
        try:
            ts = int(data)
            result = datetime.utcfromtimestamp(ts).strftime('%Y%m%d%H%M%S')
        except Exception as e:
            self.LOGGER.getLogger().error(e)
        
        return [result]


if __name__ == "__main__":
    _str = "Hello World"
    print(UnixTimeStamp().apply(_str))
