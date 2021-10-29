# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : bmg8551@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class MergeURLResCode(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.num_feat = 1
        self.input_type = self.arg_list[0]

    def apply(self, data):

        try:
            # data = data.split(self.split_separator)
            # self.LOGGER.error("data?????? {}".format(data))
            data1 = None
            data2 = None
            data1_flag = 'str'
            data2_flag = 'str'
            try:
                data1 = int(data[0])
                data1_flag = 'int'
            except:
                data1 = data[0]
            try:
                data2 = int(data[1])
                data2_flag = 'int'
            except:
                data2 = data[1]

            res_code = None
            url = None

            if data2_flag == "int":
                url = data1
                res_code = data2

            else:
                res_code = data1
                url = data2

            if self.input_type == 0:
                url_split_list = url.split(" ")
                url = url_split_list[1]
            else:
                pass

            url = url.strip()
            url = url.split("?")[0]
            # url = url.replace(":", "_")

            # cutting_index = url.find("/")
            # url = url[cutting_index + 1:]

            result_str = str(res_code) + "|" + str(url)
            return [result_str]

        except Exception as e:

            self.LOGGER.error(e, exc_info=True)
            return ["#PADDING#|#PADDING#"] * self.num_feat


if __name__ == "__main__":
    payload_list =[
        ["200", "www.g2b.go.kr:8081/pt/menu/selectSubFrame.do"],
        ["200", "www.g2b.go.kr:8081/main"],
        ["200", "www.g2b.go.kr:8081/ingam/ingam.jsp"],
        ["200", "www.g2b.go.kr:8081/main"],
        ["200", "www.g2b.go.kr:8081/ep/invitation/publish/bidInfoDtl.do"],
        ["200", "www.g2b.go.kr:8081/inc/api.php"],
        ["200", "www.g2b.go.kr:8081/pt/e-support/fwdEsupportMain.do"],
    ]
    payload = ["200", "	www.g2b.go.kr:8081/pt/menu/selectSubFrame.do"]
    tokenizer = MergeURLResCode(stat_dict=None, arg_list=[1])
    for payload in payload_list:
        result = tokenizer.apply(payload)
        print(result)
        print(len(result))
