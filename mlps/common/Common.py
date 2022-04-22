#  -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
#  Powered by Seculayer © 2021 Service Model Team, R&D Center.
#

import json
from pycmmn.Singleton import Singleton
from pycmmn.utils.FileUtils import FileUtils
from pycmmn.logger.MPLogger import MPLogger
from mlps.common.Constants import Constants


class Common(object, metaclass=Singleton):
    # MAKE DIR
    FileUtils.mkdir(Constants.DIR_LOG)
    FileUtils.mkdir(Constants.DIR_DATA_ROOT)
    FileUtils.mkdir(Constants.DIR_PROCESSING)
    FileUtils.mkdir(Constants.DIR_STORAGE)
    FileUtils.mkdir(Constants.DIR_RESULT)
    FileUtils.mkdir(Constants.DIR_TEMP)
    FileUtils.mkdir(Constants.DIR_ERROR)
    FileUtils.mkdir(Constants.DIR_LOG)

    # LOG SETTING
    LOGGER = MPLogger(log_name=Constants.LOG_NAME, log_level=Constants.LOG_LEVEL, log_dir=Constants.DIR_LOG)
    LOGGER.getLogger().info("MLPS v.%s MLPS Logger initialized..." % Constants.VERSION)


if __name__ == '__main__':
    Common()
