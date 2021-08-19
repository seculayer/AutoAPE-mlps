# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

from typing import Tuple, List
import re


class ConvertFunctionInfo(object):
    def __init__(self, fn_str, fn_args: list, stat_dict: dict):
        self.fn_str = fn_str
        self.fn_args = fn_args
        self.stat_dict = stat_dict

    def __str__(self):
        return "\nfunction tag : {}" \
               "\nfunction args : {}" \
               "\nstatistics : {}".format(self.fn_str,
                                          self.fn_args, self.stat_dict)

    def get_fn_str(self):
        return self.fn_str

    def get_fn_args(self):
        return self.fn_args

    def get_stat_dict(self):
        return self.stat_dict


class ConvertFunctionInfoBuilder(object):
    _REGEX_FN_PARSE = "\\[\\[@([\\w\\d_]+)\\(([^\\]*]*)\\)\\]\\]"
    _PATTERN_REGEX_FN_PARSE = re.compile(_REGEX_FN_PARSE)

    def __init__(self):
        self.fn_str = "[[@not_normal()]]"
        self.stat_dict = dict()

    def set_fn_str(self, fn_str):
        self.fn_str = fn_str
        return self

    def set_stat_dict(self, stat_dict):
        self.stat_dict = stat_dict
        return self

    def _parse_fn_name_params(self) -> Tuple[str, List[str]]:
        try:
            parsed = self._PATTERN_REGEX_FN_PARSE.match(self.fn_str).groups()
            args = parsed[1].replace("\'", "").split(",")
            return parsed[0], args
        except AttributeError as e:
            return "not_normal", list()

    def build(self) -> ConvertFunctionInfo:
        fn_name, fn_args = self._parse_fn_name_params()
        return ConvertFunctionInfo(fn_name, fn_args, self.stat_dict)


if __name__ == '__main__':
    ConvertFunctionInfoBuilder() \
        .set_fn_str("[[@ngram_tokenizer('100','3','1')]]") \
        .build()
