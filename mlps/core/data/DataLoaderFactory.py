# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team

from pycmmn.sftp.SFTPClientManager import SFTPClientManager
from mlps.common.Common import Common
from mlps.common.Constants import Constants
from mlps.info.JobInfo import JobInfo
from mlps.core.data.dataloader.DataLoaderImage import DataLoaderImage
from mlps.core.data.dataloader.DataLoaderText import DataLoaderText


class DataloaderFactory(object):
    LOGGER = Common.LOGGER.getLogger()

    @staticmethod
    def create(dataset_format: str, job_info: JobInfo, sftp_client: SFTPClientManager):
        case = {
            Constants.DATASET_FORMAT_TEXT: "DataLoaderText",
            Constants.DATASET_FORMAT_IMAGE: "DataLoaderImage",
            Constants.DATASET_FORMAT_TABLE: "DataLoaderText"
        }.get(dataset_format)
        return eval(case)(job_info, sftp_client)


if __name__ == '__main__':
    pass
