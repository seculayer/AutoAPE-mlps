# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import os
import json
from datetime import datetime

from mlps.common.Common import Common
from gensim.models.callbacks import CallbackAny2Vec
from mlps.core.RestManager import RestManager


class LearnResultCallback(CallbackAny2Vec):
    # Callback to print loss after each epoch.
    LOGGER = Common.LOGGER.getLogger()

    def __init__(self, job_key, data_len, global_sn="0"):
        self.epoch = 1
        self.global_sn = global_sn
        self.job_key = job_key
        self.data_len = data_len
        self.start_time = None
        self.end_time = None
        self.total_time = 0
        self.eps = 0
        self.learn_result = list()

    def on_epoch_begin(self, model):
        self.start_time = datetime.now()

    def on_epoch_end(self, model):
        self.end_time = datetime.now()

        loss = model.get_latest_training_loss()
        self.total_time += (self.end_time - self.start_time).total_seconds()
        self.eps = self.data_len / self.total_time
        _result = {"global_sn": self.global_sn, "step": self.epoch, "loss": loss}
        self.learn_result.append(_result)

        if json.loads(os.environ["TF_CONFIG"])["task"]["index"] == "0":
            RestManager.update_learn_result(
                job_key=self.job_key,
                rst=self.learn_result
            )

        self.LOGGER.info(_result)
        self.epoch += 1

    def get_learn_result(self):
        return self.learn_result

    def get_eps(self):
        return self.eps
