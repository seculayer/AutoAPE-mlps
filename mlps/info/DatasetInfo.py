# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

from typing import List, Dict

from mlps.info.FieldInfo import FieldInfo


class DatasetInfo(object):
    def __init__(self, dataset_dict: dict, project_target_field: str):
        self.total_dist_file_cnt: int = int(dataset_dict.get("dist_file_cnt", "1"))
        self.metadata: List[Dict] = dataset_dict.get("metadata_json", {}).get("meta", [])
        self.data_analysis_json: List[Dict] = dataset_dict.get("fields", [])
        self.fields: List[FieldInfo] = self.set_fields(
            self.data_analysis_json,
            self.metadata,
            project_target_field
        )
        self.label_yn: str = dataset_dict.get("label_yn", "N")
        self.file_list: List[str] = dataset_dict.get("metadata_json", {}).get("file_list", [])

    @staticmethod
    def set_fields(data_analysis_json, metadata, project_target_field):
        fields = list()
        for field_dict in data_analysis_json:
            field_sn: int = int(field_dict.get("field_sn"))
            meta_dict = None
            try:
                meta_dict = metadata[field_sn]
            except IndexError:
                meta_dict = {}
            field = FieldInfo(field_dict, meta_dict, project_target_field)
            fields.append(field)

        return fields

    def get_fields(self) -> List[FieldInfo]:
        return self.fields

    # def get_dist_lines(self) -> List[int]:
    #     return self.file_lines
    #
    # def get_statistic(self) -> dict:
    #     return self.statistic
