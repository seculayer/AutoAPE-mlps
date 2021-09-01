# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

from typing import Union, List, Tuple
import numpy as np

from mlps.common.Common import Common
from mlps.common.Constants import Constants
from mlps.common.utils.StringUtil import StringUtil
from mlps.core.apeflow.interface.model.ModelBuilder import ModelBuilder
from mlps.core.apeflow.interface.model.ModelAbstract import ModelAbstract
from mlps.core.RestManager import RestManager


class ModelInterface(object):
    LOGGER = Common.LOGGER.getLogger()

    def __init__(self, method_type, param_dict_list, ext_data):
        self.method_type: str = method_type
        self.ext_data: Union[dict, list, None] = ext_data
        self.model_list = self._build(param_dict_list)
        self.param_dict_list = param_dict_list
        self.input_data = dict()
        self.prev_data = None

    def _build(self, param_dict_list) -> List[Tuple[ModelAbstract, bool]]:
        model_list = list()
        for param_dict in param_dict_list:
            model: ModelAbstract = ModelBuilder.create(param_dict, self.ext_data)
            val: Tuple = (model, StringUtil.get_boolean(param_dict["learning"]))
            model_list.append(val)
        return model_list

    def set_dataset(self, input_data, prev_data):
        for key in input_data.keys():
            try:
                self.input_data[key] = np.array(input_data[key])
            except Exception as e:
                self.LOGGER.error(e, exc_info=True)
                self.input_data[key] = input_data[key]

        if prev_data is None:
            self.prev_data = prev_data
        else:
            self.prev_data = self._make_prev_data(prev_data)

    @staticmethod
    def _make_prev_data(prev_data) -> dict:
        return {"x": prev_data}

    def learn(self) -> None:
        for model, is_learn in self.model_list:
            if is_learn:
                model.learn(self._make_dataset())

    def eval(self) -> None:
        result_list: List[Tuple[int, Union[list, dict]]] = list()

        for idx, (model, is_learn) in enumerate(self.model_list):
            if is_learn:
                tp = (idx, model.eval(self._make_dataset()))
                result_list.append(tp)

        for idx, result in result_list:
            RestManager.post_learn_result(
                job_key=self.param_dict_list[idx]["job_key"],
                task_idx=self.param_dict_list[idx]["task_idx"],
                rst_type=Constants.RST_TYPE_EVAL,
                global_sn=self.param_dict_list[idx]["global_sn"],
                rst=result
            )

    def predict(self, is_rst_return=False) -> Union[List, None]:
        result_list = list()

        for model, is_learn in self.model_list:
            result_list.append(model.predict(self._make_dataset()['x']))

        # self.method_type이 "Parallel"가 아닐경우, self.model_list의 길이는 1
        if is_rst_return and self.method_type != "Parallel":
            if len(result_list) >= 2:
                self.LOGGER.error("Never Occur into this case !!! Trace why result_list is bigger 1")
                raise TypeError
            return result_list[0]
        else:
            for idx, result in enumerate(result_list):
                RestManager.post_inference_result(
                    job_key=self.param_dict_list[idx]["job_key"],
                    task_idx=self.param_dict_list[idx]["task_idx"],
                    global_sn=self.param_dict_list[idx]["global_sn"],
                    rst=result
                )

    def _make_dataset(self) -> dict:
        case = {
            "Basic": "_make_basic_dataset",
            "ModelAttach": "_make_model_attach_dataset",
            "DataAttach": "_make_data_attach_dataset",
            "Parallel": "_make_parallel_dataset"
        }.get(self.method_type, None)

        if case is None:
            self.LOGGER.error("Method Type is None, Interface Not Found...")
            raise ModuleNotFoundError

        return eval(case)()

    def _make_basic_dataset(self) -> dict:
        return self.input_data

    def _make_model_attach_dataset(self) -> dict:
        res_data = dict()
        if "y" in self.input_data.keys():
            res_data["y"] = self.input_data["y"]
        res_data["x"] = self.prev_data["x"]
        return res_data

    def _make_data_attach_dataset(self) -> dict:
        res_data = dict()
        if "y" in self.input_data.keys():
            res_data["y"] = self.input_data["y"]
        res_data["x"] = np.concatenate((self.input_data["x"], self.prev_data["x"]), axis=1)
        return res_data

    def _make_parallel_dataset(self) -> dict:
        res_data = dict()
        if "y" in self.input_data.keys():
            res_data["y"] = self.input_data["y"]
        res_data["x"] = self.prev_data["x"]
        return res_data
