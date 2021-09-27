# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import tensorflow as tf
import os
import json
from datetime import datetime
from mlps.common.Common import Common
from mlps.common.Constants import Constants
from mlps.core.RestManager import RestManager


class LearnResultCallback(tf.keras.callbacks.Callback):
    def __init__(self, **kwargs):
        tf.keras.callbacks.Callback.__init__(self)
        self.job_key = kwargs["job_key"]
        self.global_sn = kwargs["global_sn"]
        self.data_len = kwargs["data_len"]
        self.LOGGER = Common.LOGGER.getLogger()
        self.learn_result = None
        self.start_time = None
        self.end_time = None
        self.total_time = 0
        self.eps = 0

    def on_epoch_begin(self, epoch, logs=None):
        self.start_time = datetime.now()

    def on_epoch_end(self, epoch, logs=None):
        self.end_time = datetime.now()
        self.total_time += (self.end_time - self.start_time).total_seconds()
        self.eps = self.data_len / self.total_time
        result = logs
        result["step"] = epoch + 1
        self.LOGGER.info(result)
        self.learn_result = result

        if json.loads(os.environ["TF_CONFIG"])["task"]["index"] == "0":
            RestManager.post_learn_result(
                job_key=self.job_key,
                task_idx=json.loads(os.environ["TF_CONFIG"])["task"]["index"],
                rst_type=Constants.RST_TYPE_LEARN,
                global_sn=self.global_sn,
                rst=result
            )

    def get_learn_result(self):
        return self.learn_result

    def get_eps(self):
        return self.eps
