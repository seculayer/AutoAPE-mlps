# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import paramiko
from mlps.common.crypto.AES256 import AES256
from mlps.common.sftp.PySFTPAuthException import PySFTPAuthException


class PySFTPClient(object):
    # class : PySFTPClient
    def __init__(self, host: str, port: int, username: str, password: str):
        try:
            self.transport = paramiko.Transport((host, port))
            self.transport.connect(username=AES256().decrypt(username), password=AES256().decrypt(password))
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        except paramiko.ssh_exception.AuthenticationException:
            raise PySFTPAuthException

    def open(self, filename, option="r",) -> paramiko.SFTPFile:
        return self.sftp.open(filename, option)

    def close(self):
        self.sftp.close()
        self.transport.close()

    def rename(self, src, dst):
        self.sftp.rename(src, dst)


if __name__ == '__main__':
    sftp_client = PySFTPClient("localhost", 22, "Kmw/y3YWiiO7gJ/zqMvCuw==", "jTf6XrqcYX1SAhv9JUPq+w==")
    with sftp_client.open("/home/seculayer/temp.tmp", "w") as f:
        f.write("test.1" + "\n")

    with sftp_client.open("/home/seculayer/temp.tmp", "r") as f:
        for line in f.readlines():
            print(line)
    sftp_client.close()
