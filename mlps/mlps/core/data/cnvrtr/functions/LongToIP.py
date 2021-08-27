# -*- coding: utf-8 -*-
# Author : Seungyeon Jo
# e-mail : syjo@seculayer.co.kr
# Powered by Seculayer © 2018 AI-Core Team

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class LongToIP(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def apply(self, data):
        result = 0
        
        try:
            result = self._longToIp(data)
        except Exception as e:
            self.LOGGER.error(e)
        
        return [result]

    def _longToIp(self, ipint):
        return '.'.join([str(ipint >> (i << 3) & 0xFF) for i in range(4)[::-1]])


if __name__ == "__main__":
    _ipint = 16909060  # 1.2.3.4
    print(LongToIP(stat_dict=None, arg_list=[]).apply(_ipint))
