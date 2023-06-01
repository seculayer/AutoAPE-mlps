#  -*- coding: utf-8 -*-
#  Author : Manki Baek
#  e-mail : manki.baek@seculayer.com
#  Powered by Seculayer © 2021 Service Model Team, R&D Center.
import copy
import os
import json
import traceback
from typing import Union, Dict, List
from threading import Timer
from datetime import datetime
import numpy as np

from mlps.info.JobInfo import JobInfoBuilder, JobInfo
from mlps.core.data.DataManager import DataManagerBuilder, DataManager
from mlps.common.Constants import Constants
from mlps.common.Common import Common
from apeflow.api.MLModels import MLModels
from pycmmn.decorator.CalTimeDecorator import CalTimeDecorator
from pycmmn.rest.RestManager import RestManager
from pycmmn.sftp.SFTPClientManager import SFTPClientManager
from mlps.core.data.datawriter.ResultWriter import ResultWriter


class MLPSProcessor(object):
    LOGGER = Common.LOGGER.getLogger()

    def __init__(self, hist_no: str, task_idx: str, job_type: str) -> None:
        self.mrms_sftp_manager: SFTPClientManager = SFTPClientManager(
            "{}:{}".format(Constants.MRMS_SVC, Constants.MRMS_SFTP_PORT),
            Constants.MRMS_USER, Constants.MRMS_PASSWD, self.LOGGER
        )

        try:
            self.job_info: JobInfo = JobInfoBuilder() \
                .set_hist_no(hist_no=hist_no) \
                .set_task_idx(task_idx) \
                .set_job_dir(Constants.DIR_JOB) \
                .set_job_type(job_type=job_type) \
                .set_logger(self.LOGGER) \
                .set_sftp_client(self.mrms_sftp_manager) \
                .build()
        except Exception as e:
            RestManager.set_status(
                Constants.REST_URL_ROOT, self.LOGGER,
                job_type, hist_no, task_idx,
                Constants.STATUS_ERROR, '-'
            )
            raise e
        job_info_for_log = copy.deepcopy(self.job_info.info_dict)
        job_info_for_log.pop('datasets')
        self.LOGGER.info(f"{job_info_for_log}")
        self.job_key: str = self.job_info.get_key()
        self.job_type: str = job_type
        self.task_idx: str = task_idx
        self.model: Union[None, MLModels] = None
        self.data_loader_manager: Union[None, DataManager] = None

        RestManager.set_status(
            Constants.REST_URL_ROOT, self.LOGGER,
            self.job_type, self.job_key, self.task_idx,
            Constants.STATUS_RUNNING, '-'
        )

        self.timer = None
        if self.job_type == Constants.JOB_TYPE_LEARN:
            self.LOGGER.info("resource usage checking start..")
            self.start_resource_usage(self.job_key)

    def start_resource_usage(self, job_key):
        RestManager.send_resource_usage(
            Constants.REST_URL_ROOT, self.LOGGER, job_key
        )
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
            RestManager.set_time(
                Constants.REST_URL_ROOT, self.LOGGER, self.job_type, self.job_key, self.task_idx, "start"
            )

            self.data_loader_init()
            self.data_loader_manager.run()
            self.model_init()
            if self.job_type == Constants.JOB_TYPE_LEARN:
                self.learn()
                self.copy_job()
                self.eval()
            else:  # self.job_type == Constants.JOB_TYPE_INFERENCE:
                self.inference()

            RestManager.set_status(
                Constants.REST_URL_ROOT, self.LOGGER,
                self.job_type, self.job_key, self.task_idx,
                Constants.STATUS_COMPLETE, '-'
            )
            RestManager.set_time(
                Constants.REST_URL_ROOT, self.LOGGER,
                self.job_type, self.job_key, self.task_idx, "end"
            )

        except Exception as e:
            self.LOGGER.error(e, exc_info=True)
            RestManager.set_status(
                Constants.REST_URL_ROOT, self.LOGGER,
                self.job_type, self.job_key, self.task_idx,
                Constants.STATUS_ERROR, traceback.format_exc()
            )

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

    @CalTimeDecorator("MLPS Learn", LOGGER)
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
            RestManager.update_eps(
                Constants.REST_URL_ROOT, self.LOGGER, self.job_info.get_key(), model_eps
            )

        self.LOGGER.info("-- MLModels learning end. [{}]".format(self.job_key))

    @CalTimeDecorator("MLPS Eval", LOGGER)
    def eval(self) -> None:
        self.LOGGER.info("-- MLModels eval start. [{}]".format(self.job_key))

        eval_data = self.data_loader_manager.get_eval_data()
        json_data = self.data_loader_manager.get_json_data()

        self.model.eval(data=eval_data)

        # RestManager.post_learn_result(self.job_key, self.task_idx,
        #                               Constants.RST_TYPE_RAW, "0", json_data)

        self.LOGGER.info("-- MLModels eval end. [{}]".format(self.job_key))

    @CalTimeDecorator("MLPS Inference", LOGGER)
    def inference(self) -> None:
        try:
            self.LOGGER.info(f"-- MLModels inference start. [{self.job_key}]")

            inferenece_data: dict = self.data_loader_manager.get_inference_data()

            result_list = self.model.predict(inferenece_data)
            self.result_write(result_list)

            self.LOGGER.info("-- MLModels inference end. [{}]".format(self.job_key))
        except Exception as e:
            raise e
        finally:
            RestManager.send_inference_progress(
                Constants.REST_URL_ROOT, self.LOGGER, self.job_key, 100.0, "delete"
            )

    @CalTimeDecorator("MLPS Result Write", LOGGER)
    def result_write(self, result_list):
        json_data = self.data_loader_manager.get_json_data()
        json_data = self._insert_inference_info(json_data, result_list)

        ResultWriter.result_file_write(
            result_path=Constants.DIR_RESULT,
            results=json_data,
            result_type="inference"
        )

    def _insert_inference_info(self, json_data, result_list: List[Dict]):
        curr_time = datetime.now().strftime('%Y%m%d%H%M%S')
        is_ensemble = True if len(result_list) > 1 else False

        for line_idx, jsonline in enumerate(json_data):
            for alg_idx, result in enumerate(result_list):
                # predict result
                key_name = f"{alg_idx}_result" if is_ensemble else "result"
                prob_key_name = f"{alg_idx}_accuracy" if is_ensemble else "accuracy"

                jsonline[key_name] = int(result["pred"][line_idx])
                if result["proba"] is not None:
                    if isinstance(result["proba"][line_idx], (list, np.ndarray)):
                        jsonline[prob_key_name] = float(result["proba"][line_idx].max())
                    else:
                        try:
                            jsonline[prob_key_name] = float(result["proba"][line_idx])
                        except Exception as e:
                            self.LOGGER.error(f"result type : {type(result['proba'][line_idx])}")

            jsonline["eqp_dt"] = curr_time
            jsonline["infr_hist_no"] = self.job_key
            json_data[line_idx] = jsonline

        return json_data

    def copy_job(self):
        if int(self.job_info.get_task_idx()) == 0:
            job_path = "{}/{}/{}.job".format(Constants.DIR_JOB, self.job_info.get_project_id(), self.job_key)
            dir_model = "{}/{}".format(Constants.DIR_STORAGE, self.job_info.get_hist_no())

            with self.mrms_sftp_manager.get_client().open(f"{job_path}", option="r") as r:
                job = r.read()
            with self.mrms_sftp_manager.get_client().open(f"{dir_model}/{self.job_key}.job", option='w') as w:
                w.write(job)
