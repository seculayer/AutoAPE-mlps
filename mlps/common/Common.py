#  -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
#  Powered by Seculayer © 2021 Service Model Team, R&D Center.
#

import json
from mlps.common.Singleton import Singleton
from mlps.common.utils.FileUtils import FileUtils
from mlps.common.logger.MPLogger import MPLogger
from mlps.common.utils.StringUtil import StringUtil
from mlps.common.Constants import Constants


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
    FileUtils.mkdir(Constants.DIR_LOG)
    FileUtils.mkdir(Constants.DIR_USER_CUSTOM_ROOT)
    FileUtils.mkdir(Constants.DIR_USER_CUSTOM_ROOT + "/{}".format(Constants.CUSTOM_PACK_NM))

    CNVRTR_PACK_LIST = [
        "mlps.core.data.cnvrtr.functions",
        Constants.CUSTOM_PACK_NM
    ]

    with open(Constants.DIR_RESOURCES + "/com_code.json", "r") as f:
        COM_CODE = json.load(f)

    with open(Constants.DIR_RESOURCES + "/com_func.json", "r") as f:
        COMMON_FUNC = json.load(f)

    with open(Constants.DIR_RESOURCES + "/rest_url_info.json", "r") as f:
        REST_URL_DICT = json.load(f)

    ACTIVATE_FN_CODE_DICT = COMMON_FUNC.get("activation_fn_code")
    CONV_FN_CODE_DICT = COMMON_FUNC.get("conv_fn_code")
    POOLING_FN_CODE_DICT = COMMON_FUNC.get("pooling_fn_code")
    UPSAMPLING_FN_CODE_DICT = COMMON_FUNC.get("upsample_fn_code")
    OPTIMIZER_FN_CODE_DICT = COMMON_FUNC.get("optimizer_fn_code")

    # LOG SETTING
    LOGGER = MPLogger(log_name=Constants.LOG_NAME, log_level=Constants.LOG_LEVEL, log_dir=Constants.DIR_LOG)
    LOGGER.getLogger().info("MLPS v.%s MLPS Logger initialized..." % Constants.VERSION)

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
