# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team

import re
from mlps.core.RestManager import RestManager


class ConvertManager(object):
    @staticmethod
    def get_cvt_db():
        func_dict_list = RestManager.get_cnvr_dict()
        convert_dict = dict()

        re_exp = "\\[\\[@(.+)\\(\\)\\]\\]"
        p1 = re.compile(re_exp)

        for func_dict in func_dict_list:
            cvt_dict = dict()
            cvt_dict["class"] = func_dict["conv_func_cls"]
            function_nm = p1.match(func_dict["conv_func_tag"]).group(1)

            convert_dict[function_nm] = cvt_dict

        return convert_dict

    @classmethod
    def get_convert_dict(cls):
        return cls.get_cvt_db()

    @staticmethod
    def get_func_nm_regex(convert_dict):
        regex = "\\[\\[@((?:"
        cvt_keys = list(convert_dict.keys())

        for i in range(len(cvt_keys) - 1):
            regex += cvt_keys[i] + "|"

        # regex += cvt_keys[-1] + "))\\((?:'([^']*)')?(?:,\\s*'([^']*)')?\\)\\]\\]"
        regex += cvt_keys[-1] + "))\\((?:'([^']*)')?(?:,\\s*'([^']*)')?(?:,\\s*'([^']*)')?(?:,\\s*'([^']*)')?\\)\\]\\]"
        return regex


if __name__ == '__main__':
    con_dict = {'sign_encode': {'class': 'SignEncode'}, 'trim': {'class': 'Trim'},
                 'special_word_char': {'class': 'SpecialWordChar'}, 'regex_get': {'class': 'RegexGet'},
                 'transform_url2_v2': {'class': 'TransformURL2v2'}, 'longtoip': {'class': 'LongToIP'},
                 'transform_ru_v7': {'class': 'TransformRUv7'}, 'port_normal': {'class': 'PortNormal'},
                 'com_code': {'class': 'ComCodeNormalize'}, 'transform_url2_v4': {'class': 'TransformURL2v4'},
                 'transform_url_v8': {'class': 'TransformURLv8'}, 'transform_ru_v10': {'class': 'TransformRUv10'},
                 'ip_normal': {'class': 'IPNormal'}, 'transform_url_v4': {'class': 'TransformURLv4'},
                 'extract_domain': {'class': 'ExtractDomain'}, 'hex_tostring': {'class': 'HexToString'},
                 'transform_url_v3': {'class': 'TransformURLv3'}, 'transform_url2_v6': {'class': 'TransformURL2v6'},
                 'eqpdt_tokenizer': {'class': 'EqpDtTokenizer'}, 'transform_url_v2': {'class': 'TransformURLv2'},
                 'Tokenizer': {'class': 'Tokenizer'}, 'special_word_char_1': {'class': 'SpecialWordChar_1'},
                 'transform_url_v9': {'class': 'TransformURLv9'}, 'substr': {'class': 'Substr'},
                 'transform_url2_v1': {'class': 'TransformURL2v1'}, 'transform_ru_v6': {'class': 'TransformRUv6'},
                 'transform_url_v1': {'class': 'TransformURLv1'}, 'ifnull': {'class': 'IfNull'},
                 'transform_ru_v14': {'class': 'TransformRUv14'}, 'basic_normal': {'class': 'BasicNormal'},
                 'transform_url2_v7': {'class': 'TransformURL2v7'}, 'tokenizer_1': {'class': 'Tokenizer_1'},
                 'transform_url_v10': {'class': 'TransformURLv10'}, 'touppercase': {'class': 'ToUpperCase'},
                 'replaceall': {'class': 'ReplaceAll'}, 'transform_ru_v13_1': {'class': 'TransformRUv13_1'},
                 'transform_ru_v8': {'class': 'TransformRUv8'}, 'transform_ru_v2': {'class': 'TransformRUv2'},
                 'transform_ru_v5': {'class': 'TransformRUv5'}, 'transform_bt_v1': {'class': 'TransformBTv1'},
                 'date': {'class': 'Date'}, 'stringtomd5': {'class': 'StringToMD5'},
                 'ngram_tokenizer': {'class': 'NgramTokenizer'}, 'special_char_extract': {'class': 'SpecialCharExtract'},
                 'transform_url_v6': {'class': 'TransformURLv6'}, 'zscore_normal': {'class': 'ZScoreNormal'},
                 'not_normal': {'class': 'NotNormal '}, 'transform_url_v7': {'class': 'TransformURLv7'},
                 'minmax_normal': {'class': 'MinMaxNormal'}, 'dev_usage': {'class': 'DevUsage'},
                 'transform_ru_v4': {'class': 'TransformRUv4'}, 'transform_ru_v13': {'class': 'TransformRUv13'},
                 'transform_url_v11': {'class': 'TransformURLv11'}, 'ip_transfer_divide': {'class': 'IPTransferDivide'},
                 'split_special_char': {'class': 'SplitSpecialChar'}, 'unix_timestamp': {'class': 'UnixTimeStamp'},
                 'transform_url2_v3': {'class': 'TransformURL2v3'}, 'transform_url2_v8': {'class': 'TransformURL2v8'},
                 'decimal_scale': {'class': 'DecimalScaleNormal'}, 'tolowercase': {'class': 'ToLowerCase'},
                 'one_hot_encode': {'class': 'OneHotEncode'}, 'transform_url2_v99': {'class': 'TransformURL2v99'},
                 'transform_ru_v9': {'class': 'TransformRUv9'}, 'replace': {'class': 'Replace'},
                 'special_word_char_2': {'class': 'SpecialWordChar_2'}, 'decode_base64': {'class': 'DecodeBase64'},
                 'transform_ru_v11': {'class': 'TransformRUv11'}, 'hex_removeheader': {'class': 'HexRemoveHeader'},
                 'transform_url_v5': {'class': 'TransformURLv5'}, 'transform_url2_v5': {'class': 'TransformURL2v5'},
                 'ip_transfer_merge': {'class': 'IPTransferMerge'}, 'transform_ru_v12': {'class': 'TransformRUv12'},
                 'transform_ru_v3': {'class': 'TransformRUv3'}, 'transform_bt_v2': {'class': 'TransformBTv2'},
                 'transform_ru_v1': {'class': 'TransformRUv1'}, 'sispwc': {'class': 'SISpWC'},
                 'xsspwc': {'class': 'XSSpWC'}, 'xxespwc': {'class': 'XXESpWC'}, 'xispwc': {'class': 'XISpWC'},
                 'ssrfspwc': {'class': 'SSRFSpWC'}, 'ptspwc': {'class': 'PTSpWC'}, 'idspwc': {'class': 'IDSpWC'},
                 'fuspwc': {'class': 'FUSpWC'}, 'fdspwc': {'class': 'FDSpWC'}}

    reg_exp = ConvertManager.get_func_nm_regex(con_dict)

    # fn_string = "[[@ngram_tokenizer()]]"
    # fn_string = "[[@ngram_tokenizer('100')]]"
    # fn_string = "[[@ngram_tokenizer('100','3')]]"
    fn_string = "[[@ngram_tokenizer('100','3','1')]]"
    p1 = re.compile(reg_exp)
    functions = p1.match(fn_string).groups()
    print(functions)
