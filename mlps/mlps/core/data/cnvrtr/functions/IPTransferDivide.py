# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : bmg8551@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class IPTransferDivide(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.num_feat = 4

    # 토크나이징 하는곳
    def apply(self, data):
        try:
            row = data.split(".")
        except Exception as e:
            # self.LOGGER.error(e)
            row = ["0", "0", "0", "0"]

        return row


if __name__ == "__main__":
    payload = "192.168.1.110"
    tokenizer = IPTransferDivide(stat_dict=None, arg_list=None)
    print(tokenizer.apply(payload))
