# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

from typing import List

from mlps.common.info.FieldInfo import FieldInfo


class DatasetInfo(object):
    def __init__(self, dataset_dict: dict):
        self.dataset_type = dataset_dict.get("dataset_type")
        self.file_lines = dataset_dict.get("dist_file_lines", list())
        self.statistic = dataset_dict.get("statistic", dict())
        self.fields = self.set_fields(dataset_dict.get("fields", list()), self.statistic)

    @staticmethod
    def set_fields(fields_dict_list, statistic):
        fields = list()
        for field_dict in fields_dict_list:
            field = FieldInfo(field_dict, statistic)
            fields.append(field)

        return fields

    def __str__(self) -> str:
        return "\ndataset_type : {},\n" \
               "file_lines : {}, \n" \
               "statistic : {}".format(self.dataset_type,
                                       self.file_lines,
                                       self.statistic)

    def get_max_lines(self, task_idx) -> int:
        return self.file_lines[task_idx]

    def get_fields(self) -> List[FieldInfo]:
        return self.fields

    def get_dist_lines(self) -> List[int]:
        return self.file_lines

    def get_statistic(self) -> dict:
        return self.statistic
