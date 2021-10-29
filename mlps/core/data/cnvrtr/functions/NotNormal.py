# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : bmg8551@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class NotNormal(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.num_feat = 1

    def apply(self, data):
        try:
            # CRLF
            try:
                data = data.replace("[\r\n]+", "#CRLF#")
                # data = data.replace("\r\n", "#CRLF#").replace("\n", "#CRLF#").replace("\r", "#CRLF#")
                # comma
                data = data.replace("\\,", "#COMMA#" )

                try:
                    data = float(data)
                except:
                    pass
            except:
                pass

        except Exception as e:
            # print log for error
            self.LOGGER.error(e)
        # List return
        result = list()

        result.append(data)
        return result


if __name__ == "__main__":
    _str = "Hello\\,\\,\\,World!\r\n+"
    not_nor = NotNormal(stat_dict=None, arg_list=None)
    _str = not_nor.apply(data=_str)
    print(_str)
