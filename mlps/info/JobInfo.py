# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import logging

from pycmmn.Singleton import Singleton
from mlps.common.Constants import Constants
from pycmmn.exceptions.FileLoadError import FileLoadError
from pycmmn.rest.RestManager import RestManager
from mlps.info.DatasetInfo import DatasetInfo
from pycmmn.sftp.SFTPClientManager import SFTPClientManager
from pycmmn.utils.StringUtil import StringUtil


class JobInfo(object, metaclass=Singleton):
    def __init__(self, hist_no, task_idx, job_type, job_dir, logger, sftp_client):
        self.job_type: str = job_type
        self.hist_no: str = hist_no
        self.task_idx: str = task_idx
        self.job_dir: str = job_dir
        self.LOGGER = logger
        self.sftp_client: SFTPClientManager = sftp_client

        self.info_dict: dict = self._load()
        self.LOGGER.debug(self.info_dict)

        self.dataset_info: DatasetInfo = self._create_dataset(self.info_dict.get("datasets"))

    # ---- loading
    def _create_job_filename(self) -> str:
        return self.job_type + "_" + self.hist_no + ".job"

    def _load(self) -> dict:
        filename = self._create_job_filename()
        try:
            if self.job_type == Constants.JOB_TYPE_LEARN:
                case = f"{RestManager.get_project_id(rest_url_root=Constants.REST_URL_ROOT, logger=self.LOGGER, job_key=self.hist_no)}"
            else:  # self.job_type == Constants.JOB_TYPE_INFERENCE:
                case = "inference"
            path = f"{self.job_dir}/{case}/{filename}"
            job_dict = self.sftp_client.load_json_data(path)

        except Exception as e:
            self.LOGGER.error(str(e), exc_info=True)
            raise FileLoadError(file_name=filename)

        return job_dict

    def _create_dataset(self, dataset_dict) -> DatasetInfo:
        dataset = DatasetInfo(dataset_dict, self.get_target_field())
        self.LOGGER.debug(str(dataset))

        return dataset

    # ---- get
    def get_hist_no(self) -> str:
        return self.hist_no

    def get_dataset_info(self) -> DatasetInfo:
        return self.dataset_info

    def get_job_type(self) -> str:
        return self.job_type

    def get_task_idx(self) -> str:
        return self.task_idx

    def get_fields(self):
        return self.dataset_info.get_fields()

    def get_sampling_type(self) -> str:
        return self.info_dict.get("sample_type_cd", "4")  # SAMPLE_TYPE_NONE

    def get_sampling_ratio(self) -> float:
        return float(self.info_dict.get("edu_per", 80) / 100)

    def get_key(self) -> str:
        # key format : jobType_HistNo
        return self.info_dict.get("key", "")

    def get_param_dict_list(self) -> list:
        return [self.info_dict.get("algorithms", dict())]

    def set_input_units(self, input_units):
        for param_dict in self.get_param_dict_list():
            param_dict["params"]["input_units"] = input_units

    def set_output_units(self, output_units):
        for param_dict in self.get_param_dict_list():
            param_dict["params"]["output_units"] = output_units

    def get_num_worker(self) -> int:
        return int(self.info_dict.get("num_worker", "1"))

    def get_project_id(self) -> str:
        return self.info_dict.get("project_id")

    def get_target_field(self) -> str:
        return self.info_dict.get("project_target_field")

    def get_dataset_cnt_labels(self) -> dict:
        meta_list: list = self.info_dict.get("datasets", {}).get("metadata_json", {}).get("meta")
        target_field = self.get_target_field()
        rst = None
        for meta in meta_list:
            if meta.get("field_nm") == target_field:
                rst = meta.get("statistics").get("unique")
                break

        return rst

    def get_file_list(self) -> list:
        return self.info_dict.get("datasets", {}).get("metadata_json", {}).get("file_list")

    def get_dataset_lines(self) -> list:
        if self.get_dataset_format() == Constants.DATASET_FORMAT_IMAGE:
            return self.info_dict.get("datasets", {}).get("metadata_json", {}).get("file_num")
        else:  # Constants.DATASET_FORMAT_TEXT, Constants.DATASET_FORMAT_TABLE
            return self.info_dict.get("datasets", {}).get("metadata_json", {}).get("file_num_line")

    def get_dist_yn(self) -> bool:
        return StringUtil.get_boolean(self.info_dict.get("algorithms", {}).get("dist_yn", "").lower())

    def get_dataset_format(self) -> str:
        return self.info_dict.get("dataset_format")

    # ----- rtdetect
    # def get_detect_type_cd(self) -> str:
    #     return self.info_dict.get("detect_type_cd", "1")
    #
    # def get_models_list(self) -> list:
    #     return self.info_dict.get("models", list())
    #
    # def get_datasets_info_json(self) -> dict:
    #     return self.info_dict.get("datasets", dict())
    #
    # def get_detect_id(self) -> str:
    #     return self.info_dict.get("detect_id", "")
    #
    # def get_model_id_list(self) -> list:
    #     return self.info_dict.get("model_id_list", list())


class JobInfoBuilder(object):
    def __init__(self):
        self.job_type = None
        self.hist_no = None
        self.task_idx = None
        self.job_dir = None
        self.logger = logging.getLogger()
        self.sftp_client = None

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

    def set_sftp_client(self, sftp_client):
        self.sftp_client = sftp_client
        return self

    def build(self) -> JobInfo:
        return JobInfo(
            hist_no=self.hist_no, task_idx=self.task_idx,
            job_type=self.job_type, job_dir=self.job_dir,
            logger=self.logger, sftp_client=self.sftp_client
        )
