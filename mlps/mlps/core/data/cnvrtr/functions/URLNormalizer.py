# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.

from typing import Tuple, List

from mlps.core.data.cnvrtr.functions.SpWCAbstract import SpWCAbstract


class URLNormalizer(SpWCAbstract):
    TOKEN_LIST = ['=', ':', '/', '+', '-', '%', '&', '?', '(', ')',
                  '!', ';', '*', "'", ",", "<", ">"]

    def __init__(self, **kwargs):
        """
        :param kwargs:
        ConvertAbstract(arg_list, stat_dict)
        kwargs["arg_list"], kwarg["stat_dict"]

        arg_list[0] = max length

        must
        """
        super().__init__(**kwargs)
        self.num_feat = 1

    @staticmethod
    def _load_special_word_dict() -> Tuple[dict, dict]:
        return dict(), dict()

    def apply(self, data) -> List:
        data = self._replace_basic(data)
        data = self._url_decode(data)
        data = self._tokenize(data)
        return [data]

    @staticmethod
    def _tokenize(data: str) -> str:
        for token in URLNormalizer.TOKEN_LIST:
            data = data.replace(str(token), ' ' + str(token) + ' ').replace("  ", " ")
        data = data.strip()
        return data

    def _convert_value(self, data):
        result = list()
        for word in data:
            result.append(word)
        return result

    def processConvert(self, data):
        return self.apply(data)

    def get_num_feat(self):
        return self.num_feat


if __name__ == '__main__':
    test_data = "https://test.seculayer.com/url.ext?key=value&key2=value"
    url_norm = URLNormalizer(arg_list=[], stat_dict=dict())
    print(url_norm.apply(test_data))
