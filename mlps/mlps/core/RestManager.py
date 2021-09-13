# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import requests as rq
import json
from typing import List, Union
from mlps.common.Common import Common
from mlps.common.Constants import Constants
from mlps.common.Singleton import Singleton


class RestManager(object, metaclass=Singleton):

    @staticmethod
    def get(url) -> str:
        response = rq.get(url)

        return response.text

    @staticmethod
    def post(url: str, data: dict) -> rq.Response:
        response = rq.post(url, json=data)

        return response

    @staticmethod
    def get_cnvr_dict() -> dict:
        url = Constants.REST_URL_ROOT + Common.REST_URL_DICT.get("cnvr_list", [])
        return json.loads(RestManager.get(url))

    @staticmethod
    def update_status_cd(status: str, job_key: str, task_idx: str, msg: str) -> None:
        url = Common.REST_URL_DICT.get("learn_status_update", "")
        obj = {
            "status": status,
            "job_key": job_key,
            "task_idx": task_idx,
            "message": msg
        }
        RestManager.post(url=url, data=obj)

    @staticmethod
    def post_learn_result(job_key: str, task_idx: str, rst_type: str, global_sn: str, rst: dict):
        url = Common.REST_URL_DICT.get("learn_result_return", "")
        obj = {
            "job_key": job_key,
            "task_idx": task_idx,
            "rst_type": rst_type,
            "global_sn": global_sn,
            "result": rst
        }
        RestManager.post(url=url, data=obj)

    @staticmethod
    def post_inference_result(job_key: str, task_idx: str, global_sn: str, rst: List[Union[list, dict, int, str]]):
        url = Common.REST_URL_DICT.get("inference_result_return", "")
        obj = {
            "job_key": job_key,
            "task_idx": task_idx,
            "global_sn": global_sn,
            "result": rst
        }
        RestManager.post(url=url, data=obj)


