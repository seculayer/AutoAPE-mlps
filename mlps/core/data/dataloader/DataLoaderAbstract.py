# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

from typing import Tuple, List
import numpy as np
import json

from mlps.common.Common import Common
from mlps.common.info.FieldInfo import FieldInfo
from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract
from mlps.core.data.cnvrtr.ConvertFactory import ConvertFactory


class DataLoaderAbstract(object):

    def __init__(self, job_info, sftp_client):
        self.LOGGER = Common.LOGGER.getLogger()
        self.job_info = job_info
        self.sftp_client = sftp_client

    @staticmethod
    def _convert(line, fields, functions) -> Tuple[list, list, dict]:
        features = list()
        labels = list()

        for idx, field in enumerate(fields):
            if True:  # not field.multiple():
                name = field.field_name
                value = line.get(name, "")
            # else:
            #     value = list()
            #     for name in field.field_name.split("@COMMA@"):
            #         value.append(line.get(name, ""))
            cvt_data = list()
            # TODO : 한 필드에 2개의 함수가 있을 경우 잘 동작하는지 확인
            for fn in functions[idx]:
                value = fn.apply(value)
            if field.label():
                labels += value
            else:
                if name == "image":
                    features = value[0]
                else:
                    features += value
        return features, labels, line

    @staticmethod
    def build_functions(fields: List[FieldInfo]) -> List[List[ConvertAbstract]]:
        functions: List[List[ConvertAbstract]] = list()
        for field in fields:
            cvt_fn_list: List[ConvertAbstract] = list()
            for fn_info in field.get_function():
                cvt_fn_list.append(ConvertFactory.create_cvt_fn(fn_info))
            functions.append(cvt_fn_list)
        return functions

    def make_inout_units(self, features, labels):
        input_units = np.shape(features)[1:]
        output_units = np.shape(labels)[-1]
        self.job_info.set_input_units(input_units)
        self.job_info.set_output_units(output_units)
        self.LOGGER.info("input_units : {}".format(input_units))
        self.LOGGER.info("output_units : {}".format(output_units))

    def write_dp_result(self, features, labels, file_path):
        rst_dict = dict()
        save_path = file_path.rsplit('/', 2)[0]

        self.LOGGER.info("features[0]: {}".format(features[0]))
        self.LOGGER.info("labels[0]: {}".format(labels[0]))

        rst_dict['features'] = features
        rst_dict['targets'] = labels

        f = self.sftp_client.get_client().open(
            f"{save_path}/{self.job_info.get_hist_no()}_{self.job_info.get_task_idx()}.dp",
            'w'
        )

        try:
            f.write(json.dumps(rst_dict, indent=2))
        except Exception as e:
            self.LOGGER.error(e, exc_info=True)
        finally:
            f.close()

    def read(self, file_list: List[str], fields: List[FieldInfo]) -> List:
        raise NotImplementedError

