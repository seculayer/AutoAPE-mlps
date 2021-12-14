#  -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
#  Powered by Seculayer © 2021 Service Model Team, R&D Center.

import os

from mlps.common.Singleton import Singleton
from mlps.common.utils.ConfUtils import ConfUtils
from mlps.common.utils.FileUtils import FileUtils
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

    try:
        VERSION_MANAGER = VersionManagement(app_path=_working_dir)
    except Exception as e:
        # DEFAULT
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
    DIR_JOB = DIR_PROCESSING + _CONFIG.get("dir_job", "/jobs")
    DIR_MODEL = DIR_PROCESSING + _CONFIG.get("dir_model", "/models")
    DIR_LOAD_MODEL = DIR_PROCESSING + _CONFIG.get("dir_load_model", "/load_models")
    DIR_LEARN_FEAT = DIR_PROCESSING + _CONFIG.get("dir_learn_feat", "/features")
    DIR_RESULT = DIR_PROCESSING + _CONFIG.get("dir_result", "/results")
    DIR_TEMP = DIR_PROCESSING + _CONFIG.get("dir_temp", "/temp")
    DIR_ML_TMP = DIR_PROCESSING + _CONFIG.get("dir_ml_tmp", "/temp")
    DIR_ERROR = DIR_PROCESSING + _CONFIG.get("dir_error", "/errors")
    DIR_RESOURCES = (
        FileUtils.get_realpath(file=__file__)
        + "/.."
        + _CONFIG.get("dir_resources", "/resources")
    )
    DIR_USER_CUSTOM_ROOT = _CONFIG.get(
        "user_custom_algorithm_package_root", "/eyeCloudAI/app/ape/custom"
    )
    CUSTOM_PACK_NM = _CONFIG.get("user_custom_converter_package_nm", "cnvrtr")
    DIR_RESOURCES_CNVRTR = DIR_RESOURCES + "/cnvrtr"

    # LOG SETTING
    DIR_LOG = DIR_APP + _CONFIG.get("log_dir", "/logs")
    LOG_NAME = _CONFIG.get("log_name", "MLProcessingServer")
    LOG_LEVEL = _CONFIG.get(
        "log_level", "INFO"
    )  # one of [INFO, DEBUG, WARN, ERROR, CRITICAL]

    # JOB SETTING
    JOB_EXT = _CONFIG.get("job_ext", ".job")

    ETLS_WAITING_TIME = int(_CONFIG.get("etls_wating_time", "5"))

    # REMOVE TEMP FOLDER
    try:
        REMOVE_TEMP_FOLDER = (
            True
            if _CONFIG.get("remove_temp_folder", "true").lower() == "true"
            else False
        )
    except:
        REMOVE_TEMP_FOLDER = False  # AS DEFAULT

    # SUB PROCESS
    MAX_SUB_PROCESS = int(_CONFIG.get("max_sub_process", "12"))

    # DATA LOADER
    DATALOADER_EXT = _CONFIG.get("dataloader_ext", ".done")
    DATALOADER_TIMEOUT = int(_CONFIG.get("dataloader_timeout", "30"))  # second

    # DATA CVT
    try:
        DATAPROCESS_CVT_DATA = (
            True if _CONFIG.get("cvt_data", "True").lower() == "true" else False
        )
    except:
        DATAPROCESS_CVT_DATA = False  # AS DEFAULT

    REST_URL_ROOT = "http://{}:{}".format(
        _CONFIG.get("mrms_svc", "mrms-svc"),
        _CONFIG.get("mrms_rest_port", "9200"),
    )

    # Hosts
    MRMS_SVC = _CONFIG.get("mrms_svc", "mrms-svc")
    MRMS_USER = _CONFIG.get("mrms_username", "HE12RmzKHQtH3bL7tTRqCg==")
    MRMS_PASSWD = _CONFIG.get("mrms_password", "jTf6XrqcYX1SAhv9JUPq+w==")
    MRMS_SFTP_PORT = int(_CONFIG.get("mrms_sftp_port", "10022"))
    MRMS_REST_PORT = int(_CONFIG.get("mrms_rest_port", "9200"))

    JOB_TYPE_LEARN = "learn"
    SAMPLE_TYPE_RANDOM = "1"
    SAMPLE_TYPE_OVER = "2"
    SAMPLE_TYPE_UNDER = "3"
    SAMPLE_TYPE_NONE = "4"

    STATUS_REQ = "1"
    STATUS_START = "2"
    STATUS_RUNNING = "5"
    STATUS_COMPLETE = "6"
    STATUS_ERROR = "7"

    RST_TYPE_LEARN = "1"
    RST_TYPE_EVAL = "2"
    RST_TYPE_RAW = "3"

    # APEFlow Setting
    BATCH_SIZE = int(_CONFIG.get("batch_size", "32"))
    REDIS_SERVER_IP = _CONFIG.get("redis_s2s_ip", "10.1.35.236")
    REDIS_SERVER_PORT = _CONFIG.get("redis_s2s_port", "6379")

    EARLY_TYPE_NONE = "0"
    EARLY_TYPE_MIN = "1"
    EARLY_TYPE_MAX = "2"
    EARLY_TYPE_VAR = "3"

    TF = "TF"
    KERAS = "Keras"
    TFV1 = "TFV1"
    TF_BACKEND_LIST = [TF, KERAS, TFV1]
    TF_BACKEND_V1 = "TFv1"
    TF_BACKEND_V2 = "TFv2"
    TF_BACKEND_NONE = "None"
    GENSIM = "GS"
    SCIKIT_LEARN = "SKL"
    APEFLOW = "APE"
    PYTORCH = "PyTorch"

    TF_DEVICE_CPU = "CPU"
    TF_DEVICE_GPU = "GPU"

    DIST_TYPE_SINGLE = "single"
    DIST_TYPE_DISTRIBUTE = "distribute"

    OUT_MODEL_PB = "pb"
    OUT_MODEL_TF = "tf"
    OUT_MODEL_JSON = "json"
    OUT_MODEL_PKL = "pkl"
    OUT_MODEL_JAVA = "java"
    OUT_MODEL_FOLDER = "folder"
    OUT_MODEL_HYBRID = "hybrid"
    OUT_MODEL_HYBRID_TF = "hybridTF"
    OUT_MODEL_KERAS_TOKENIZER = "kToken"
    OUT_MODEL_APE_OUTLIER_DETCTION = "APE_OUTLIER_DETECTION"
    OUT_MODEL_ONNX = "onnx"  # https://onnx.ai/
    OUT_MODEL_PYTORCH = "PyTorch"

    DATASET_FORMAT_TEXT = "1"
    DATASET_FORMAT_IMAGE = "2"


if __name__ == "__main__":
    print(Constants.__dict__)
