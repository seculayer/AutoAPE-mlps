# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

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
from mlps.core.SFTPClientManager import SFTPClientManager
from mlps.core.data.DataLoaderFactory import DataloaderFactory


class DataManager(object, metaclass=Singleton):

    def __init__(self, job_info: JobInfo, sftp_client: SFTPClientManager) -> None:
        # threading.Thread.__init__(self)
        self.LOGGER = Common.LOGGER.getLogger()
        self.job_info: JobInfo = job_info
        self.data_queue: Queue = Queue()
        self.DataSampler = DataSampler(self.job_info)
        self.sftp_client = sftp_client

        self.dataset_info: DatasetInfo = self.job_info.get_dataset_info()
        self.dataset = {}

        self.job_type = self.job_info.get_job_type()

    @CalTimeDecorator("Data Manager")
    def run(self) -> None:
        try:
            self.LOGGER.info("DataManager Start.")

            # ---- data load
            data_list = self.read_files(self.dataset_info.get_fields())

            self.DataSampler.set_data(data_list)
            if self.job_type == Constants.JOB_TYPE_LEARN:
                self.dataset = self.DataSampler.sampling()
            else:  # self.job_type == Constants.JOB_TYPE_INFERENCE:
                self.dataset = data_list

            self.LOGGER.info("DataManager End.")
        except Exception as e:
            self.LOGGER.error(e, exc_info=True)
            RestManager.set_status(self.job_info.get_job_type(), self.job_info.get_key(),
                                   self.job_info.get_task_idx(), Constants.STATUS_ERROR,
                                   traceback.format_exc())
            raise e

    def read_files(self, fields: List[FieldInfo]) \
            -> List:
        # ---- prepare
        # 분산이 되면 워커마다 파일 1개씩, 아니면 워커1개가 모든 파일을 읽는다
        file_list = list()
        if self.job_info.get_dist_yn() \
                and (len(self.job_info.get_file_list()) == self.job_info.get_num_worker()):
            idx = int(self.job_info.get_task_idx())
            file_list.append(self.job_info.get_file_list()[idx])
        else:
            file_list = self.job_info.get_file_list()

        # data_list = self.read_subproc(file_list, fields)
        data_list = DataloaderFactory.create(
                        dataset_format=self.job_info.get_dataset_format(),
                        job_info=self.job_info,
                        sftp_client=self.sftp_client
                    ).read(file_list, fields)

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
            .set_job_info(self.job_info) \
            .build()

    def get_learn_data(self) -> dict:
        return {"x": self.dataset[0][0], "y": self.dataset[0][1]}

    def get_eval_data(self) -> dict:
        return {"x": self.dataset[1][0], "y": self.dataset[1][1]}

    def get_json_data(self) -> list:
        return self.dataset[2]

    def get_inference_data(self) -> dict:
        return {"x": self.dataset[0], "y": self.dataset[1]}


# ---- builder Pattern
class DataManagerBuilder(object):
    def __init__(self):
        self.job_info = None
        self.sftp_client = None

    def set_job_info(self, job_info):
        self.job_info = job_info
        return self

    def set_sftp_client(self, sftp_client):
        self.sftp_client = sftp_client
        return self

    def build(self) -> DataManager:
        return DataManager(job_info=self.job_info, sftp_client=self.sftp_client)
