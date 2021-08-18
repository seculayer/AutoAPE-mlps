#  -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
#  Powered by Seculayer © 2021 Service Model Team, R&D Center.
#

from typing import Tuple, List
import os

# ----  pycmmn
from pycmmn.common.Singleton import Singleton
from pycmmn.interfaces.FileUtils import FileUtils
from pycmmn.logger.MPLogger import MPLogger
from pycmmn.common.StringUtil import StringUtil

# ----  mlps
from mlps.common.Constants import Constants


# class : Common
class Common(object, metaclass=Singleton):
    # MAKE DIR
    FileUtils.mkdir(Constants.DIR_LOG)
    FileUtils.mkdir(Constants.DIR_DATA_ROOT)
    FileUtils.mkdir(Constants.DIR_PROCESSING)
    FileUtils.mkdir(Constants.DIR_STORAGE)
    FileUtils.mkdir(Constants.DIR_LEARN_FEAT)
    FileUtils.mkdir(Constants.DIR_MODEL)
    FileUtils.mkdir(Constants.DIR_LOAD_MODEL)
    FileUtils.mkdir(Constants.DIR_RESULT)
    FileUtils.mkdir(Constants.DIR_ML_TMP)
    FileUtils.mkdir(Constants.DIR_ERROR)

    # LOG SETTING
    LOGGER = MPLogger(log_name=Constants.LOG_NAME, log_level=Constants.LOG_LEVEL, log_dir=Constants.DIR_LOG)
    LOGGER.getLogger().info("MLPS v.%s MLPS Logger initialized..." % Constants.VERSION)

    @classmethod
    def get_feature_files(cls, directory="./", sep="_", info=None, ext=".done", filename_list=None) \
            -> Tuple[List[str], int]:
        if info is None:
            info = []
        if filename_list is None:
            filename_list = []

        file_list = os.listdir(directory)
        result_list = list()
        max_files = 1
        for filename in file_list:
            filename_split = os.path.splitext(filename)
            if ext == filename_split[-1]:
                if cls.match_feature_filename(filename_split[0], info, sep):
                    full_filename = "%s/%s" % (directory, filename)
                    if not cls.check_duplicate_filenames(full_filename, filename_list):
                        max_files = cls.get_max_files(filename_split[0], sep) + 1
                        result_list.append(full_filename)
                else:
                    continue
        return result_list, max_files

    @staticmethod
    def get_max_files(filename, sep="_") -> int:
        data = filename.split(sep)
        return StringUtil.get_int(data[-1])

    @staticmethod
    def match_feature_filename(filename, info=None, sep="_") -> bool:
        if info is None:
            info = []

        data = filename.split(sep)
        # hist_no, task_idx, dataset_idx
        if (data[0] == info[0]) and (data[1] == info[1]) and (data[2] == info[2]):
            return True
        else:
            return False

    @staticmethod
    def check_duplicate_filenames(filename, filename_list):
        if filename in filename_list:
            return True
        else:
            return False


if __name__ == '__main__':
    Common()
