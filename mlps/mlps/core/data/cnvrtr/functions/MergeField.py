# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : bmg8551@seculayer.co.kr
# Powered by Seculayer © 2017 AI-TF Team

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class MergeField(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.num_feat = 1
        self.seperator: str = self.arg_list[0]
        if self.seperator == "" or self.seperator is None:
            # default value
            self.seperator = " "

    def apply(self, data):
        len_data = len(data)
        try:
            data = list(map(str.lower, data))
            result = self.seperator.join(data)

            return [result]

        except Exception as e:

            self.LOGGER.error(e, exc_info=True)

            result = ["#PADDING#"] * len_data
            return [self.seperator.join(result)]


if __name__ == "__main__":
    payload_list = [
        ["200", "www.g2b.go.kr:8081/pt/menu/selectSubFrame.do"],
        ["200", "www.g2b.go.kr:8081/main"],
        ["200", "www.g2b.go.kr:8081/ingam/ingam.jsp"],
        ["200", "www.g2b.go.kr:8081/main"],
        ["200", "www.g2b.go.kr:8081/ep/invitation/publish/bidInfoDtl.do"],
        ["200", "www.g2b.go.kr:8081/inc/api.php"],
        ["200", "www.g2b.go.kr:8081/pt/e-support/fwdEsupportMain.do"],
    ]
    # payload = ["200", "	www.g2b.go.kr:8081/pt/menu/selectSubFrame.do"]
    tokenizer = MergeField(stat_dict=None, arg_list=["@"])
    for payload in payload_list:
        rst = tokenizer.apply(payload)
        print(rst)
        print(len(rst))
