# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import tensorflow as tf

from mlps.common.Singleton import Singleton


class TFDistributeRunnerV2(metaclass=Singleton):
    # TensorFlow 2.0 분산처리 Wrapper Class
    # for tf.keras.model and tf.Module
    def __init__(self):
        self.strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy(
            communication=tf.distribute.experimental.CommunicationImplementation.RING
        )
        # self.strategy=tf.distribute.experimental.CentralStorageStrategy()

    def get_strategy(self):
        return self.strategy


if __name__ == '__main__':
    pass
