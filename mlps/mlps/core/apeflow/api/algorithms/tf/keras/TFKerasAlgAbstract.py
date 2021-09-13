# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import json
import os
import numpy as np
import tensorflow as tf

from mlps.common.Constants import Constants
from mlps.core.apeflow.interface.model.export.TFSavedModel import TFSavedModel
from mlps.core.apeflow.api.algorithms.AlgorithmAbstract import AlgorithmAbstract
from mlps.core.apeflow.interface.utils.tf.keras.LearnResultCallback import LearnResultCallback
from mlps.core.apeflow.interface.utils.tf.keras.EarlyStopCallback import EarlyStopCallback


class TFKerasAlgAbstract(AlgorithmAbstract):
    # MODEL INFORMATION (STATIC)
    ALG_CODE = "TFKerasAlgAbstract"
    ALG_TYPE = []
    DATA_TYPE = []
    VERSION = "2.0.0"
    LIB_TYPE = Constants.KERAS
    TAG = "serve"
    OUT_MODEL_TYPE = Constants.OUT_MODEL_TF

    def __init__(self, param_dict, ext_data=None):
        AlgorithmAbstract.__init__(self, param_dict, ext_data=ext_data)

        self.parallel_step = None
        self.num_workers = param_dict["num_workers"]

        self.input_name = "{}_{}_inputs".format(param_dict["model_nm"], param_dict["alg_sn"])
        self.output_name = "{}_{}_predicts".format(param_dict["model_nm"], param_dict["alg_sn"])

        # VARIABLES
        self.model = None
        try:
            self.task_idx = int(json.loads(os.environ["TF_CONFIG"])["task"]["index"])
        except:
            self.task_idx = 0

        # -- build model
        self._build()
        self.model.built = True

    def _build(self):
        raise NotImplementedError

    def _make_train_dataset(self, data):
        len_data = len(data["x"])
        try:
            data["x"] = data["x"].astype(np.float32)
        except:
            pass
        buffer_size = len_data

        # if buffer_size % global_batch_size != 0 :
        if buffer_size % self.batch_size != 0:
            self.parallel_step = buffer_size // self.batch_size + 1
            # self.parallel_step += int(self.task_idx)
        else:
            self.parallel_step = buffer_size // self.batch_size
            # self.parallel_step += int(self.task_idx)

        if "y" in data.keys():
            try:
                if "Regressor" in self.ALG_TYPE:
                    data["y"] = np.array(data["y"], dtype=np.float32)
                else:
                    data["y"] = np.array(data["y"])
            except:
                pass

            dataset = tf.data.Dataset.from_tensor_slices(
                (data["x"], data["y"])
            ).shuffle(
                buffer_size=self.batch_size
            ).repeat().batch(
                self.batch_size  # , drop_remainder=drop_remainder
            )

        else:
            dataset = tf.data.Dataset.from_tensor_slices(
                (data["x"])
            ).shuffle(
                buffer_size=self.batch_size
            ).repeat().batch(
                self.batch_size  # , drop_remainder=drop_remainder
            )

        # data shard option 해제
        options = tf.data.Options()
        options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.OFF
        dataset = dataset.with_options(options)
        return dataset

    def saved_model(self):
        TFSavedModel.save(self)

    def load_model(self):
        TFSavedModel.load(self)

    def learn(self, dataset):
        # learn result
        global_step = self.learn_params["global_step"]
        global_sn = self.param_dict["global_sn"]
        result_callback = LearnResultCallback(
            global_sn=global_sn,
            job_key=self.param_dict["job_key"]
        )

        # early stop
        early_stop_callback = EarlyStopCallback(self.learn_params)
        self.model.fit(
            x=self._make_train_dataset(dataset),
            epochs=global_step,
            callbacks=[result_callback, early_stop_callback],
            verbose=1, steps_per_epoch=self.parallel_step
        )

    def predict(self, x):
        batch_size = self.batch_size
        start = 0
        results = None

        while start < len(x):
            end = start + batch_size
            if start == 0 and batch_size < len(x):
                batch_x = tf.keras.backend.cast(x[start: end], tf.float32)
                results = self.model(batch_x).numpy()

            elif start == 0 and batch_size >= len(x):
                batch_x = tf.keras.backend.cast(x, tf.float32)
                results = self.model(batch_x).numpy()

            elif end >= len(x):
                batch_x = tf.keras.backend.cast(x[start:], tf.float32)
                results = np.concatenate((results, self.model(batch_x).numpy()), axis=0)

            else:
                batch_x = tf.keras.backend.cast(x[start:end], tf.float32)
                results = np.concatenate((results, self.model(batch_x).numpy()), axis=0)
            start += batch_size

        return results

    def eval_default_rst(self, dataset):
        x = dataset["x"]

        pred = self.predict(x)
        try:
            pred = pred.tolist()
        except:
            pass

        return pred

    def eval_regressor(self, dataset):
        return self.eval_default_rst(dataset)

    def eval_fe(self, dataset):
        return self.eval_default_rst(dataset)

    def eval_od(self, dataset):
        result_list = list()

        return result_list
