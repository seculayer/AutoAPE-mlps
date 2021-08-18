#  -*- coding: utf-8 -*-
#  Author : Manki Baek
#  e-mail : manki.baek@seculayer.com
#  Powered by Seculayer © 2021 Service Model Team, R&D Center.
#
import shutil
import datetime
import threading
import time

from pycmmn.common.Singleton import Singleton
from pycmmn.interfaces.FileUtils import FileUtils
from mlps.common.Common import Common
from mlps.common.Constants import Constants


class Utils(object, metaclass=Singleton):

    @staticmethod
    def move_key_folder(dir_org, dir_tmp, job_key, filename):
        src_filename = "%s/%s" % (dir_org, filename)
        tmp_folder = "%s/%s" % (dir_tmp, job_key)
        FileUtils.mkdir(tmp_folder)
        dst_filename = "%s/%s" % (tmp_folder, filename)
        shutil.move(src_filename, dst_filename)

    @staticmethod
    def rm_key_folder(dir_dst, job_key):
        FileUtils.remove_dir(dir_name="{}/{}".format(dir_dst, job_key))
        Common.LOGGER.getLogger().info("remove temp folder : [{}]".format("{}/{}".format(dir_dst, job_key)))

    @staticmethod
    def move_error_folder(job_key):
        src_folder = "{}/{}".format(Constants.DIR_ML_TMP, job_key)
        dst_folder = "{}/{}".format(Constants.DIR_ERROR, job_key)
        try:
            shutil.move(src=src_folder, dst=dst_folder)
            Common.LOGGER.getLogger().info("temp folder moved. src-[{}] dst-[{}]".format(src_folder, dst_folder))
        except shutil.Error as e:
            Common.LOGGER.getLogger().debug(e, exc_info=True)

    @staticmethod
    def get_model_type(model_type_cd):
        # APE003 : 모델 타입
        try:
            return Constants.COM_CODE["APE003"][str(model_type_cd)]
        except Exception as e:
            Common.LOGGER.getLogger().error(str(e))
            return None

    @staticmethod
    def get_dataset_type(data_type_cd):
        # APE004 : 데이터셋 타입
        try:
            return Constants.COM_CODE["APE004"][str(data_type_cd)]
        except Exception as e:
            Common.LOGGER.getLogger().error(str(e))
            return None

    @staticmethod
    def get_method_type(method_type_cd):
        # APE005 : 앙상블 메소드 타입
        try:
            return Constants.COM_CODE["APE005"][str(method_type_cd)]
        except Exception as e:
            Common.LOGGER.getLogger().error(str(e))
            return None

    @staticmethod
    def get_sampling_type(sample_type_cd):
        # APE005 : 앙상블 메소드 타입
        try:
            return Constants.COM_CODE["APE007"][str(sample_type_cd)]
        except Exception as e:
            Common.LOGGER.getLogger().error(str(e))
            return None

    @staticmethod
    def make_timer(max_time=5):
        return Timer(max_time=max_time)

    @staticmethod
    def get_current_time():
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    @staticmethod
    def get_current_time_without_sec():
        return datetime.datetime.now().strftime("%Y%m%d%H%M")

    @staticmethod
    def get_current_time_with_mili_sec():
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")


class Timer(threading.Thread):
    def __init__(self, max_time=5):
        threading.Thread.__init__(self)

        self.mlps_logger = Common.LOGGER.getLogger()
        self._suspend = False
        self._exit = False

        self.MAX_TIME = max_time
        self.CURRENT_TIME = 0
        self.SAVE_TIME = 0

    def run(self):
        while self._exit is False:
            self.CURRENT_TIME = time.time()
            time.sleep(0.5)

    def set_time(self):
        self.SAVE_TIME = time.time()

    def timeout(self):
        if self.CURRENT_TIME - self.SAVE_TIME > self.MAX_TIME:
            # self.mlps_logger.info("timer exit")
            return True
        else:
            return False

    def suspend(self):
        self._suspend = True

    def resume(self):
        self._suspend = False

    def exit(self):
        self._exit = True
