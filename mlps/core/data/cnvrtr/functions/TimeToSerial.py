# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : manki.baek@seculayer.com
# Powered by Seculayer © 2017-2018 AI Core Team, Intelligence R&D Center.

from datetime import datetime

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class TimeToSerial(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_type = int(self.arg_list[0]) # 0 : one day, 1 : one week, 2 : one month
        self.interval = int(self.arg_list[1]) # unit : minute
        if int(self.interval < 1):
            self.interval = 1
        self.num_feat = 1
        self.max_len = 1
        # ["월", "화", "수", "목", "금", "토", "일"]

    def apply(self, data):
        try:
            if len(data) == 14:
                str2datetime = datetime.strptime(data, "%Y%m%d%H%M%S")

            elif len(data) == 15 or len(data) == 16 : # "2019-06-26 0:10"
                str2datetime = datetime.strptime(data, "%Y-%m-%d %H:%M")
            else:
                try:
                    str2datetime = data.split('.')[0]
                except:
                    str2datetime = data[:19]
                str2datetime = datetime.strptime(str2datetime, "%Y-%m-%d %H:%M:%S")

            month = str2datetime.month
            days = str2datetime.day
            hour = str2datetime.hour
            minute = str2datetime.minute

            result = 0.
            if self.input_type == 0: # created during one day
                result = int((hour * 60 + minute) / self.interval) + 1
            elif self.input_type == 1: # created during one week
                week_day = str2datetime.weekday()
                result = int(week_day * (1440 / self.interval)) + \
                         int((hour * 60 + minute) / self.interval) + 1

            else:                 # created during one month
                # TODO
                pass

            result_list = list()
            # self.LOGGER.error("----------result : {}".format(result))
            result_list.append(result)

            return result_list

        except Exception as e :
            # print(e)
            # self.LOGGER.error(e, exc_info=True)
            return [0.]

    def get_num_feat(self):
        return self.max_len


if __name__ == '__main__':
    # data = "hjg yjhg 6ug679t g6guy g321%!#% $^$Fgsdfha"
    # data = "2019-06-26 11:00:05"
    data = "20210324060000"
    data_list = [
        # "2019-06-24 00:00:00",
        # "2019-01-01 0:40",
        # "2019-01-01 12:40",
        # "2019-06-26 00:02:05",
        # "2019-10-01 13:25:06",
        # "2019-06-27 11:00:05.297+0900",
        # "2019-06-28 11:00:06.922+0900",
        # "2019-06-29 11:00:16.367+0900",
        # "2019-06-20 11:00:18.793+0900",
        # "2019-06-30 11:01:14.334+0900",
        # "2019-06-01 11:01:26.254+0900",
        # "2019-06-02 11:02:19.750+0900",
        # "2019-06-02 23:59:19.750+0900",
        # "2019-06-03 11:02:20.798+0900",
        # "2019-06-04 11:03:11.080+0900",
        # "2019-06-05 11:03:17.449+0900",
        # "2019-06-06 23:59:17.494+0900",
        # "20190902200000",
        # "2019-06-26 0:10",
        # "2019-06-26 23:10",
        # "20191002132506",
        "20191001190107",
        "2019-01-01 0:00",
        "2019-07-09 8:10",
        "10/Dec/2019: 12:58:58 +0900"
                     ]
    cvt_fn = TimeToSerial(stat_dict=None, arg_list=[0, 1]) # arg_list : [input_type, interval(minute)]

    rst = cvt_fn.apply(data=data)
    print(rst)
    # for data in data_list:
    #     rst = cvt_fn.apply(data=data)
    #     print(rst)


