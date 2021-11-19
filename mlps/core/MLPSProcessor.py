#  -*- coding: utf-8 -*-
#  Author : Manki Baek
#  e-mail : manki.baek@seculayer.com
#  Powered by Seculayer © 2021 Service Model Team, R&D Center.

import os
import json
import shutil
import traceback
from typing import Union
from threading import Timer

from mlps.common.utils.FileUtils import FileUtils
from mlps.common.info.JobInfo import JobInfoBuilder, JobInfo
from mlps.core.data.DataManager import DataManagerBuilder, DataManager
from mlps.common.Constants import Constants
from mlps.common.Common import Common
from mlps.core.apeflow.api.MLModels import MLModels
from mlps.common.decorator.CalTimeDecorator import CalTimeDecorator
from mlps.core.RestManager import RestManager
from mlps.core.SFTPClientManager import SFTPClientManager


class MLPSProcessor(object):
    LOGGER = Common.LOGGER.getLogger()

    def __init__(self, hist_no: str, task_idx: str, job_type: str) -> None:
        self.mrms_sftp_manager: SFTPClientManager = SFTPClientManager(
            "{}:{}".format(Constants.MRMS_SVC, Constants.MRMS_SFTP_PORT), Constants.MRMS_USER, Constants.MRMS_PASSWD)

        self.job_info: JobInfo = JobInfoBuilder() \
            .set_hist_no(hist_no=hist_no) \
            .set_task_idx(task_idx) \
            .set_job_dir(Constants.DIR_LEARN_FEAT) \
            .set_job_type(job_type=job_type) \
            .set_logger(self.LOGGER) \
            .set_sftp_client(self.mrms_sftp_manager) \
            .build()

        self.job_key: str = self.job_info.get_key()
        self.job_type: str = job_type
        self.task_idx: str = task_idx
        self.model: Union[None, MLModels] = None
        self.data_loader_manager: Union[None, DataManager] = None

        curr_sttus_cd = RestManager.get_status_cd(self.job_info.get_key())
        if int(curr_sttus_cd) < int(Constants.STATUS_RUNNING):
            RestManager.update_status_cd(Constants.STATUS_RUNNING, self.job_key,
                                         self.task_idx, '-')\

        self.timer = None
        self.send_resource_usage(self.job_key)

    def send_resource_usage(self, job_key):
        RestManager.send_resource_usage(job_key)
        self.timer = Timer(2, RestManager.send_resource_usage, [job_key])
        self.timer.start()

    def data_loader_init(self) -> None:
        self.data_loader_manager = DataManagerBuilder() \
            .set_job_info(job_info=self.job_info) \
            .set_sftp_client(self.mrms_sftp_manager) \
            .build()

    def run(self) -> None:
        try:
            if self.task_idx == "0":
                RestManager.update_time(self.job_key, "start")
            self.data_loader_init()
            self.data_loader_manager.run()
            self.model_init()
            self.learn()
            self.eval()

            curr_sttus_cd = RestManager.get_status_cd(self.job_info.get_key())
            if int(curr_sttus_cd) < int(Constants.STATUS_COMPLETE):
                RestManager.update_status_cd(Constants.STATUS_COMPLETE, self.job_key,
                                             self.task_idx, '-')

            if self.task_idx == "0":
                RestManager.update_time(self.job_key, "end")
        except Exception as e:
            self.LOGGER.error(e, exc_info=True)
            curr_sttus_cd = RestManager.get_status_cd(self.job_info.get_key())
            if int(curr_sttus_cd) < int(Constants.STATUS_ERROR):
                RestManager.update_status_cd(Constants.STATUS_ERROR, self.job_key,
                                             self.task_idx, traceback.format_exc())
        finally:
            self.timer.join()

    def model_init(self) -> None:
        cluster_info = json.loads(os.environ["TF_CONFIG"])
        self.model = MLModels(
            param_dict_list=self.job_info.get_param_dict_list(),
            cluster=cluster_info["cluster"],
            task_idx=self.task_idx,
            job_key=self.job_key,
            job_type=self.job_type
        )
        self.model.build()
        self.LOGGER.info("MLPS v.{} MLModels initialized complete. [{}]".format(Constants.VERSION, self.job_key))

    @CalTimeDecorator("MLPS Learn")
    def learn(self) -> None:
        self.LOGGER.info("-- MLModels learning start. [{}]".format(self.job_key))

        _data = self.data_loader_manager.get_learn_data()
        self.model.learn(data=_data)

        if int(self.job_info.get_task_idx()) == 0:
            if FileUtils.is_exist("{}/{}".format(Constants.DIR_MODEL, self.job_info.get_hist_no())):
                FileUtils.remove_dir("{}/{}".format(Constants.DIR_MODEL, self.job_info.get_hist_no()))
            shutil.copytree("{}/{}".format(Constants.DIR_ML_TMP, self.job_info.get_hist_no()),
                            "{}/{}".format(Constants.DIR_MODEL, self.job_info.get_hist_no()))

        self.LOGGER.info("-- MLModels learning end. [{}]".format(self.job_key))

    @CalTimeDecorator("MLPS Eval")
    def eval(self) -> None:
        self.LOGGER.info("-- MLModels eval start. [{}]".format(self.job_key))

        eval_data = self.data_loader_manager.get_eval_data()
        json_data = self.data_loader_manager.get_json_data()

        self.model.eval(data=eval_data)

        # RestManager.post_learn_result(self.job_key, self.task_idx,
        #                               Constants.RST_TYPE_RAW, "0", json_data)

        self.LOGGER.info("-- MLModels eval end. [{}]".format(self.job_key))
