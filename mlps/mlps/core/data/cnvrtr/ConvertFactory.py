# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team

from mlps.core.data.cnvrtr import ConvertAbstract
from mlps.tools.DynamicClassLoader import DynamicClassLoader
from mlps.common.info.ConvertFunctionInfo import ConvertFunctionInfo
from mlps.common.Common import Common
from mlps.core.data.cnvrtr.ConvertManager import ConvertManager


class ConvertFactory(object):
    LOGGER = Common.LOGGER.getLogger()
    CVT_DICT = ConvertManager.get_convert_dict()

    @classmethod
    def create_cvt_fn(cls, cvt_fn_info: ConvertFunctionInfo, cvt_dict=None) -> ConvertAbstract:
        fn_tag = cvt_fn_info.get_fn_str()
        if cvt_dict is None:
            cvt_dict = cls.CVT_DICT
        class_nm = cvt_dict.get(
            fn_tag, {'not_normal': {"class": "NotNormal"}}) \
            .get("class", "NotNormal")

        fn_args = cvt_fn_info.get_fn_args()
        stat_dict = cvt_fn_info.get_stat_dict()

        try:
            return DynamicClassLoader.load_multi_packages(packages=Common.CNVRTR_PACK_LIST,
                                                          class_nm=class_nm)(arg_list=fn_args, stat_dict=stat_dict)
        except Exception as e:
            cls.LOGGER.warn(str(e), exc_info=True)
            return DynamicClassLoader.load_multi_packages(packages=Common.CNVRTR_PACK_LIST,
                                                          class_nm="NotNormal")(arg_list=list(), stat_dict=dict())


if __name__ == '__main__':
    pass
