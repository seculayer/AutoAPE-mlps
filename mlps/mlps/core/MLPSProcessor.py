#  -*- coding: utf-8 -*-
#  Author : Manki Baek
#  e-mail : manki.baek@seculayer.com
#  Powered by Seculayer © 2021 Service Model Team, R&D Center.

import os
import json
import shutil
# import traceback
from typing import Union

from mlps.common.utils.FileUtils import FileUtils
from mlps.common.info.JobInfo import JobInfoBuilder, JobInfo
from mlps.core.data.DataManager import DataManagerBuilder, DataManager
from mlps.common.Constants import Constants
from mlps.common.Common import Common
from mlps.core.apeflow.api.MLModels import MLModels
from mlps.common.decorator.CalTimeDecorator import CalTimeDecorator
from mlps.core.RestManager import RestManager


class MLPSProcessor(object):
    LOGGER = Common.LOGGER.getLogger()

    def __init__(self, hist_no: str, task_idx: str, job_type: str) -> None:
        self.job_info: JobInfo = JobInfoBuilder() \
            .set_hist_no(hist_no=hist_no) \
            .set_task_idx(task_idx) \
            .set_job_dir(Constants.DIR_LEARN_FEAT) \
            .set_job_type(job_type=job_type) \
            .set_logger(self.LOGGER) \
            .build()

        self.job_key: str = self.job_info.get_key()
        self.job_type: str = job_type
        self.task_idx: str = task_idx
        self.model: Union[None, MLModels] = None
        self.data_loader_manager: Union[None, DataManager] = None

    def data_loader_init(self) -> None:
        try:
            self.data_loader_manager = DataManagerBuilder() \
                .set_job_info(job_info=self.job_info) \
                .build()
        except Exception as e:
            self.LOGGER.error(e, exc_info=True)
            # RestManager.update_status_cd(Constants.STATUS_DATA_CONVERT_ERROR, self.job_key,
            #                              self.task_idx, traceback.format_exc())
            raise e

    def run(self) -> None:
        self.data_loader_init()
        self.data_loader_manager.start()
        self.model_init()
        self.data_loader_manager.join()
        self.learn()
        self.eval()

    def model_init(self) -> None:
        try:
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

        except Exception as e:
            self.LOGGER.error(e, exc_info=True)
            # RestManager.update_status_cd(Constants.STATUS_LEARN_ERROR, self.job_key,
            #                              self.task_idx, traceback.format_exc())
            raise e

    @CalTimeDecorator("MLPS Learn")
    def learn(self) -> None:
        try:
            self.LOGGER.info("-- MLModels learning start. [{}]".format(self.job_key))
            RestManager.update_status_cd(Constants.STATUS_LEARNING, self.job_key,
                                         self.task_idx, '-')

            _data = self.data_loader_manager.get_learn_data()
            self.model.learn(data=_data)

            if int(self.job_info.get_task_idx()) == 0:
                if FileUtils.is_exist("{}/{}".format(Constants.DIR_MODEL, self.job_info.get_model_id())):
                    FileUtils.remove_dir("{}/{}".format(Constants.DIR_MODEL, self.job_info.get_model_id()))
                shutil.copytree("{}/{}".format(Constants.DIR_ML_TMP, self.job_info.get_model_id()),
                                "{}/{}".format(Constants.DIR_MODEL, self.job_info.get_model_id()))

            self.LOGGER.info("-- MLModels learning end. [{}]".format(self.job_key))
            RestManager.update_status_cd(Constants.STATUS_LEARN_COMPLETE, self.job_key,
                                         self.task_idx, '-')
        except Exception as e:
            self.LOGGER.error(e, exc_info=True)
            # RestManager.update_status_cd(Constants.STATUS_LEARN_ERROR, self.job_key,
            #                              self.task_idx, traceback.format_exc())
            raise e

    @CalTimeDecorator("MLPS Eval")
    def eval(self) -> None:
        try:
            self.LOGGER.info("-- MLModels eval start. [{}]".format(self.job_key))
            RestManager.update_status_cd(Constants.STATUS_EVALUATING, self.job_key,
                                         self.task_idx, '-')

            eval_data = self.data_loader_manager.get_eval_data()
            json_data = self.data_loader_manager.get_json_data()

            self.model.eval(data=eval_data)

            RestManager.post_learn_result(self.job_key, self.task_idx,
                                          Constants.RST_TYPE_RAW, json_data)

            self.LOGGER.info("-- MLModels eval end. [{}]".format(self.job_key))
            RestManager.update_status_cd(Constants.STATUS_EVALUATE_COMPLETE, self.job_key,
                                         self.task_idx, '-')

        except Exception as e:
            self.LOGGER.error(e, exc_info=True)
            # RestManager.update_status_cd(Constants.STATUS_EVALUATE_ERROR, self.job_key,
            #                              self.task_idx, traceback.format_exc())
            raise e
