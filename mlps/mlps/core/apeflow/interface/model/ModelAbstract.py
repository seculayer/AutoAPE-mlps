# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team, R&D Center.
from mlps.common.Common import Common
from mlps.core.apeflow.api.algorithms.AlgorithmAbstract import AlgorithmAbstract
from mlps.core.apeflow.api.algorithms.AlgorithmFactory import AlgorithmFactory


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
        self.model.learn(dataset)
        self.model.saved_model()

    def eval(self, dataset):
        # learning
        result = self.model.eval(dataset)
        return result

    def predict(self, x):
        result = self.model.predict(x)
        return result
