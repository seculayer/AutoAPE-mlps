# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import random
import numpy as np
from typing import List, Callable

from mlps.common.Common import Common
from mlps.common.Constants import Constants
from mlps.common.info import JobInfo


class DataSampler(object):
    def __init__(self, job_info: JobInfo):

        self.LOGGER = Common.LOGGER.getLogger()
        self.job_info = job_info

        self.features = list()
        self.labels = list()
        self.origin_data = list()

        self.min_lines = min(self.job_info.get_dataset_lines())
        try:
            self.cnt_label_lines: dict = self.job_info.get_dataset_cnt_labels()
        except:
            self.cnt_label_lines: dict = {}

    def set_data(self, data_list):
        self.features = data_list[0]
        self.labels = data_list[1]
        self.origin_data = data_list[2]

    def sampling(self):
        self.LOGGER.info("Data Sampler Start ...")
        sample_type_code = self.job_info.get_sampling_type()

        case: Callable = {
            Constants.SAMPLE_TYPE_NONE: self._none_sampling,
            Constants.SAMPLE_TYPE_RANDOM: self._random_sampling,
            Constants.SAMPLE_TYPE_OVER: self._over_sampling,
            Constants.SAMPLE_TYPE_UNDER: self._under_sampling
        }.get(sample_type_code, self._random_sampling)

        rst = case()
        self.LOGGER.info("Data Sampler End ...")

        return rst

    def _none_sampling(self) -> List[List[object]]:
        self.features = self.features[: self.min_lines]
        self.labels = self.labels[: self.min_lines]
        self.origin_data = self.origin_data[: self.min_lines]

        return [
            [self.features, self.labels],
            [self.features, self.labels],
            self.origin_data
        ]

    def _random_sampling(self) -> List[List[object]]:
        # data_len = len(self.features)
        data_len = self.min_lines
        sample_ratio = self.job_info.get_sampling_ratio()
        index_list = list(range(data_len))

        random.shuffle(index_list)

        # Sampling
        num_learn_idx = int(data_len * sample_ratio)
        # learning set
        learn_idx_list = index_list[0: num_learn_idx]
        # evaluate set
        eval_idx_list = index_list[num_learn_idx:]

        learn_data = [[self.features[idx] for idx in learn_idx_list],
                      [self.labels[idx] for idx in learn_idx_list]]
        eval_data = [[self.features[idx] for idx in eval_idx_list],
                     [self.labels[idx] for idx in eval_idx_list]]
        sampled_json_data = [self.origin_data[idx] for idx in eval_idx_list]

        return [learn_data, eval_data, sampled_json_data]

    def _under_sampling(self) -> List[List[object]]:
        [learn_data, eval_data, sampled_json_data] = self._random_sampling()

        n_class_idx_dict = self.cnt_label_idx(learn_data)
        num_classes = len(n_class_idx_dict)

        # Under Sampling
        min_num_data = -1
        # for sub_list in n_class_idx_dict.values():
        #     if (len(sub_list) < min_num_data) or min_num_data == -1:
        #         min_num_data = len(sub_list)
        for key in n_class_idx_dict.keys():
            len_key = len(n_class_idx_dict[key])
            if min_num_data > len_key or min_num_data == -1:
                min_num_data = len_key

        total_choice = list()
        for no_class in range(num_classes):
            class_data_len = len(n_class_idx_dict[str(no_class)])
            if min_num_data < class_data_len:
                try:
                    n_class_idx_dict[str(no_class)] = n_class_idx_dict[str(no_class)][:min_num_data]
                except:
                    self.LOGGER.error('failed to random_choice (data list of {}_class is empty)'.format(no_class))

            total_choice += n_class_idx_dict[str(no_class)]
        random.shuffle(total_choice)
        learn_data = np.take(learn_data, total_choice, axis=1)
        learn_data = [list(val) for val in learn_data]

        self.LOGGER.info("Data cnt of under sampling result : {}".format(len(learn_data[0])))
        return [learn_data, eval_data, sampled_json_data]

    def _over_sampling(self) -> List[List[object]]:
        [learn_data, eval_data, sampled_json_data] = self._random_sampling()

        n_class_idx_dict = self.cnt_label_idx(learn_data)
        num_classes = len(n_class_idx_dict)

        # Over Sampling
        # len_arr = [len(x) for x in n_class_idx_dict.values()]
        # max_num_data = max(len_arr)
        max_num_data = -1
        for key in n_class_idx_dict.keys():
            len_key = len(n_class_idx_dict[key])
            if max_num_data < len_key:
                max_num_data = len_key

        total_choice = list()
        for no_class in range(num_classes):
            class_data_len = len(n_class_idx_dict[str(no_class)])
            if max_num_data > class_data_len:
                try:
                    random_choice = list(np.random.choice(n_class_idx_dict[str(no_class)], max_num_data - class_data_len))
                except:
                    self.LOGGER.error('failed to choice (data list of {}_class is empty)'.format(no_class))
                    random_choice = []
                n_class_idx_dict[str(no_class)] += random_choice

            total_choice += n_class_idx_dict[str(no_class)]
        random.shuffle(total_choice)
        learn_data = np.take(learn_data, total_choice, axis=1)
        learn_data = [list(val) for val in learn_data]

        self.LOGGER.info("Data cnt of over sampling result : {}".format(len(learn_data[0])))
        return [learn_data, eval_data, sampled_json_data]

    def cnt_label_idx(self, learn_data) -> dict:
        labels_encoded = None
        try:
            # if one_hot data
            if len(learn_data[1][0]) >= 2:
                labels_encoded = list(np.argmax(learn_data[1], 1))
            else:
                labels_encoded = [0 for label in learn_data[1]]
        except Exception as e:
            self.LOGGER.error(e, exc_info=True)
            labels_encoded = [0]

        num_classes = max(labels_encoded) + 1

        n_class_idx_dict = dict()
        for i in range(num_classes):
            n_class_idx_dict["{}".format(i)] = list()

        for idx in range(len(labels_encoded)):
            try:
                n_class_idx_dict["{}".format(labels_encoded[idx])].append(idx)
            except:
                self.LOGGER.error("sampling : index list add error")

        return n_class_idx_dict
