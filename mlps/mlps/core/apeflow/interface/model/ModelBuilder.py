# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

from mlps.common.Constants import Constants
from mlps.core.apeflow.api.algorithms.AlgorithmFactory import AlgorithmFactory
from mlps.core.apeflow.interface.model.TFModel import TFModel
from mlps.core.apeflow.interface.model.SKLModel import SKLModel
from mlps.core.apeflow.interface.model.GSModel import GSModel
from mlps.core.apeflow.interface.model.APEModel import APEModel


class ModelBuilder(object):
    @staticmethod
    def create(param_dict, ext_data=None):
        alg_code = param_dict["algorithm_code"]
        lib_type = AlgorithmFactory.get_lib_type(alg_code)
        if lib_type in Constants.TF_BACKEND_LIST:
            return TFModel(param_dict, ext_data)
        elif lib_type == Constants.SCIKIT_LEARN:
            return SKLModel(param_dict, ext_data)
        elif lib_type == Constants.GENSIM:
            return GSModel(param_dict, ext_data)
        elif lib_type == Constants.APEFLOW:
            return APEModel(param_dict, ext_data)
