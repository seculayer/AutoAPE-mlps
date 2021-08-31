# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import time

from mlps.common.Constants import Constants
from mlps.common.Common import Common
from mlps.core.MLPSProcessor import MLPSProcessor


class MLProcessingServer(object):
    LOGGER = Common.LOGGER.getLogger()

    def __init__(self, key, task_idx, job_type) -> None:
        self.key: str = key
        self.task_idx: str = task_idx
        self.job_type: str = job_type

        self.LOGGER.info(Constants.VERSION_MANAGER.print_version())

        # waiting ETLS
        time.sleep(3)

        self.processor = MLPSProcessor(key, task_idx, job_type)
        
    def run(self) -> None:
        self.processor.run()


if __name__ == '__main__':
    import sys
    _key = sys.argv[1]
    _task_idx = sys.argv[2]
    _job_type = sys.argv[3]

    mlps = MLProcessingServer(_key, _task_idx, _job_type)
    mlps.run()
