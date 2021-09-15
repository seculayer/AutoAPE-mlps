# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import os
import json

from mlps.common.Common import Common
from mlps.common.Constants import Constants
from mlps.core.RestManager import RestManager
from gensim.models.callbacks import CallbackAny2Vec


class LearnResultCallback(CallbackAny2Vec):
    # Callback to print loss after each epoch.
    LOGGER = Common.LOGGER.getLogger()

    def __init__(self, job_key, global_sn="0"):
        self.epoch = 1
        self.global_sn = global_sn
        self.job_key = job_key

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        _result = {"global_sn": self.global_sn, "step": self.epoch, "loss": loss}

        # RestManager.post_learn_result(
        #     job_key=self.job_key,
        #     task_idx=json.loads(os.environ["TF_CONFIG"])["task"]["index"],
        #     rst_type=Constants.RST_TYPE_LEARN,
        #     global_sn=self.global_sn,
        #     rst=_result
        # )

        self.LOGGER.info(_result)
        self.epoch += 1
