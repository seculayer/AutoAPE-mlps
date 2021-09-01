# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import tensorflow as tf
import os
from mlps.common.Constants import Constants
from mlps.common.Common import Common
from mlps.common.exceptions.TFBackendError import TFBackendError


class TFUtils(object):

    @staticmethod
    def disable_tfv2():
        tf.compat.v1.disable_v2_behavior()
        tf.get_logger().propagate = False

    @staticmethod
    def validate_backend_tf(lib_type_list):
        # 정상 상태 - tfv1
        if Constants.TFV1 in lib_type_list and (
                Constants.KERAS not in lib_type_list and Constants.TF not in lib_type_list):
            return Constants.TF_BACKEND_V1

        # 정상 상태 - tfv2
        elif Constants.TFV1 not in lib_type_list and (
                Constants.KERAS in lib_type_list or Constants.TF in lib_type_list):
            return Constants.TF_BACKEND_V2

        # 혼합 상태 - 지원 안함
        elif Constants.TFV1 in lib_type_list and (Constants.KERAS in lib_type_list or Constants.TF in lib_type_list):
            raise TFBackendError

        # TENSOR FLOW 없음
        else:
            return Constants.TF_BACKEND_NONE

    @staticmethod
    def tf_backend_init(alg_code_list, task_idx):
        # TFFactory.set_cluster(cluster, task_idx, gpu_no)
        # os.environ["CUDA_VISIBLE_DEVICES"] = str(task_idx)

        Common.LOGGER.getLogger().info("TF_CONFIG : {}".format(os.environ["TF_CONFIG"]))

        if os.environ.get("CUDA_VISIBLE_DEVICES", None) is "-1":
            Common.LOGGER.getLogger().info("Running CPU MODE")

        else:
            physical_devices = tf.config.experimental.list_physical_devices('GPU')

            if os.environ.get("CUDA_VISIBLE_DEVICES", None) is None:
                os.environ["CUDA_VISIBLE_DEVICES"] = os.environ.get("NVIDIA_COM_GPU_MEM_IDX", "0")

            if len(physical_devices) != 0:
                # allow growth GPU memory

                Common.LOGGER.getLogger().debug("gpu_no : {}, task_idx : {}, physical devices: {}".format(
                    os.environ["CUDA_VISIBLE_DEVICES"], task_idx, physical_devices
                ))

                if "KDAEOD" in alg_code_list:
                    gpu_weight = 0.7
                else:
                    gpu_weight = 0.25

                # 메모리 제한
                mem_limit = int(int(os.environ.get("NVIDIA_COM_GPU_MEM_CONTAINER", 1024)) * gpu_weight)
                Common.LOGGER.info("GPU Memory Limit Size : {}".format(mem_limit))
                tf.config.experimental.set_memory_growth(physical_devices[0], False)
                tf.config.experimental.set_virtual_device_configuration(
                    physical_devices[0],
                    [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=mem_limit)])
            else:
                Common.LOGGER.getLogger().debug("Physical Devices(GPU) are None")


if __name__ == '__main__':
    TFUtils.disable_tfv2()
