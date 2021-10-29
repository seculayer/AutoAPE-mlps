# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : manki.baek@seculayer.com
# Powered by Seculayer © 2017-2018 AI Core Team, Intelligence R&D Center.

from mlps.core.data.cnvrtr.ConvertAbstract import ConvertAbstract


class String2ASCII(ConvertAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_len = int(self.arg_list[0])
        self.seq_len = int(self.arg_list[1])
        self.num_feat = self.max_len

    def apply(self, row):
        try:
            feature = list()
            for idx, word in enumerate(row):
                if idx >= self.seq_len:
                    break
                feature.append(self.cvt_ascii(word, self.max_len))

            if len(feature) < self.seq_len:
                interval = self.seq_len - len(feature)
                for idx in range(interval):
                    feature.append([0 for i in range(self.max_len)])
            return feature

        except Exception as e:
            # print(e)
            self.LOGGER.error(e, exc_info=True)
            return [0.] * self.max_len

    @staticmethod
    def cvt_ascii(data, max_length):
        word = list()
        for idx, c in enumerate(str(data)):
            if idx >= max_length:
                break

            word.append(ord(c))

        if len(word) < max_length:
            word += [0 for i in range(max_length-len(word))]
        return word

    def get_num_feat(self):
        return self.max_len


if __name__ == '__main__':
    # data = "hjg yjhg 6ug679t g6guy g321%!#% $^$Fgsdfha"
    _data = ["0", "53018000", "20140523173202"]
    cvt_fn = String2ASCII(stat_dict=None, arg_list=[5, 3])

    rst = cvt_fn.apply(row=_data)
    print(rst)
    print(len(rst))
