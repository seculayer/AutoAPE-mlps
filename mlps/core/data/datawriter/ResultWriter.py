# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2017 AI-TF Team
######################################################################################
import os
import json
import socket

from pycmmn.utils.Utils import Utils
from pycmmn.utils.FileUtils import FileUtils
######################################################################################


# class : ResultWriterAbstract
class ResultWriter(object):
    @staticmethod
    def result_file_write(**kwargs):
        result_path = kwargs["result_path"]
        results = kwargs["results"]
        result_type = kwargs["result_type"]
        host_name = socket.gethostname()

        file_name = f"{result_path}/{result_type}_{Utils.get_current_time_with_mili_sec()}_{host_name}"

        len_results = len(results)
        # Common.LOGGER.getLogger().info("[{}] : {} rows".format(file_name, len_results))
        if len_results == 0:
            return

        # write json
        start = 0
        batch_size = 20000
        idx = 0
        while start <= len_results:
            if start + batch_size < len_results:
                batch_result = results[start: start + batch_size]
            else:
                batch_result = results[start:]

            # Common.LOGGER.getLogger().info("[{}_{}] : {} rows".format(file_name, idx, len(batch_result)))
            f = FileUtils.file_pointer("{}_{}.tmp".format(file_name, idx), "w")
            line_idx = 0
            for line in batch_result:
                # json.dump(line, codecs.getwriter("utf-8")(f) , ensure_ascii=False)
                if line.__contains__('image'):
                    line.pop('image')
                json.dump(line, f, ensure_ascii=False)
                f.write("\n")

                if line_idx % 5000 == 0:
                    f.flush()
                line_idx += 1

            f.close()
            # rename
            # os.rename("{}_{}.tmp".format(file_name, idx), "{}_{}.{}".format(file_name, idx, ext))
            os.rename("{}_{}.tmp".format(file_name, idx), "{}_{}.{}".format(file_name, idx, "done"))
            # Common.LOGGER.getLogger().info("{} result file write complete - {}_{}.{}".format(ext, file_name, idx, "done"))
            start += batch_size
            idx += 1
