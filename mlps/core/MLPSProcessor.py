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
from datetime import datetime

from mlps.common.utils.FileUtils import FileUtils
from mlps.common.info.JobInfo import JobInfoBuilder, JobInfo
from mlps.core.data.DataManager import DataManagerBuilder, DataManager
from mlps.common.Constants import Constants
from mlps.common.Common import Common
from mlps.core.apeflow.api.MLModels import MLModels
from mlps.common.decorator.CalTimeDecorator import CalTimeDecorator
from mlps.core.RestManager import RestManager
from mlps.core.SFTPClientManager import SFTPClientManager
from mlps.core.data.datawriter.ResultWriter import ResultWriter


class MLPSProcessor(object):
    LOGGER = Common.LOGGER.getLogger()

    def __init__(self, hist_no: str, task_idx: str, job_type: str) -> None:
        self.mrms_sftp_manager: SFTPClientManager = SFTPClientManager(
            "{}:{}".format(Constants.MRMS_SVC, Constants.MRMS_SFTP_PORT), Constants.MRMS_USER, Constants.MRMS_PASSWD)

        self.job_info: JobInfo = JobInfoBuilder() \
            .set_hist_no(hist_no=hist_no) \
            .set_task_idx(task_idx) \
            .set_job_dir(Constants.DIR_JOB) \
            .set_job_type(job_type=job_type) \
            .set_logger(self.LOGGER) \
            .set_sftp_client(self.mrms_sftp_manager) \
            .build()

        self.job_key: str = self.job_info.get_key()
        self.job_type: str = job_type
        self.task_idx: str = task_idx
        self.model: Union[None, MLModels] = None
        self.data_loader_manager: Union[None, DataManager] = None

        RestManager.set_status(self.job_type, self.job_key, self.task_idx,
                               Constants.STATUS_RUNNING, '-')

        self.timer = None
        if self.job_type == Constants.JOB_TYPE_LEARN:
            self.start_resource_usage(self.job_key)

    def start_resource_usage(self, job_key):
        RestManager.send_resource_usage(job_key)
        self.timer: Timer = Timer(2, self.start_resource_usage, [job_key])
        # if daemon set true, when parents are terminated it is killed immediately
        self.timer.daemon = True
        self.timer.start()

    def data_loader_init(self) -> None:
        self.data_loader_manager = DataManagerBuilder() \
            .set_job_info(job_info=self.job_info) \
            .set_sftp_client(self.mrms_sftp_manager) \
            .build()

    def run(self) -> None:
        try:
            RestManager.set_time(self.job_type, self.job_key, self.task_idx, "start")

            self.data_loader_init()
            self.data_loader_manager.run()
            self.model_init()
            if self.job_type == Constants.JOB_TYPE_LEARN:
                self.learn()
                self.eval()
            else:  # self.job_type == Constants.JOB_TYPE_INFERENCE:
                self.inference()

            RestManager.set_status(self.job_type, self.job_key, self.task_idx,
                                   Constants.STATUS_COMPLETE, '-')
            RestManager.set_time(self.job_type, self.job_key, self.task_idx, "end")

        except Exception as e:
            self.LOGGER.error(e, exc_info=True)
            RestManager.set_status(self.job_type, self.job_key, self.task_idx,
                                   Constants.STATUS_ERROR, traceback.format_exc())

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
        len_data = len(_data['x'])
        start = datetime.now()
        self.model.learn(data=_data)
        end_time = datetime.now()

        if int(self.job_info.get_task_idx()) == 0:
            # update eps
            model_eps = len_data / (end_time - start).total_seconds() * \
                            int(self.job_info.get_param_dict_list()[-1].get("global_step"))
            RestManager.update_eps(self.job_info.get_key(), model_eps)
            # move model folder
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

    @CalTimeDecorator("MLPS Inference")
    def inference(self) -> None:
        self.LOGGER.info(f"-- MLModels inference start. [{self.job_key}]")

        inferenece_data: dict = self.data_loader_manager.get_inference_data()

        result_list = self.model.predict(inferenece_data)
        self.result_write(result_list)

        self.LOGGER.info("-- MLModels inference end. [{}]".format(self.job_key))

    @CalTimeDecorator("MLPS Result Write")
    def result_write(self, result_list):
        json_data = self.data_loader_manager.get_json_data()
        json_data = self._insert_info(json_data, result_list)

        ResultWriter.result_file_write(
            result_path=Constants.DIR_RESULT,
            results=json_data,
            result_type="inference"
        )

    def _insert_info(self, json_data, result_list):
        curr_time = datetime.now().strftime('%Y%m%d%H%M%S')
        is_ensemble = True if len(result_list) > 1 else False

        for line_idx, jsonline in enumerate(json_data):
            for alg_idx, result in enumerate(result_list):
                # predict result
                key_name = f"{alg_idx}_result" if is_ensemble else "total_result"
                if isinstance(result[line_idx], list) and len(result[line_idx]) > 1:
                    jsonline[key_name] = int(result[line_idx].argmax(axis=1))
                else:
                    jsonline[key_name] = int(result[line_idx])
            jsonline["eqp_dt"] = curr_time
            jsonline["hist_no"] = self.job_key
            json_data[line_idx] = jsonline

        return json_data
