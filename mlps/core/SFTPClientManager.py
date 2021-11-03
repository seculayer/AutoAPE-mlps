# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.
import json
from typing import List

from mlps.common.sftp.PySFTPClient import PySFTPClient
from mlps.common.Constants import Constants
from mlps.common.Common import Common


class SFTPClientManager(object):
    # class : SFTPClientManager
    def __init__(self, service: str, username: str, password: str):
        self.logger = Common.LOGGER.get_logger()
        self.service: List[str] = service.split(":")
        self.username = username
        self.password = password

        self.sftp_client = PySFTPClient(self.service[0], int(self.service[1]),
                                        self.username, self.password)

        self.logger.info("initialized service - [{}] SFTP Client Initialized.".format(service))

    def get_client(self) -> PySFTPClient:
        return self.sftp_client

    def rename(self, src, dst) -> None:
        self.sftp_client.rename(src, dst)

    def close(self) -> None:
        self.sftp_client.close()

    def load_json_data(self, filename):
        f = self.get_client().open(filename, "r")
        json_data = json.loads(f.read())
        f.close()
        return json_data


if __name__ == '__main__':
    SFTPClientManager(Constants.MRMS_SVC, Constants.MRMS_USER, Constants.MRMS_PASSWD)
