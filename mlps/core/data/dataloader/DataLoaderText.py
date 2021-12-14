# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

from typing import List

from mlps.common.Constants import Constants
from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract
from mlps.core.data.dataloader.DataLoaderAbstract import DataLoaderAbstract


class DataLoaderText(DataLoaderAbstract):

    def __init__(self, job_info, sftp_client):
        super().__init__(job_info, sftp_client)

    def read(self, file_list, fields):
        functions: List[List[ConvertAbstract]] = self.build_functions(fields)
        self.LOGGER.info(functions)

        features = list()
        labels = list()
        origin_data = list()

        for file in file_list:
            self.LOGGER.info("read text file : {}".format(file))
            generator = self.sftp_client.load_json_oneline(
                            filename=file,
                            dataset_format=Constants.DATASET_FORMAT_TEXT
                        )
            while True:
                line: str = next(generator)
                if line == "#file_end#":
                    break
                feature, label, data = self._convert(line, fields, functions)

                features.append(feature), labels.append(label), origin_data.append(data)

        if Constants.DATAPROCESS_CVT_DATA:
            self.write_dp_result(features, labels, file_list[0])  # file_list[0] : for dataset path

        self.make_inout_units(features, labels)
        return [features, labels, origin_data]
