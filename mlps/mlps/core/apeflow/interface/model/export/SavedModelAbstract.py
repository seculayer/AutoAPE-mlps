# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import os
from typing import Callable

from mlps.common.Constants import Constants
from mlps.common.Common import Common
from mlps.common.utils.FileUtils import FileUtils
from mlps.common.exceptions.NotSupportTypeError import NotSupportTypeError


class SavedModelAbstract(object):
    LOGGER = Common.LOGGER.getLogger()

    @classmethod
    def init(cls, dir_model, param_dict):
        if cls._check_dir_model(dir_model):
            try:
                # backup
                FileUtils.move_dir(dir_model, dir_model + "_prev")
                FileUtils.mkdir('{}/{}/{}'.format(Constants.DIR_TEMP, param_dict["model_nm"], param_dict["alg_sn"]))
            except Exception as e:
                Common.LOGGER.getLogger().error(str(e), exc_info=True)
        else:
            if not FileUtils.is_exist('{}/{}'.format(Constants.DIR_TEMP, param_dict["model_nm"])):
                FileUtils.mkdir('{}/{}'.format(Constants.DIR_TEMP, param_dict["model_nm"]))
                FileUtils.mkdir('{}/{}/{}'.format(Constants.DIR_TEMP, param_dict["model_nm"], param_dict["alg_sn"]))

    @classmethod
    def save(cls, model):
        param_dict = model.param_dict

        dir_model = '{}/{}/{}'.format(
            Constants.DIR_TEMP, param_dict["model_nm"], param_dict["alg_sn"]
        )
        try:
            cls.init(dir_model, param_dict)
            case: Callable = cls._save_case_fn(model)

            try:
                case(model, dir_model)
            except Exception as e:
                cls.LOGGER.error(e, exc_info=True)
                raise NotSupportTypeError(algorithm_type=model.OUT_MODEL_TYPE)

            cls._remove_backup(dir_model)
        except Exception as e:
            cls.LOGGER.error(str(e), exc_info=True)
            # RESTORE
            try:
                FileUtils.remove_dir(dir_model)
                FileUtils.move_dir(dir_model + "_prev", dir_model)
            except Exception as e:
                cls.LOGGER.error(str(e), exc_info=True)

    @classmethod
    def _save_case_fn(cls, model) -> Callable:
        raise NotImplementedError

    @classmethod
    def _remove_backup(cls, dir_model) -> None:
        # REMOVE BACKUP-MODEL
        try:
            if cls._check_dir_model(dir_model + "_prev"):
                FileUtils.remove_dir(dir_model + "_prev")
        except Exception as e:
            cls.LOGGER.error(str(e), exc_info=True)

        cls.LOGGER.info("model saved ....")
        cls.LOGGER.info("model dir : {}".format(dir_model))

    @classmethod
    def _check_dir_model(cls, dir_model):
        return os.path.exists(dir_model)

    @classmethod
    def load(cls, model):
        param_dict = model.param_dict
        dir_model = '{}/{}/{}'.format(
            Constants.DIR_TEMP, param_dict["model_nm"], param_dict["alg_sn"]
        )

        if not cls._check_dir_model(dir_model):
            dir_model = '{}/{}/{}'.format(
                Constants.DIR_LOAD_MODEL, param_dict["model_nm"], param_dict["alg_sn"]
            )

        if cls._check_dir_model(dir_model):
            try:
                case: Callable = cls._load_case_fn(model)
                try:
                    case(model, dir_model)
                except Exception as e:
                    cls.LOGGER.error(e, exc_info=True)
                    raise NotSupportTypeError(algorithm_type=model.OUT_MODEL_TYPE)

                cls.LOGGER.info("model load ....")
                cls.LOGGER.info("model dir : {}".format(dir_model))
            except Exception as e:
                cls.LOGGER.warn(str(e), exc_info=True)
        else:
            cls.LOGGER.warn("MODEL FILE IS NOT EXIST : [{}]".format(dir_model))

    @classmethod
    def _load_case_fn(cls, model) -> Callable:
        raise NotImplementedError
