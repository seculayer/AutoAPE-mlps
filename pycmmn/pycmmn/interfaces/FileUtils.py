# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team
######################################################################################

import os
import shutil


class FileUtils(object):
    @staticmethod
    def mkdir(dir_name):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    @staticmethod
    def get_realpath(file=None):
        return os.path.dirname(os.path.realpath(file))

    @classmethod
    def remove_dir(cls, dir_name):
        if cls.is_exist(dir_name):
            shutil.rmtree(dir_name)

    @staticmethod
    def is_exist(file):
        return os.path.exists(file)

    @staticmethod
    def file_pointer(filename, mode):
        return open(filename, mode, encoding='UTF-8', errors='ignore')


if __name__ == '__main__':
    pass
