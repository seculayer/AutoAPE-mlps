# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : bmg8551@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class MergeField_KTDS(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.num_feat = 1
        self.input_type = self.arg_list[0]

    def apply(self, data):
        try:
            if len(data) == 5:

                result = data[0].lower() + data[1].lower() + "∥" + data[2].lower() + "∥" + data[3].lower() + "∥" + data[4].lower()
            else:
                self.LOGGER.error("[MergeField_KTDS] input data error !!! len(data) : {}, data : {}".format(len(data),data))
                result = ""

            return [result]

        except Exception as e:
            self.LOGGER.error("[MergeField_KTDS] Convert error !!! len(data) : {}, data : {}".format(len(data),data))
            self.LOGGER.error(e, exc_info=True)
            return ["|PADDING#" * 5]


if __name__ == "__main__":
    _data = ["hoSt_domain", "url", "url2", "referer", "browser_type"]
    print(_data)
    print(list(map(str.lower, _data)))
    # print(MergeField_KTDS.apply(data))

