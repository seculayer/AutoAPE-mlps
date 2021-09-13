# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team, R&D Center.
import os
import json
import joblib

from keras_preprocessing.text import tokenizer_from_json
from mlps.common.utils.FileUtils import FileUtils
from mlps.common.Constants import Constants
from mlps.common.Common import Common
from mlps.common.exceptions.NotSupportTypeError import NotSupportTypeError


class TFSavedModel(object):

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
        if model.task_idx != 0:
            return
        param_dict = model.param_dict

        dir_model = '{}/{}/{}'.format(
            Constants.DIR_TEMP, param_dict["model_nm"], param_dict["alg_sn"]
        )

        cls.init(dir_model, param_dict)

        try:
            out_model_type = cls._set_out_model_type(model)

            save_fn = {
                Constants.OUT_MODEL_TF: "cls._save_model_keras" if model.LIB_TYPE == Constants.KERAS else "-",
                Constants.OUT_MODEL_JSON: "cls._save_model_json",
                Constants.OUT_MODEL_KERAS_TOKENIZER: "cls._save_model_keras_tokenizer",
                Constants.OUT_MODEL_APE_OUTLIER_DETCTION: "cls._save_model_ape_outlier_detection"
            }
            try:
                eval(save_fn[out_model_type])(model, dir_model)
            except Exception as e:
                Common.LOGGER.getLogger().error(e, exc_info=True)
                raise NotSupportTypeError(algorithm_type=out_model_type)

            # REMOVE BACKUP-MODEL
            try:
                if cls._check_dir_model(dir_model + "_prev"):
                    FileUtils.remove_dir(dir_model + "_prev")
            except Exception as e:
                Common.LOGGER.getLogger().error(str(e), exc_info=True)

            Common.LOGGER.getLogger().info("model saved ....")
            Common.LOGGER.getLogger().info("model dir : {}".format(dir_model))

        except Exception as e:
            Common.LOGGER.getLogger().error(str(e), exc_info=True)
            # RESTORE
            try:
                FileUtils.remove_dir(dir_model)
                FileUtils.move_dir(dir_model + "_prev", dir_model)
            except Exception as e:
                Common.LOGGER.getLogger().error(str(e), exc_info=True)

    @classmethod
    def _check_dir_model(cls, dir_model):
        return os.path.exists(dir_model)

    @staticmethod
    def _save_model_keras(model, dir_model):
        model.model.save_weights(dir_model + '/weights.h5', save_format='h5')

    @staticmethod
    def _save_model_json(model, dir_model):
        FileUtils.mkdir(dir_model)
        model_dict = model.model
        model_dict["ALG_CODE"] = model.ALG_CODE
        model_dict["ALG_TYPE"] = model.param_dict["algorithm_type"]
        model_nm = "{}/apeflow_json".format(dir_model)
        f = FileUtils.file_pointer("{}.tmp".format(model_nm), "w")
        try:
            json.dump(model_dict, f, indent=4)
        except Exception as e:
            Common.LOGGER.getLogger().error(e, exc_info=True)
        finally:
            f.close()
        os.rename("{}.tmp".format(model_nm), "{}.model".format(model_nm))

    @staticmethod
    def _save_model_keras_tokenizer(model, dir_model):
        FileUtils.mkdir(dir_model)
        model_nm = "{}/apeflow_json".format(dir_model)
        f = FileUtils.file_pointer("{}.tmp".format(model_nm), "w")
        try:
            f.write(model.model.to_json())
        except Exception as e:
            Common.LOGGER.getLogger().error(e, exc_info=True)
        finally:
            f.close()
        os.rename("{}.tmp".format(model_nm), "{}.model".format(model_nm))

    @classmethod
    def _save_model_ape_outlier_detection(cls, model, dir_model):
        cls._save_model_keras(model.model, dir_model)
        model_nm = "{}/outlier_kmeans".format(dir_model)
        joblib.dump(model.kmeans_model, "{}.pkl".format(model_nm))
        result_dict = dict()
        result_dict["ALG_CODE"] = model.ALG_CODE
        result_dict["ALG_TYPE"] = model.param_dict["algorithm_type"]
        result_dict["max_distances"] = model.max_distances

        f = FileUtils.file_pointer("{}.tmp".format(model_nm), "w")
        try:
            json.dump(result_dict, f, indent=4)
        except Exception as e:
            Common.LOGGER.getLogger().error(e, exc_info=True)
        finally:
            f.close()
        os.rename("{}.tmp".format(model_nm), "{}.json".format(model_nm))

    @classmethod
    def _set_out_model_type(cls, model):
        try:
            out_model_type = model.OUT_MODEL_TYPE
        except:
            # 하위 호환
            out_model_type = Constants.OUT_MODEL_TF

        return out_model_type

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
                out_model_type = cls._set_out_model_type(model)

                load_fn = {
                    Constants.OUT_MODEL_TF: "cls._load_model_keras" if model.LIB_TYPE == Constants.KERAS else "-",
                    Constants.OUT_MODEL_JSON: "cls._load_model_json",
                    Constants.OUT_MODEL_KERAS_TOKENIZER: "cls._load_model_keras_tokenizer",
                    Constants.OUT_MODEL_APE_OUTLIER_DETCTION: "cls._load_model_ape_outlier_detection"
                }
                try:
                    eval(load_fn[out_model_type])(model, dir_model)
                except Exception as e:
                    Common.LOGGER.getLogger().error(e, exc_info=True)
                    raise NotSupportTypeError(algorithm_type=out_model_type)

                Common.LOGGER.getLogger().info("model load ....")
                Common.LOGGER.getLogger().info("model dir : {}".format(dir_model))

            except Exception as e:
                Common.LOGGER.getLogger().warn(str(e), exc_info=True)
        else:
            Common.LOGGER.getLogger().warn("MODEL FILE IS NOT EXIST : [{}]".format(dir_model))

    @staticmethod
    def _load_model_keras(model, dir_model):
        try:
            model.model.load_weights(dir_model + '/weights.h5')
        except Exception as e:
            Common.LOGGER.getLogger().error(e, exc_info=True)

    @staticmethod
    def _load_model_json(model, dir_model):
        model_nm = "{}/apeflow_json".format(dir_model)
        f = FileUtils.file_pointer("{}.model".format(model_nm), "r")
        try:
            model.model = json.load(f)
        except Exception as e:
            Common.LOGGER.getLogger().error(e, exc_info=True)
        finally:
            f.close()

    @staticmethod
    def _load_model_keras_tokenizer(model, dir_model):
        model_nm = "{}/apeflow_json".format(dir_model)
        f = FileUtils.file_pointer("{}.model".format(model_nm), "r")
        try:
            data = f.read()
            model.model = tokenizer_from_json(data)
        except Exception as e:
            Common.LOGGER.getLogger().error(e, exc_info=True)
        finally:
            f.close()

    @classmethod
    def _load_model_ape_outlier_detection(cls, model, dir_model):
        model_nm = "{}/outlier_kmeans".format(dir_model)
        cls._load_model_keras(model.model, dir_model)
        model.kmeans_model = joblib.load("{}.pkl".format(model_nm))

        f = FileUtils.file_pointer("{}.json".format(model_nm), "r")
        try:
            model.max_distances = json.load(f).get("max_distances")
        except Exception as e:
            Common.LOGGER.getLogger().error(e, exc_info=True)
        finally:
            f.close()
