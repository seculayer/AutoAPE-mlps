# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

from datetime import datetime
import os
import json

from mlps.common.Common import Common
from mlps.core.apeflow.api.algorithms.AlgorithmAbstract import AlgorithmAbstract
from mlps.core.apeflow.api.algorithms.AlgorithmFactory import AlgorithmFactory
from mlps.core.RestManager import RestManager


class ModelAbstract(object):
    def __init__(self, param_dict: dict, ext_data=None):
        self.LOGGER = Common.LOGGER.getLogger()
        self.param_dict = param_dict
        self.ext_data = ext_data
        self.model = None

    def _build(self) -> AlgorithmAbstract:
        model = AlgorithmFactory.create(param_dict=self.param_dict, ext_data=self.ext_data)
        model.load_model()

        return model

    def learn(self, dataset):
        # learning
        start_time = datetime.now()
        self.model.learn(dataset)
        learn_time_sec = (datetime.now() - start_time).total_seconds()
        eps = len(dataset["x"]) / learn_time_sec
        learn_rst = self.model.learn_result(dataset)
        if json.loads(os.environ["TF_CONFIG"])["task"]["index"] == "0":
            RestManager.update_eps(self.param_dict["job_key"], eps)
            RestManager.update_learn_result(self.param_dict["job_key"], learn_rst[-1])

        self.model.saved_model()

    def eval(self, dataset):
        # learning
        result = self.model.eval(dataset)
        return result

    def predict(self, x):
        result = self.model.predict(x)
        return result
