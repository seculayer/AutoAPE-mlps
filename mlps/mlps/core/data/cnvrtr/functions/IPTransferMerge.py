# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : bmg8551@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class IPTransferMerge(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.num_feat = 1

    # 토크나이징 하는곳
    def apply(self, data):
        try:
            data1 = data[0]
            data2 = data[1]

            row = data1 + "." + data2
            row = [row] * 6
        except Exception as e:
            # self.LOGGER.error(e)
            row = ["0", "0", "0", "0", "0", "0"]

        return row


if __name__ == "__main__":
    payload = ["192.168.1.110", "192.168.1.111"]
    tokenizer = IPTransferMerge(stat_dict=None, arg_list=None)
    print(tokenizer.apply(payload))

# | EqpDtTokenizer     | 장비 발생 시각에서 시간과 분을 추출한다.
# | DevUsage           | 장비의 사용률을 0~1 사이로 Normalize 한다.
# | IPTransferDivide   | ip 주소를 '.'으로 split하여 반환한다.
# | IPTransferMerge    | 두개의 ip 주소를 하나의 필드로 합한 문자열을 반환한다.
