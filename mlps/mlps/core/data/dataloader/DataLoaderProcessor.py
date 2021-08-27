# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import multiprocessing
from multiprocessing import Queue
from typing import List, Tuple, Union

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract
from mlps.core.data.cnvrtr.ConvertFactory import ConvertFactory
from mlps.common.Common import Common
from mlps.common.info.FieldInfo import FieldInfo
from mlps.common.utils.FileUtils import FileUtils
from mlps.common.utils.JSONUtils import JSONUtils


class DataLoaderProcessor(multiprocessing.Process):
    LOGGER = Common.LOGGER.getLogger()

    def __init__(self, data_queue: Queue, file_name: str, fields: List[FieldInfo], idx):
        multiprocessing.Process.__init__(self)
        self.is_terminate = False
        self.data_queue = data_queue
        self.file_name = file_name
        self.idx = idx
        self.fields: List[FieldInfo] = fields
        self.functions: List[List[ConvertAbstract]] = self.build_functions(fields)

    def run(self) -> None:
        self.LOGGER.info("DataLoader Process[{}] is starting...".format(self.idx))

        if self.file_name is not None:
            data = self._read()
            self.data_queue.put(data)

        self.LOGGER.info("DataLoader Process[{}] is terminate...".format(self.idx))
        self.LOGGER.info("Data Queue Length : {}".format(self.data_queue.qsize()))

    @staticmethod
    def build_functions(fields: List[FieldInfo]) -> List[List[ConvertAbstract]]:
        functions: List[List[ConvertAbstract]] = list()
        for field in fields:
            cvt_fn_list: List[ConvertAbstract] = list()
            for fn_info in field.get_function():
                cvt_fn_list.append(ConvertFactory.create_cvt_fn(fn_info))
            functions.append(cvt_fn_list)
        return functions

    def _read(self) -> List:
        self.LOGGER.info("read file : {}".format(self.file_name))
        features = list()
        labels = list()
        origin_data = list()
        f = None
        try:
            f = FileUtils.file_pointer(self.file_name, "r")
            for line in f.readlines():
                feature, label, data = self._convert(line)
                features.append(feature), labels.append(label), origin_data.append(data)
        except Exception as e:
            self.LOGGER.error(str(e), exc_info=True)
            raise NotImplementedError
        finally:
            if f is not None:
                f.close()

        return [features, labels, origin_data]

    def _convert(self, line) -> Tuple[list, list, dict]:
        features = list()
        labels = list()
        data = JSONUtils.ujson_load(line)
        for idx, field in enumerate(self.fields):
            if not field.multiple():
                name = field.field_name
                value = data.get(name, "")
            else:
                value = list()
                for name in field.field_name.split("@COMMA@"):
                    value.append(data.get(name, ""))
            cvt_data = list()
            # TODO : 한 필드에 2개의 함수가 있을 경우 잘 동작하는지 확인
            for fn in self.functions[idx]:
                cvt_data += fn.apply(value)
            if field.label():
                labels += cvt_data
            else:
                features += cvt_data
        return features, labels, data


class DataLoaderProcessorBuilder(object):
    def __init__(self):
        self.data_queue: Union[Queue, None] = None
        self.file_name: str = ""
        self.fields = list()
        self.idx: int = 0

    def set_data_queue(self, queue):
        self.data_queue = queue
        return self

    def set_filename(self, file_name: str):
        self.file_name = file_name
        return self

    def set_fields(self, fields):
        self.fields = fields
        return self

    def set_idx(self, idx):
        self.idx = idx
        return self

    def build(self) -> DataLoaderProcessor:
        return DataLoaderProcessor(self.data_queue, self.file_name, self.fields, self.idx)
