# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import numpy as np

from mlps.common.Constants import Constants
from mlps.common.Common import Common
from mlps.common.exceptions.ParameterError import ParameterError


class AlgorithmAbstract(object):
    ALG_CODE = "AlgorithmAbstract"
    ALG_TYPE = []
    DATA_TYPE = []
    VERSION = "1.0.0"
    LIB_TYPE = "None"

    def __init__(self, param_dict: dict, ext_data=None):
        # 파라미터 체크
        self.LOGGER = Common.LOGGER.getLogger()
        _param_dict = dict(param_dict, **param_dict.get("params"))
        self.ext_data = ext_data
        self.param_dict = self._check_parameter(_param_dict)
        self.learn_params = self._check_learning_parameter(_param_dict)
        self.early_steps = 0
        self.batch_size = Constants.BATCH_SIZE

    @staticmethod
    def _check_parameter(param_dict):
        _param_dict = dict()

        _param_dict["model_nm"] = str(param_dict["model_nm"])
        _param_dict["alg_sn"] = str(param_dict["alg_sn"])
        _param_dict["global_sn"] = str(param_dict["global_sn"])
        _param_dict["algorithm_type"] = str(param_dict["algorithm_type"])
        _param_dict["job_key"] = str(param_dict["job_key"])
        _param_dict["task_idx"] = str(param_dict["task_idx"])

        return _param_dict

    @staticmethod
    def _check_learning_parameter(param_dict):
        _param_dict = dict()
        # Parameter Setting
        try:
            _param_dict["global_step"] = int(param_dict["global_step"])
            if _param_dict["global_step"] < 1:
                _param_dict["global_step"] = 1
            _param_dict["early_type"] = param_dict["early_type"]
            if _param_dict["early_type"] != Constants.EARLY_TYPE_NONE:
                _param_dict["minsteps"] = int(param_dict["minsteps"])
                _param_dict["early_key"] = param_dict["early_key"]
                _param_dict["early_value"] = float(param_dict["early_value"])
        except Exception as e:
            raise ParameterError
        return _param_dict

    def early_stop(self, **kwargs):
        if self.learn_params["early_type"] == Constants.EARLY_TYPE_NONE:
            return False

        results = kwargs["results"]
        key = self.learn_params["early_key"]
        if self.learn_params["early_type"] == Constants.EARLY_TYPE_MIN:
            if self.learn_params["minsteps"] < results[-1]["step"]:
                if results[-1][key] < self.learn_params["early_value"]:
                    return True

        elif self.learn_params["early_type"] == Constants.EARLY_TYPE_MAX:
            if self.learn_params["minsteps"] < results[-1]["step"]:
                if results[-1][key] > self.learn_params["early_value"]:
                    return True

        elif self.learn_params["early_type"] == Constants.EARLY_TYPE_VAR:
            try:
                if abs(results[-1][key] - results[-2][key]) < self.learn_params["early_value"]:
                    self.early_steps += 1
                else:
                    self.early_steps = 0
            except Exception as e:
                pass

            if self.early_steps >= self.learn_params["minsteps"]:
                self.LOGGER.info("------ EARLY STOP !!!!! -----")
                return True
        return False

    def learn(self, dataset: dict):
        raise NotImplementedError

    def predict(self, x):
        raise NotImplementedError

    def load_model(self):
        raise NotImplementedError

    def saved_model(self):
        raise NotImplementedError

    def eval(self, dataset: dict):
        results = list()
        fn_dict = {
            "Classifier": "self.eval_classifier",
            "Regressor": "self.eval_regressor",
            "Clustering": "self.eval_clustering",
            "FE": "self.eval_fe",
            "OD": "self.eval_od"
        }
        try:
            results.append(eval(fn_dict[self.param_dict["algorithm_type"]])(dataset=dataset))
        except Exception as e:
            self.LOGGER.error(e, exc_info=True)

        return results

    def eval_classifier(self, dataset: dict):
        x = dataset["x"]
        y = dataset["y"]

        num_classes = self.param_dict["output_units"]

        predicts = self.predict(x)

        if len(predicts.shape) >= 2:
            pred = np.argmax(predicts, axis=1)

        else:
            pred = [round(float(val)) for val in predicts]

        if len(y.shape) >= 2:
            _y = np.argmax(y, axis=1)
        else:
            _y = list(map(int, y))

        results = list()
        for c in range(int(num_classes)):
            result = {
                "global_sn": self.param_dict["global_sn"],
                "total": np.sum(np.equal(_y, c), dtype="int32"),
                "TP": np.sum(np.take(np.equal(_y, c), np.where(np.equal(pred, c))))  # 정탐
            }
            result["FN"] = int(result["total"]) - int(result["TP"])  # 미탐
            result["FP"] = np.sum(np.equal(pred, c)) - int(result["TP"])  # 오탐
            # self.AI_LOGGER.info(result)
            results.append(result)

        self.LOGGER.debug(results)
        return results
