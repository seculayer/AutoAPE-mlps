#  -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
#  Powered by Seculayer © 2021 Service Model Team, R&D Center.

import os

from pycmmn.Singleton import Singleton
from pycmmn.utils.ConfUtils import ConfUtils
from pycmmn.utils.FileUtils import FileUtils
from pycmmn.tools.VersionManagement import VersionManagement


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
    DIR_RESULT = DIR_PROCESSING + _CONFIG.get("dir_result", "/results")
    DIR_TEMP = DIR_PROCESSING + _CONFIG.get("dir_temp", "/temp")
    DIR_ERROR = DIR_PROCESSING + _CONFIG.get("dir_error", "/errors")
    DIR_RESOURCES = (
        FileUtils.get_realpath(file=__file__)
        + "/.."
        + _CONFIG.get("dir_resources", "/resources")
    )

    # LOG SETTING
    DIR_LOG = DIR_APP + _CONFIG.get("log_dir", "/logs")
    LOG_NAME = _CONFIG.get("log_name", "MLProcessingServer")
    LOG_LEVEL = _CONFIG.get(
        "log_level", "INFO"
    )  # one of [INFO, DEBUG, WARN, ERROR, CRITICAL]

    ETLS_WAITING_TIME = int(_CONFIG.get("etls_waiting_time", "5"))

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

    # DATA CVT
    try:
        DATAPROCESS_CVT_DATA = (
            True if _CONFIG.get("cvt_data", "True").lower() == "true" else False
        )
    except:
        DATAPROCESS_CVT_DATA = False  # AS DEFAULT

    JOB_TYPE_LEARN = "learn"
    JOB_TYPE_INFERENCE = "inference"

    SAMPLE_TYPE_RANDOM = "1"
    SAMPLE_TYPE_OVER = "2"
    SAMPLE_TYPE_UNDER = "3"
    SAMPLE_TYPE_NONE = "4"

    STATUS_REQ = "1"
    STATUS_START = "2"
    STATUS_RUNNING = "5"
    STATUS_COMPLETE = "6"
    STATUS_ERROR = "7"

    DATASET_FORMAT_TEXT = "1"
    DATASET_FORMAT_IMAGE = "2"
    DATASET_FORMAT_TABLE = "3"

    # TABLE FIELD TYPE
    FIELD_TYPE_NULL = "null"
    FIELD_TYPE_INT = "int"
    FIELD_TYPE_FLOAT = "float"
    FIELD_TYPE_STRING = "string"
    FIELD_TYPE_IMAGE = "image"
    FIELD_TYPE_DATE = "date"
    FIELD_TYPE_LIST = "list"

if __name__ == "__main__":
    print(Constants.__dict__)
