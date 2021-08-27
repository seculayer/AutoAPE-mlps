#  -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
#  Powered by Seculayer © 2021 Service Model Team, R&D Center.

import os
import json

#  pycmmn
from mlps.common.Singleton import Singleton
from mlps.common.utils.FileUtils import FileUtils
from mlps.common.utils.ConfUtils import ConfUtils
from mlps.tools.VersionManagement import VersionManagement


class Constants(object, metaclass=Singleton):
    _working_dir = os.getcwd()
    _data_cvt_dir = _working_dir + "/../mlps"
    _conf_xml_filename = _data_cvt_dir + "/conf/mlps-conf.xml"

    _MODE = "deploy"

    if not FileUtils.is_exist(_conf_xml_filename):
        _MODE = "dev"

        if _working_dir != "/eyeCloudAI/app/ape/mlps":
            os.chdir(FileUtils.get_realpath(__file__) + "/../../")

        _working_dir = os.getcwd()
        _data_cvt_dir = _working_dir + "/../mlps"
        _conf_xml_filename = _working_dir + "/conf/mlps-conf.xml"

    _CONFIG = ConfUtils.load(filename=_conf_xml_filename)

    # DEFAULT
    try:
        VERSION_MANAGER = VersionManagement(app_path=_working_dir)
    except Exception as e:
        VersionManagement.generate(
            version="3.0.0",
            app_path=_working_dir,
            module_nm="mlps",
        )
        VERSION_MANAGER = VersionManagement(app_path=_working_dir)
    VERSION = VERSION_MANAGER.VERSION
    MODULE_NM = VERSION_MANAGER.MODULE_NM

    # DIRECTORY SETTING
    DIR_APP = _CONFIG.get("app_dir", "/eyeCloudAI")
    DIR_MLPS = DIR_APP + _CONFIG.get("app_modules", "/app/ape/mlps")
    DIR_DATA_ROOT = DIR_APP + _CONFIG.get("dir_data_root", "/data")
    DIR_PROCESSING = DIR_DATA_ROOT + _CONFIG.get("dir_processing", "/processing/ape")
    DIR_STORAGE = DIR_DATA_ROOT + _CONFIG.get("dir_storage", "/storage/ape")
    DIR_JOB = DIR_PROCESSING + _CONFIG.get("dir_job", "/models")
    DIR_MODEL = DIR_PROCESSING + _CONFIG.get("dir_model", "/models")
    DIR_LOAD_MODEL = DIR_PROCESSING + _CONFIG.get("dir_load_model", "/load_models")
    DIR_LEARN_FEAT = DIR_PROCESSING + _CONFIG.get("dir_learn_feat", "/features")
    DIR_RESULT = DIR_PROCESSING + _CONFIG.get("dir_result", "/results")
    DIR_ML_TMP = DIR_PROCESSING + _CONFIG.get("dir_ml_tmp", "/temp")
    DIR_ERROR = DIR_PROCESSING + _CONFIG.get("dir_error", "/errors")
    DIR_RESOURCES = FileUtils.get_realpath(file=__file__) + "/.." + _CONFIG.get("dir_resources", "/resources")
    DIR_USER_CUSTOM_ROOT = _CONFIG.get("user_custom_algorithm_package_root", "/eyeCloudAI/app/ape/custom")
    CUSTOM_PACK_NM = _CONFIG.get("user_custom_converter_package_nm", "cnvrtr")
    DIR_RESOURCES_CNVRTR = DIR_RESOURCES + "/cnvrtr"

    # LOG SETTING
    DIR_LOG = DIR_APP + _CONFIG.get("log_dir", "/logs")
    LOG_NAME = _CONFIG.get("log_name", "MLProcessingServer")
    LOG_LEVEL = _CONFIG.get("log_level", "INFO")  # one of [INFO, DEBUG, WARN, ERROR, CRITICAL]

    # JOB SETTING
    JOB_EXT = _CONFIG.get("job_ext", ".job")

    # REMOVE TEMP FOLDER
    try:
        REMOVE_TEMP_FOLDER = True if _CONFIG.get("remove_temp_folder", "true").lower() == "true" else False
    except:
        REMOVE_TEMP_FOLDER = False  # AS DEFAULT

    # SUB PROCESS
    MAX_SUB_PROCESS = int(_CONFIG.get("max_sub_process", "12"))

    # DATA LOADER
    DATALOADER_EXT = _CONFIG.get("dataloader_ext", ".done")
    DATALOADER_TIMEOUT = int(_CONFIG.get("dataloader_timeout", "30"))  # second

    # DATA CVT
    try:
        DATAPROCESS_CVT_DATA = True if _CONFIG.get("cvt_data", "True").lower() == "true" else False
    except:
        DATAPROCESS_CVT_DATA = False  # AS DEFAULT

    JOB_TYPE_LEARN = "learn"
    SAMPLE_TYPE_RANDOM = "1"
    SAMPLE_TYPE_OVER = "2"
    SAMPLE_TYPE_UNDER = "3"
    SAMPLE_TYPE_NONE = "4"

    REST_URL_ROOT = "https://{}:{}".format(
        _CONFIG.get("rest_server_ip", "10.1.35.231"),
        _CONFIG.get("rest_server_port", "5543"))

    with open(DIR_RESOURCES + "/rest_url_info.json", "r") as f:
        REST_URL_DICT = json.load(f)

    with open(DIR_RESOURCES + "/com_code.json", "r") as f:
        COM_CODE = json.load(f)

    STATUS_LEARNING = 5
    STATUS_LEARN_COMPLETE = 6
    STATUS_LEARN_ERROR = 7
    STATUS_EVALUATING = 8
    STATUS_EVALUATE_COMPLETE = 9
    STATUS_EVALUATE_ERROR = 10
    STATUS_DATA_CONVERTING = 18
    STATUS_DATA_CONVERT_ERROR = 19


if __name__ == '__main__':
    print(Constants.__dict__)
