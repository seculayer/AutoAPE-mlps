# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team, Intelligence R&D Center.

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class OneHotEncode(ConvertAbstract):
    def __init__(self, arg_list: list, stat_dict: dict):
        super().__init__(arg_list=arg_list, stat_dict=stat_dict)
        self.unique_dict: dict = dict()
        self.unique_count = 0

        for idx, key in enumerate(sorted(self.stat_dict.get("unique").keys())):
            self.unique_dict[key] = idx
            self.unique_count += 1

    def apply(self, data):
        # ZERO
        result = [0 for i in range(self.unique_count)]
        try:
            # GET INDEX
            index = self.unique_dict.get(data)
            result[index] = 1
        except Exception as e:
            # self.LOGGER.getLogger().warn(e)
            result[0] = 1

        # List return
        return result

    def get_num_feat(self):
        return self.unique_count


if __name__ == "__main__":
    one_hot_encode = OneHotEncode(
        stat_dict={"unique": "0@COMMA@1", "uniqueCount": 2}, arg_list=list()
    )

    print(one_hot_encode.apply("0"))
    print(one_hot_encode.apply("1"))
    print(one_hot_encode.apply("1"))
