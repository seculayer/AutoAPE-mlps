# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import re
from typing import List

from mlps.common.utils.StringUtil import StringUtil
from mlps.common.info.ConvertFunctionInfo import ConvertFunctionInfo
from mlps.common.info.ConvertFunctionInfo import ConvertFunctionInfoBuilder


class FieldInfo(object):
    def __init__(self, field_dict: dict, stat_dict: dict):
        self.field_sn = StringUtil.get_int(field_dict.get("field_sn", 0))
        self.field_name = field_dict.get("name", "")
        self.stat_dict = stat_dict.get(self.field_name, dict())

        self.statistic = StringUtil.get_boolean(field_dict.get("stt_label", "N"))
        self.variance = StringUtil.get_boolean(field_dict.get("dispersion", "N"))
        self.unique = StringUtil.get_boolean(field_dict.get("unique_yn", "N"))
        self.max_length = StringUtil.get_boolean(field_dict.get("max_length", "N"))
        self.is_label = StringUtil.get_boolean(field_dict.get("is_label", "N"))
        self.is_multiple = StringUtil.get_boolean(field_dict.get("is_multiple", "N"))
        self.function: List[ConvertFunctionInfo] = self._create_functions(field_dict.get("functions", ""))

    def __str__(self) -> str:
        return "name : {}".format(self.field_name)

    def label(self) -> bool:
        return self.is_label

    def multiple(self) -> bool:
        return self.is_multiple

    # --- static variables
    _REGEX_FN_STR = "(\\[\\[@[\\w\\d_]+\\([^\\]]*\\)\\]\\])"
    _PATTERN_REGEX_FN_STR = re.compile(_REGEX_FN_STR)

    @classmethod
    def _get_function_str_list(cls, functions) -> List[str]:
        return cls._PATTERN_REGEX_FN_STR.findall(functions)

    def _create_functions(self, full_fn_str: str) -> List[ConvertFunctionInfo]:
        functions: List[ConvertFunctionInfo] = list()
        for fn_str in self._get_function_str_list(full_fn_str):
            fn_info = ConvertFunctionInfoBuilder() \
                .set_fn_str(fn_str) \
                .set_stat_dict(self.stat_dict) \
                .build()
            functions.append(fn_info)
        return functions

    def get_function(self) -> List[ConvertFunctionInfo]:
        return self.function

    def get_field_name(self) -> str:
        return self.field_name
