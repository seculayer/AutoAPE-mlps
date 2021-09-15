# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import tensorflow as tf
import os
import json
from mlps.common.Common import Common
from mlps.common.Constants import Constants
from mlps.core.RestManager import RestManager


class LearnResultCallback(tf.keras.callbacks.Callback):
    def __init__(self, **kwargs):
        tf.keras.callbacks.Callback.__init__(self)
        self.job_key = kwargs["job_key"]
        self.global_sn = kwargs["global_sn"]
        self.LOGGER = Common.LOGGER.getLogger()

    def on_epoch_end(self, epoch, logs=None):
        result = logs
        result["step"] = epoch + 1
        self.LOGGER.info(result)
        # RestManager.post_learn_result(
        #     job_key=self.job_key,
        #     task_idx=json.loads(os.environ["TF_CONFIG"])["task"]["index"],
        #     rst_type=Constants.RST_TYPE_LEARN,
        #     global_sn=self.global_sn,
        #     rst=result
        # )
