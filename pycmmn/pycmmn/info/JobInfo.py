# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import json
import logging
from typing import List

from pycmmn.common.StringUtil import StringUtil
from pycmmn.interfaces.FileUtils import FileUtils
from pycmmn.exceptions.JobFileLoadError import JobFileLoadError
from pycmmn.info.DatasetInfo import DatasetInfo


class JobInfo(object):
    def __init__(self, hist_no, task_idx, job_type, job_dir, logger):
        self.job_type = job_type
        self.hist_no = hist_no
        self.task_idx = task_idx
        self.job_dir = job_dir
        self.LOGGER = logger

        self.info_dict = self._load()
        self.LOGGER.info(self.info_dict)

        self.dataset_list = self._create_dataset(self.info_dict.get("datasets"))

    # ---- loading
    def _create_job_filename(self) -> str:
        return self.hist_no + "_" + self.task_idx + ".job"

    def _load(self) -> dict:
        filename = self._create_job_filename()
        f = None
        try:
            path = self.job_dir + "/" + filename
            f = FileUtils.file_pointer(path, "r")
            job_dict = json.load(f)

        except Exception as e:
            self.LOGGER.error(str(e), exc_info=True)
            raise JobFileLoadError(key=filename)

        finally:
            if f is not None:
                f.close()

        return job_dict

    def _create_dataset(self, dataset_dict_list) -> List[DatasetInfo]:
        result_list = list()
        for dataset_dict in dataset_dict_list:
            dataset = DatasetInfo(dataset_dict)
            self.LOGGER.debug(str(dataset))
            result_list.append(dataset)
        return result_list

    # ---- get
    def get_hist_no(self) -> str:
        return self.hist_no

    def get_dataset_list(self) -> List[DatasetInfo]:
        return self.dataset_list

    def num_dataset(self) -> int:
        return len(self.dataset_list)

    def get_job_type(self) -> str:
        return self.job_type

    def get_task_idx(self) -> str:
        return self.task_idx

    def get_fields(self, dataset_idx: int):
        return self.dataset_list[dataset_idx].get_fields()

    def get_sampling_type(self) -> str:
        return self.info_dict.get("sample_type_cd", "4")  # SAMPLE_TYPE_NONE

    def get_sampling_ratio(self) -> float:
        return float(StringUtil.get_int(self.info_dict.get("edu_per", 70)) / 100)

    def get_key(self) -> str:
        return self.info_dict.get("key", "")

    def get_param_dict_list(self) -> list:
        return self.info_dict.get("algorithms", list())

    def get_model_type_cd(self) -> str:
        return self.info_dict.get("model_type_cd", "")

    def get_num_worker(self) -> int:
        return int(self.info_dict.get("num_worker", "1"))

    def get_data_type(self, algorithms_idx: int) -> str:
        return self.get_param_dict_list()[algorithms_idx].get("data_type", "Single")

    def get_alg_type(self, algorithms_idx: int) -> str:
        return self.get_param_dict_list()[algorithms_idx].get("algorithm_type", "Classifier")

    def get_learn_id(self) -> str:
        return self.info_dict.get("learn_id", "")

    def get_model_id(self) -> str:
        return self.info_dict.get("model_id", "")

    def get_statistic_yn(self) -> str:
        return self.info_dict.get("statistic_yn", "N")

    def get_dataset_lines(self, dataset_idx: int) -> List[int]:
        return self.get_dataset_list()[dataset_idx].get_dist_lines()

    def get_dataset_cnt_labels(self, dataset_idx: int) -> dict:
        return self.get_dataset_list()[dataset_idx].get_statistic()["label"]["unique"]

    # ----- rtdetect
    def get_detect_type_cd(self) -> str:
        return self.info_dict.get("detect_type_cd", "1")

    def get_models_list(self) -> list:
        return self.info_dict.get("models", list())

    def get_datasets_list_json(self) -> list:
        return self.info_dict.get("datasets", [])

    def get_datasets_info_json(self) -> list:
        return self.info_dict.get("datasets", list())

    def get_detect_id(self) -> str:
        return self.info_dict.get("detect_id", "")

    def get_model_id_list(self) -> list:
        return self.info_dict.get("model_id_list", list())


class JobInfoBuilder(object):
    def __init__(self):
        self.job_type = None
        self.hist_no = None
        self.task_idx = None
        self.job_dir = None
        self.logger = logging.getLogger()

    def set_job_type(self, job_type):
        self.job_type = job_type
        return self

    def set_hist_no(self, hist_no):
        self.hist_no = hist_no
        return self

    def set_job_dir(self, job_dir):
        self.job_dir = job_dir
        return self

    def set_task_idx(self, task_idx):
        self.task_idx = task_idx
        return self

    def set_logger(self, logger):
        self.logger = logger
        return self

    def build(self) -> JobInfo:
        return JobInfo(
            hist_no=self.hist_no, task_idx=self.task_idx,
            job_type=self.job_type, job_dir=self.job_dir,
            logger=self.logger
        )
