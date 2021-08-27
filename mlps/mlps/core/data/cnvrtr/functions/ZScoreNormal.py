# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : bmg8551@seculayer.co.kr
# Powered by Seculayer © 2017 AI-TF Team

######################################################################################
###### import modules ######
### python basic
### MLPS
from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


######################################################################################
# class : ZScoreNormal
class ZScoreNormal(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.mean = self.stat_dict["avg"]    ## the mean of the normal distribution
            self.stddev = self.stat_dict["stddev"]       ## the standard deviation of the normal distribution
        except:
            self.mean = 0
            self.stddev = 0

    def apply(self, data):
        try:
            if self.stddev == 0:
                self.stddev = 1
                self.LOGGER.warn("Standard Deviation value is zero")
            temp_result = (float(data) - float(self.mean)) / float(self.stddev)
        except Exception as e:
            ## print log for error
            self.LOGGER.getLogger().error(str(e))
            temp_result = [0.0]
        ## List return
        result = list()
        result.append(temp_result)
        return result


if __name__ == "__main__":
    val = 2
    zscr_normal = ZScoreNormal(stat_dict={"avg" : 1, "stddev" : 0.1}, arg_list=list())
    print(zscr_normal.apply(val))