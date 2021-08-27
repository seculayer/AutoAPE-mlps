# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : bmg8551@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class RefererInfo(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.num_feat = 1

    def apply(self, data):

        try:

            referer = data.strip()
            referer = referer.split("?")[0]
            referer = referer.replace(":", "_")

            return [referer]

        except:
            return ["#PADDING#"] * self.num_feat


if __name__ == "__main__":
    payload_list = [
        "www.g2b.go.kr:8081/gov/koneps/co.css/base.css"
    ]
    # payload = ["www.g2b.go.kr:8081/pt/menu/selectSubFrame.do"]
    tokenizer = RefererInfo(stat_dict=None, arg_list=[1])
    for payload in payload_list:
        result = tokenizer.apply(payload)
        print(result)
        print(len(result))
