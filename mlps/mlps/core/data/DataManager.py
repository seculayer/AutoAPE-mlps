# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import threading
import os
from multiprocessing import Queue
from queue import Queue as nQ
from typing import List
import traceback

from mlps.common.Singleton import Singleton
from mlps.common.info.JobInfo import JobInfo
from mlps.common.info.FieldInfo import FieldInfo

from mlps.common.Common import Common
from mlps.common.Constants import Constants
from mlps.core.data.dataloader.DataLoaderProcessor import DataLoaderProcessor, DataLoaderProcessorBuilder
from mlps.core.data.sampling.DataSampler import DataSampler
from mlps.core.RestManager import RestManager
from mlps.common.decorator.CalTimeDecorator import CalTimeDecorator
from mlps.common.info.DatasetInfo import DatasetInfo


class DataManager(threading.Thread, metaclass=Singleton):

    def __init__(self, job_info: JobInfo) -> None:
        threading.Thread.__init__(self)
        self.LOGGER = Common.LOGGER.getLogger()
        self.job_info: JobInfo = job_info
        self.data_queue: Queue = Queue()
        self.DataSampler = DataSampler(self.job_info)

        self.dataset_info: DatasetInfo = self.job_info.get_dataset_info()
        self.dataset = {}

    @CalTimeDecorator("Data Manager")
    def run(self) -> None:
        try:
            self.LOGGER.info("DataManager Start.")
            # RestManager.update_status_cd(Constants.STATUS_DATA_CONVERTING, self.job_info.get_key(),
            #                              self.job_info.get_task_idx(), '-')

            # ---- data load
            data_list = self.read_files(Constants.DIR_LEARN_FEAT, self.dataset_info.get_fields())

            self.DataSampler.set_data(data_list)
            self.dataset = self.DataSampler.sampling()

            self.LOGGER.info("DataManager End.")
        except Exception as e:
            self.LOGGER.error(e, exc_info=True)
            # RestManager.update_status_cd(Constants.STATUS_DATA_CONVERT_ERROR, self.job_info.get_key(),
            #                              self.job_info.get_task_idx(), traceback.format_exc())
            raise e

    def read_files(self, features_dir: str, fields: List[FieldInfo]) \
            -> List:
        # ---- prepare
        info = [self.job_info.get_hist_no(), self.job_info.get_task_idx()]
        file_list = self.get_feature_files(directory=features_dir, info=info)

        data_list = self.read_subproc(file_list, fields)

        return data_list

    def read_subproc(self, file_list: List[str], fields: List[FieldInfo]) \
            -> List:
        len_files = len(file_list)
        complete_cnt = 0
        proc_queue: nQ[DataLoaderProcessor] = nQ()

        features = list()
        labels = list()
        raw_data = list()

        # sub process create
        for idx, file_name in enumerate(file_list):
            proc_queue.put(self._create_proc(file_name, fields, idx))

        # sub process execute
        while complete_cnt < len_files:
            tmp_proc_list = list()
            tmp_comp_cnt = 0
            for _ in range(Constants.MAX_SUB_PROCESS):
                if proc_queue.qsize() > 0:
                    sub_proc = proc_queue.get()
                    sub_proc.start()
                    tmp_proc_list.append(sub_proc)

            while tmp_comp_cnt < len(tmp_proc_list):
                tmp_dataset = self.data_queue.get()
                features += tmp_dataset[0]
                labels += tmp_dataset[1]
                raw_data += tmp_dataset[2]
                tmp_comp_cnt += 1

            for sub_proc in tmp_proc_list:
                sub_proc.join()
                complete_cnt += 1

        return [features, labels, raw_data]

    def _create_proc(self, file_name: str, fields: List[FieldInfo], idx: int) -> DataLoaderProcessor:
        return DataLoaderProcessorBuilder() \
            .set_data_queue(self.data_queue) \
            .set_filename(file_name) \
            .set_fields(fields) \
            .set_idx(idx) \
            .build()

    def get_feature_files(self, directory="./", sep="_", info=None, ext=".done") -> List[str]:
        file_list = os.listdir(directory)
        result_list = list()

        for filename in file_list:
            filename_split = os.path.splitext(filename)
            if ext == filename_split[-1]:
                if self.match_feature_filename(filename_split[0], info, sep):
                    full_filename = "%s/%s" % (directory, filename)
                    result_list.append(full_filename)
                else:
                    continue
        return result_list

    @staticmethod
    def match_feature_filename(filename, info=None, sep="_") -> bool:
        data = filename.split(sep)
        # hist_no, task_idx
        if (data[0] == info[0]) and (data[1] == info[1]):
            return True
        else:
            return False

    def get_learn_data(self) -> dict:
        return {"x": self.dataset[0][0], "y": self.dataset[0][1]}

    def get_eval_data(self) -> dict:
        return {"x": self.dataset[1][0], "y": self.dataset[1][1]}

    def get_json_data(self) -> list:
        return self.dataset[2]


# ---- builder Pattern
class DataManagerBuilder(object):
    def __init__(self):
        self.job_info = None

    def set_job_info(self, job_info):
        self.job_info = job_info
        return self

    def build(self) -> DataManager:
        return DataManager(job_info=self.job_info)
