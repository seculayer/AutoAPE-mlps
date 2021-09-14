# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import numpy as np
import tensorflow as tf
from sklearn.cluster import KMeans

from mlps.core.apeflow.api.algorithms.tf.keras.TFKerasAlgAbstract import TFKerasAlgAbstract
from mlps.core.apeflow.interface.utils.tf.keras.StellarGraphUtils import StellarGraphUtils
from mlps.common.exceptions.ParameterError import ParameterError
from mlps.core.apeflow.interface.utils.tf.keras.LearnResultCallback import LearnResultCallback


class KGNN(TFKerasAlgAbstract):
    # MODEL INFORMATION
    ALG_CODE = "KGNN"
    ALG_TYPE = ["OD"]
    DATA_TYPE = ["Single"]
    VERSION = "2.0.0"

    def __init__(self, param_dict, ext_data=None):
        super(KGNN, self).__init__(param_dict, ext_data)
        self.fullbatch_generator = None
        self.gcn_model = None

    def _check_parameter(self, param_dict):
        _param_dict = super(KGNN, self)._check_parameter(param_dict)
        # Parameter Setting
        try:
            _param_dict["act_fn"] = str(param_dict["act_fn"])
            _param_dict["dropout_prob"] = float(param_dict["dropout_prob"])
            _param_dict["layer_size"] = int(param_dict["layer_size"])
            _param_dict["learning_rate"] = float(param_dict["learning_rate"])
            _param_dict["optimizer_fn"] = str(param_dict["optimizer_fn"])
            _param_dict["dist_ratio"] = float(param_dict["dist_ratio"])
        except:
            raise ParameterError
        return _param_dict

    def _build(self):
        pass

    def custom_build(self, x):
        import stellargraph as sg
        act_fn = self.param_dict["act_fn"].lower()
        drop_out = self.param_dict["dropout_prob"]
        layer_size = self.param_dict["layer_size"]
        learning_rate = self.param_dict["learning_rate"]

        optimizer_fn = tf.keras.optimizers.Adam(learning_rate)

        edge = StellarGraphUtils.chsi_radius_edge_embedding(0.7, x)
        nodes = sg.IndexedArray(x, index=list(range(len(x))))

        gm = sg.StellarGraph(nodes, edge)
        self.fullbatch_generator = sg.layer.FullBatchNodeGenerator(gm, sparse=False)
        self.gcn_model = sg.layer.GCN(layer_sizes=[layer_size], activations=[act_fn],
                                      generator=self.fullbatch_generator, dropout=drop_out)
        corrpted_generator = sg.mapper.CorruptedGenerator(self.fullbatch_generator)
        gen = corrpted_generator.flow(gm.nodes())

        # deep infomax in graph
        infomax = sg.layer.DeepGraphInfomax(self.gcn_model, corrpted_generator)
        x_in, x_out = infomax.in_out_tensors()

        self.model = tf.keras.models.Model(inputs=x_in, outputs=x_out)
        self.model.compile(loss=tf.nn.sigmoid_cross_entropy_with_logits, optimizer=optimizer_fn, metrics=['acc'])
        self.model.summary(print_fn=self.LOGGER.info)

        return gen

    def learn(self, dataset):
        return []

    def eval_od(self, dataset):
        x = dataset["x"]

        predicts = self.predict(x)

        return predicts

    def predict(self, data):
        batch_size = 4096
        try:
            x = data["x"]
        except:
            x = data

        start = 0
        results = None

        while start < len(x):
            end = start + batch_size
            if start == 0 and batch_size < len(x):
                batch_x = tf.keras.backend.cast(x[start: end], tf.float32)
                results = self.predict_batch(batch_x)

            elif start == 0 and batch_size >= len(x):
                batch_x = tf.keras.backend.cast(x, tf.float32)
                results = self.predict_batch(batch_x)

            elif end >= len(x):
                batch_x = tf.keras.backend.cast(x[start:], tf.float32)
                results = np.concatenate((results, self.predict_batch(batch_x)), axis=0)

            else:
                batch_x = tf.keras.backend.cast(x[start:end], tf.float32)
                results = np.concatenate((results, self.predict_batch(batch_x)), axis=0)
            start += batch_size
        return results.tolist()

    def predict_batch(self, x):
        x = np.array(x)
        gen = self.custom_build(x)
        global_sn = self.param_dict["global_sn"]
        global_step = self.learn_params["global_step"]
        result_callback = LearnResultCallback(global_sn=global_sn)

        self.model.fit(
            x=gen, epochs=global_step,
            callbacks=[result_callback],
            verbose=1, steps_per_epoch=global_step
        )
        x_emb_in, x_emb_out = self.gcn_model.in_out_tensors()
        x_out = tf.squeeze(x_emb_out, axis=0)
        emb_model = tf.keras.models.Model(inputs=x_emb_in, outputs=x_out)

        gen = self.fullbatch_generator.flow(range(len(x)))
        embeddings = emb_model.predict(gen).tolist()

        # other methods
        kmeans = KMeans(n_clusters=1).fit(embeddings)
        kmeans_cluster_allocation = kmeans.labels_
        kmeans_cluster_centers = kmeans.cluster_centers_

        threshold_for_anomaly = np.quantile(kmeans.transform(embeddings), self.param_dict["dist_ratio"])

        result = list()
        for idx, emb in enumerate(embeddings):
            data_point = emb
            data_point_cluster_center = np.array(kmeans_cluster_centers[kmeans_cluster_allocation[idx]])
            k = data_point - data_point_cluster_center
            distance = (np.dot(k, k)) ** 0.5

            if distance > threshold_for_anomaly:
                result.append([1, distance])
            else:
                result.append([0, distance])

        return np.array(result)

    def eval(self, data):
        results = list()
        result = {"global_sn": self.param_dict["global_sn"],
                  "predicts": self.predict(data["x"])}

        results.append(result)
        return results


if __name__ == '__main__':
    # CLASSIFIER

    # physical_devices = tf.config.experimental.list_physical_devices('GPU')
    # print("physical devices: ", physical_devices)
    # for gpu_no in range(4):
    #     tf.config.experimental.set_memory_growth(physical_devices[gpu_no], True)
    __param_dict = {
        "algorithm_code": "KGNN",
        "algorithm_type": "OD",
        "data_type": "Single",
        "method_type": "Basic",
        "global_step": "10",
        "model_nm": "APEOUTLIERDETECTION-TEST",
        "alg_sn": "0",
        "job_type": "learn",
        "depth": "0",
        "global_sn": "0",
        "early_type": "0",
        "params": {
            "input_units": "2",
            "output_units": "1",
            "dropout_prob": "0.1",
            "act_fn": "ReLU",
            "layer_size": "3",
            "optimizer_fn": "Adam",
            "learning_rate": "0.01",
            "dist_ratio": "0.9"
        },
        "num_workers": "1"
    }

    __dataset = {
        "x": np.array([[-1., -1.], [-2., -1.], [1., 1.], [2., 1.]]),
        "y": np.array([[0.5, 0.5], [0.8, 0.2], [0.3, 0.7], [0.1, 0.9]]),
    }

    temp = KGNN(__param_dict)
    temp.load_model()

    eval_data = {"x": np.array([[3., 2.], [-1., -1.], [-2., -1.], [1., 1.], [2., 1.],
                                [0.5, 0.5], [0.8, 0.2], [0.3, 0.7], [0.1, 0.9], [3, 4]])}
    print(temp.predict(eval_data))
