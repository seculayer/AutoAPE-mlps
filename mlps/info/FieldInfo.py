# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import re
from typing import List

from pycmmn.utils.StringUtil import StringUtil
from dataconverter.core.ConvertFunctionInfo import ConvertFunctionInfo, ConvertFunctionInfoBuilder


class FieldInfo(object):
    def __init__(self, field_dict: dict, metadata_dict: dict, project_target_field: str):
        self.field_sn = StringUtil.get_int(field_dict.get("field_sn", 0))
        self.field_name = field_dict.get("name", "")
        self.target_field = project_target_field
        self.stat_dict = field_dict.get("statistic", dict())
        self.field_type = field_dict.get("field_type")

        # self.is_label = StringUtil.get_boolean(field_dict.get("is_label", "N"))
        if self.target_field == self.field_name:
            self.is_label = True
        else:
            self.is_label = False
        # self.is_multiple = StringUtil.get_boolean(field_dict.get("is_multiple", "N"))
        self.is_multiple = True if len(self.field_name.split("@COMMA@")) >= 2 else False
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
