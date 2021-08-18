#  -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
#  Powered by Seculayer © 2021 Service Model Team, R&D Center.

import os

#  pycmmn
from pycmmn.common.Singleton import Singleton
from pycmmn.interfaces.FileUtils import FileUtils
from pycmmn.tools.ConfUtils import ConfUtils
from pycmmn.tools.VersionManagement import VersionManagement


# class : Constants
class Constants(object, metaclass=Singleton):
    _WORKING_DIR = os.getcwd()
    _WORKING_DIR = _WORKING_DIR[:_WORKING_DIR.find("/mlps/")+5]  # +5 : "/mlps"

    # load configuration file
    _conf_xml_filename = _WORKING_DIR + "/conf/mlps-conf.xml"
    _CONFIG = ConfUtils.load(filename=_conf_xml_filename)

    # DEFAULT
    try:
        VERSION_MANAGER = VersionManagement(app_path=_WORKING_DIR)
    except Exception as e:
        VersionManagement.generate(
            version="3.0.0",
            app_path=_WORKING_DIR,
            module_nm="mlps",
        )
        VERSION_MANAGER = VersionManagement(app_path=_WORKING_DIR)
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
    DIR_RESOURCES = FileUtils.get_realpath(file=__file__) + "/../../" + _CONFIG.get("dir_resources", "/resources")

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

    COM_CODE = {
        "APE003": {
            "1": "Classifier",
            "2": "Regressor",
            "3": "Clustering",
            "4": "WE",
            "5": "DR",
            "6": "FE",
            "7": "OD",
            "8": "STS",
            "9": "DNSD",
            "10": "TA"
        },
        "APE004": {
            "1": "Single",
            "2": "TimeSeries"
        },
        "APE005": {
            "1": "Basic",
            "2": "DataAttach",
            "3": "ModelAttach",
            "4": "Parallel"
        },
        "APE007": {
            "1": "RandomSampling",
            "2": "OverSampling",
            "3": "UnderSampling",
            "4": "NoneSampling"
        }
    }


if __name__ == '__main__':
    print(Constants._CONFIG)

