# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : bmg8551@seculayer.co.kr
# Powered by Seculayer © 2017 AI-TF Team

import math
from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class DecimalScaleNormal(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max = 32767

    def apply(self, data):
        temp_result = 0.0
        length = (math.log10(self.max) + 1)
        length = math.modf(length)[1]
        try:
            temp_result = float(data) / math.pow(10, length)
            # temp_result = round(temp_result, length)
        except Exception as e:
            # print log for error
            self.LOGGER.error(str(e))

        finally:
            # List로 return
            result = list()
            result.append(temp_result)
            return result


if __name__ == "__main__":
    val = 2543
    decimal_scale = DecimalScaleNormal()
    print(decimal_scale.apply(data=val))
