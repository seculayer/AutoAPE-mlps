# -*- coding: utf-8 -*-
# Author : Manki Baek
# e-mail : manki.baek@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

import tensorflow as tf
import numpy as np
import os
import re
import random
import json
from urllib import parse
from datetime import datetime

from mlps.common.utils.FileUtils import FileUtils
from mlps.core.data.cnvrtr.functions.SWC_KDAEOD import SWC_KDAEOD
from mlps.common.Common import Common
from mlps.common.Constants import Constants
from mlps.common.exceptions.ParameterError import ParameterError
from mlps.core.apeflow.api.algorithms.tf.keras.TFKerasAlgAbstract import TFKerasAlgAbstract
from mlps.core.apeflow.interface.utils.tf.keras.LearnResultCallback import LearnResultCallback
from mlps.core.apeflow.interface.utils.tf.keras.EarlyStopCallback import EarlyStopCallback
from mlps.common.exceptions.NotSupportTypeError import NotSupportTypeError


class KDAEOD(TFKerasAlgAbstract):
    # MODEL INFORMATION
    ALG_CODE = "KDAEOD"
    ALG_TYPE = ["OD"]
    DATA_TYPE = ["Single"]
    VERSION = "1.0.0"

    # data 로 입력받은 정보 인덱스 (상수)
    _CONST_HOST_DOMAIN_IDX = 0  # host domain
    _CONST_URL_IDX = 1  # url
    _CONST_URL2_IDX = 2  # url2
    _CONST_BT_IDX = 3  # browser type

    def __init__(self, param_dict, ext_data=None):
        super(KDAEOD, self).__init__(param_dict, ext_data)
        self.rmse = None

        self.stopped_epoch = None

        start_time = datetime.now()
        # 공통 사용 변수
        self.file_ext_list = ['bmp', 'rle', 'dib', 'jpg', 'jpeg', 'gif', 'png', 'tif', 'tiff', 'svg', 'ico', 'mp3', 'mp4',
                              'caf',
                              'avi', 'mkv', 'wmv', 'swf',
                              'woff', 'woff2', 'eot', 'otf', 'ttf', 'pdf', 'ppt', 'pptx', 'doc', 'docx', 'xls', 'xlsx',
                              'hwp',
                              'scss', 'css', 'js', 'map', 'zip']

        # value 체크 관련 정규식 정리
        # value에 등장해도 되는 확장자 정의
        self.img_list = ['(.bmp', '.rle', '.dib', '.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff', '.svg', '.ico', '.mp3',
                         '.mp4', '.ai',
                         '.caf', '.avi', '.mkv', '.wmv', '.swf', '.woff', '.woff2', '.eot', '.otf', '.ttf)']
        self.img_conn = ')|(\\'.join(self.img_list)
        self.img_regx = '^[^/]*(' + self.img_conn + ')$'
        self.img_path_regx = '^(/)?([a-zA-Z0_-]+/)+[^/]+(' + self.img_conn + ')$'
        self.img_domain_regx = '^(http:|https:)//([a-zA-Z0-9_-]+.)+(kr|net|org|com)(:[0-9]{2,4})?(/)([a-zA-Z0_-]+/)+[^/]+(' + self.img_conn + ')$'

        self.doc_list = ['(.pdf', '.ppt', '.pptx', '.doc', '.docx', '.xls', '.xlsx', '.hwp', '.zip', '.csv)']
        self.doc_conn = ')|(\\'.join(self.doc_list)
        self.doc_regx = '^[^/]*(' + self.doc_conn + ')$'
        self.doc_path_regx = '^(/)?([a-zA-Z0_-]+/)+[^/]+(' + self.doc_conn + ')$'
        self.doc_domain_regx = '^(http:|https:)//([a-zA-Z0-9_-]+.)+(kr|net|org|com)(:[0-9]{2,4})?(/)([a-zA-Z0_-]+/)+[^/]+(' + self.doc_conn + ')$'

        self.han_0_regexp = re.compile(r'[ㄱ-ㅎㅏ-ㅣ가-힣]')  # 검색키워드 (한글이 있는 경우 ex:주소, 검색어)    7_searchword
        self.ext_0_regex = re.compile(r'[ㄱ-ㅎㅏ-ㅣ가-힣\W_]')
        self.englower_0_regexp = re.compile(r'[a-z]')
        self.engupper_0_regexp = re.compile(r'[A-Z]')
        self.num_0_regexp = re.compile(r'[0-9]')

        self.val_1_regexp = re.compile(r'^[0]+$')  # 숫자                 1_number
        self.val_2_regexp = re.compile(r'^[0]+[0.]+[0]+$')  # 숫자 + 기호(.)       1_numdot

        self.val_3_regexp = re.compile(r'^[a-z]+_[0]+$')  # 영어 + 언더바 + 숫자 (순서 중요) 구성      2_idNum3
        self.val_4_regexp = re.compile(r'^[a-z_]+$')  # 영어 + 언더바                            2_engUnd2
        self.val_5_regexp = re.compile(r'^[0a-z_-]+$')  # 영어 + 숫자 구성                         2_engNum1

        self.val_6_regexp = re.compile(self.img_regx)  # 파일 (문서 파일)로 구성된 경우            3_filetypeI
        self.val_6_2_regexp = re.compile(self.img_path_regx)  # 경로 + 파일 (이미지 파일)로 구성된 경우  3_pathfileI
        self.val_6_3_regexp = re.compile(self.img_domain_regx)  # 도메인 + 경로 + 파일 (이미지 파일)로 구성된 경우 3_domainfileI

        self.val_7_regexp = re.compile(self.doc_regx)  # 파일 (문서 파일)로 구성된 경우                  3_filetypeD
        self.val_7_2_regexp = re.compile(self.doc_regx)  # 경로 + 파일 (문서 파일)로 구성된 경우            3_pathfileD
        self.val_7_3_regexp = re.compile(self.doc_regx)  # 도메인 + 경로 + 파일 (문서 파일)로 구성된 경우    3_domainfileD

        self.val_8_regexp = re.compile(
            r'^(http://|https://)?([a-zA-Z0-9_-]+\.)+(kr|net|com)(:[0-9]{2,4})?$')  # 도메인 정규식2 ex)10.23.2.33 4_domain
        self.val_9_regexp = re.compile(
            r'^(http://|https://)?([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})(:[0-9]{2,4})?$')  # 도메인 정규식1 ex)www.naver.com     4_url

        self.val_10_regexp = re.compile(r'^(/)?([a-zA-Z0_-]+/)+[a-zA-Z0_\-.]+')  # URL 경로 + 파일     5_urlpath1
        self.val_11_regexp = re.compile(
            r'^(http://|https://)?([a-zA-Z0-9_-]+\.)+(kr|net|com)(:[0-9]{2,4})?(/)([a-zA-Z0_-]+/)*[a-zA-Z0_\-.]+')  # URL 경로    5_urlpath2
        self.val_12_regexp = re.compile(
            r'^(http://|https://)?([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})(:[0-9]{2,4})?(/)([a-zA-Z0_-]+/)*[a-zA-Z0_\-.]+')  # URL 경로    5_urlpath3

        self.val_13_regexp = re.compile(
            r'^[a-zA-Z0-9]([\\._-]?[a-zA-Z0-9])*@[a-zA-Z0-9]([\\._-]?[a-zA-Z0-9])*\.(kr|net|com)$')  # 이메일 형태    6_email1

        self.val_14_regexp = re.compile(r'^<(.)+:(.)+>(.)*</(.)+>$')  # xml 형태 정의            8_xml
        self.val_15_regexp = re.compile(r'^{\}$')  # xml 형태 정의            8_xml

        self.val_16_regexp = re.compile(
            r'^{\"[a-zA-Z0-9_-]+\":\"([a-zA-Z0-9_-]*|[a-zA-Z0-9]([\\._-]?[a-zA-Z0-9])*@[a-zA-Z0-9]([\\._-]?[a-zA-Z0-9])*\.(kr|net|com))\"$')  # json 형태     9_json
        self.val_17_regexp = re.compile(
            r'^\"[a-zA-Z0-9_-]+\":\"([a-zA-Z0-9_-]*|[a-zA-Z0-9]([\\._-]?[a-zA-Z0-9])*@[a-zA-Z0-9]([\\._-]?[a-zA-Z0-9])*\.(kr|net|com))\"$')  # json 형태     9_json
        self.val_18_regexp = re.compile(
            r'^\"[a-zA-Z0-9_-]+\":\"([a-zA-Z0-9_-]*|[a-zA-Z0-9]([\\._-]?[a-zA-Z0-9])*@[a-zA-Z0-9]([\\._-]?[a-zA-Z0-9])*\.(kr|net|com))\"\}$')  # json 형태     9_json
        self.val_19_regexp = re.compile(r'^{\}$')  # json 형태     9_json
        self.val_20_regexp = re.compile(r'^\[\]$')  # json 형태     9_json

        self.val_21_regexp = re.compile(r'^[a-zA-Z0+/]+=$')  # 마지막이 = 이고, 영어 + 숫자 + 슬래시 + '+'    10_hash1
        self.val_22_regexp = re.compile(r'^[a-zA-Z0+/]+==$')  # 마지막이 == 이고, 영어 + 숫자 + 슬래시 + '+'   10_hash2

        self.val_23_regexp = re.compile(r'^[a-z]+[a-z.]+[a-z]$')  # 영어 + 기호(.) 구성      2_engdot

        self.file_0_regex = re.compile(r'^[0._-]+$')  # 0 + 기호(.) + 언더바 + 하이
        self.file_1_regex = re.compile(r'^[a._-]+$')  # a + 기호(.) + 언더바 + 하이
        self.file_2_regex = re.compile(r'^[0a-zA-Z._-]+$')  # 0 + 알파벳 + 기호(.) + 언더바 + 하이

        self.path_0_regex = re.compile(r'^[0._-]+$')  # 0 + 기호(.) + 언더바 + 하이
        self.path_1_regex = re.compile(r'^[0a-zA-Z._-]+$')  # 0 + 알파벳 + 기호(.) + 언더바 + 하이

        self.int_regexp = re.compile(r'^[0-9]+$')
        # end_time = datetime.now()
        # self.LOGGER.info("re compile time : {}".format(end_time - start_time))

    def _check_parameter(self, param_dict):
        _param_dict = super(KDAEOD, self)._check_parameter(param_dict)

        # Parameter Setting
        try:
            _param_dict["act_fn"] = str(param_dict["act_fn"])
            _param_dict["algorithm_type"] = str(param_dict["algorithm_type"])

            _param_dict["dropout_prob"] = float(param_dict["dropout_prob"])
            _param_dict["hidden_units"] = list(map(int, str(param_dict["hidden_units"]).split(",")))
            _param_dict["optimizer_fn"] = str(param_dict["optimizer_fn"])
            _param_dict["learning_rate"] = float(param_dict["learning_rate"])
        except:
            raise ParameterError
        return _param_dict

    def _build(self):
        # Parameter Setting
        input_units = self.param_dict["input_units"]
        output_units = self.param_dict["output_units"]

        model_nm = self.param_dict["model_nm"]
        alg_sn = self.param_dict["alg_sn"]
        hidden_units = self.param_dict["hidden_units"]
        act_fn = self.param_dict["act_fn"]
        dropout_prob = self.param_dict["dropout_prob"]

        optimizer_fn = self.param_dict["optimizer_fn"]
        learning_rate = self.param_dict["learning_rate"]

        activation = eval(Common.ACTIVATE_FN_CODE_DICT[act_fn])

        # Generate to Keras Model
        self.model = tf.keras.Sequential()
        self.inputs = tf.keras.Input(shape=(1024,), name="{}_{}_X".format(model_nm, alg_sn))
        self.model.add(self.inputs)

        #####################################################################################
        for idx, hidden_unit in enumerate(hidden_units):
            self.model.add(tf.keras.layers.Dense(hidden_unit,
                                                 name="{}_{}_encoder_dense_{}".format(model_nm, alg_sn, idx),
                                                 activation=activation
                                                 ))
            self.model.add(tf.keras.layers.Dropout(dropout_prob))

        hidden_units.reverse()
        hidden_units = hidden_units[1:]
        len_hidden = len(hidden_units)

        for idx, hidden_unit in enumerate(hidden_units):
            self.model.add(tf.keras.layers.Dense(hidden_unit,
                                                 name="{}_{}_decoder_dense_{}".format(model_nm, alg_sn, idx),
                                                 activation=activation
                                                 ))
            if idx != len_hidden - 1:
                self.model.add(tf.keras.layers.Dropout(dropout_prob))

        self.model.add(tf.keras.layers.Dense(1024,
                                             name="{}_{}_predicts".format(model_nm, alg_sn),
                                             activation='sigmoid'
                                             ))

        self.predicts = self.model.get_layer(index=-1)

        self.model.compile(
            loss='mse',
            optimizer=eval(Common.OPTIMIZER_FN_CODE_DICT[optimizer_fn])(learning_rate),
            metrics=['mae']
        )
        # if self.param_dict["job_type"] != "predict":
        #     self.model.summary(print_fn=self.LOGGER.info)

    @staticmethod
    def preprocessing(data):
        # 전처리
        rst_list = list()

        cvt_fn = SWC_KDAEOD(stat_dict={}, arg_list=[1024, 'Basic'])

        for url in data:
            rst_list.append(cvt_fn.apply(url[0]))

        return rst_list

    def learn(self, dataset):
        # learn result
        self.batch_size = 1024
        global_sn = self.param_dict["global_sn"]
        global_step = self.param_dict["global_step"]
        result_callback = LearnResultCallback(global_sn=global_sn)
        self.LOGGER.info("Data Converting Start...")
        x = self.url_proc(dataset["x"])
        preproc_x = self.preprocessing(x)

        self.LOGGER.info("Data Converting End and Learning Start...")

        dataset["x"] = preproc_x
        dataset["y"] = preproc_x

        dataset, parallel_step = self._make_train_dataset(dataset)

        # early stop
        early_stop_callback = EarlyStopCallback(self.learn_params)
        self.model.fit(
            x=dataset, epochs=global_step,
            steps_per_epoch=parallel_step,
            callbacks=[result_callback, early_stop_callback],
            verbose=1
        )
        self.stopped_epoch = early_stop_callback.get_stopped_epoch()

        result = result_callback.get_result()
        pred_result = self.mse_predict(dataset["x"], make_rmse=True)
        self.rmse = np.sqrt(np.mean((pred_result - np.array(dataset['x'])) ** 2))
        self.LOGGER.info("rmse : {}".format(self.rmse))

        for rst in result:
            rst["rmse_val"] = self.rmse

        return result

    def predict(self, x):
        total_results = list()
        len_x = len(x)
        self.LOGGER.info("origin data length : {}".format(len(x)))
        start_total_time = datetime.now()
        # start_time = datetime.now()
        x = self.url_proc(x)
        # end_time = datetime.now()
        # self.LOGGER.info("url_proc_time : [{}]".format(end_time - start_time))
        # start_time = datetime.now()
        preproc_data = self.preprocessing(x)
        # end_time = datetime.now()
        # self.LOGGER.info("preproc_time : [{}]".format(end_time - start_time))

        # start_time = datetime.now()
        mse_results = self.mse_predict(preproc_data, make_rmse=False)
        # mse_results = [[1, 0]] * len_x
        # end_time = datetime.now()
        # self.LOGGER.info("mse_predict_time : [{}]".format(end_time - start_time))
        # start_time = datetime.now()
        path_results, param_results, rst_list = self.url_predict(x)
        # end_time = datetime.now()
        # self.LOGGER.info("url/param_predict_time : [{}]".format(end_time - start_time))
        # start_time = datetime.now()
        bt_results = self.bt_predict(x)
        # end_time = datetime.now()
        # self.LOGGER.info("bt_predict_time : [{}]".format(end_time - start_time))
        # start_time = datetime.now()
        att_results = self.att_predict(x)
        # end_time = datetime.now()
        # self.LOGGER.info("att_predict_time : [{}]".format(end_time - start_time))
        end_total_time = datetime.now()
        self.LOGGER.info("predict_time : [{}]".format(end_total_time - start_total_time))
        # duration_sec = (end_total_time - start_total_time).seconds
        # if duration_sec == 0:
        #         duration_sec = 1
        # self.LOGGER.info("time of per data : [{}]".format(len(x) / duration_sec))

        # 가중치를 이용한 total_result 계산 추가
        for idx in range(len_x):
            temp_list = list()
            temp_list.extend(mse_results[idx])
            temp_list.extend(path_results[idx])
            temp_list.extend(param_results[idx])
            temp_list.extend(bt_results[idx])
            temp_list.extend(att_results[idx])

            # calculate total result
            total_rst = self.cal_total_rst(temp_list)
            temp_list.append(total_rst[0])
            temp_list.append(self.rmse)
            temp_list.append(total_rst[1])
            temp_list.append(x[idx][0])
            temp_list.extend(rst_list[idx])
            total_results.append(temp_list)

        return total_results

    @staticmethod
    def cal_total_rst(result_list):
        # total result 구해야함
        ae_result = result_list[0]
        if result_list[2] < 0:
            path_result = 1
        else:
            path_result = result_list[2]
        if result_list[4] is not 0:
            param_result = 1
        else:
            param_result = result_list[4]

        bt_result = result_list[6]
        att_result = result_list[8]

        rst_point = (ae_result + (att_result * 0.5)
                     + path_result + (param_result * 0.5) + (bt_result * 2)) / 2
        if rst_point >= 0.8:
            total_result = 1
        else:
            total_result = 0

        return [total_result, rst_point]

    @staticmethod
    def url_proc(_x):
        # host_domain / url / url2 예외처리 및 문자열 합치기
        rst_list = list()
        for line in _x:
            domain = line[0]
            url = line[1]
            url2 = line[2]
            bt = line[3]
            try:
                post_data = line[4]
            except:
                post_data = None

            # domain 필드 빈 값인 경우
            if domain == '-':
                domain = ''
            # url 필드 빈 값인 경우
            if url == '-' or url == 'x':
                url = ''
            # url2 필드 빈 값인 경우
            if url2 == '-' or url2 == 'x':
                url2 = ''
            # url, url2 필드가 완전 일치하는 경우
            if url == url2:
                url2 = ''

            # url 필드가 깨진 문자열이고 url2에 정상 패스가 들어가 있는경우
            if (re.match(r'[^\u0000-\u007F\u3131-\u318E\uAC00-\uD7A3]+', url) is not None) and (re.match(r'^/', url2) is not None):
                url = ''

            # domain 값이 url에 중복 발생하는 경우
            domain = re.sub(r'^([/]?http[s]?://)?([w]{3}.)?', '', domain)
            url = re.sub(r'^([/]?http[s]?://)?([w]{3}.)?', '', url)
            if url.startswith(domain):
                domain = ''

            url = url + url2

            rst = domain + url

            rst = re.sub(r'^([/]?http[s]?://)?([w]{3}.)?', '', rst)

            rst = parse.unquote(rst)

            rst_list.append([rst, bt, post_data])

        return rst_list

    def url_predict(self, data_x):
        path_results = list()
        param_results = list()
        url_filter = self.ext_data.get("path_keyword", {})
        param_filter = self.ext_data.get("param_keyword", {})
        rst_list = list()

        for line in data_x:
            tmp_list = list()
            url = line[0]

            # host_domain = ''
            # path_only = ''
            # file_only = ''  # 실제 파일명 or 규칙(ex> eng_file_length)
            # file_ext = ''
            # url_path = ''
            # param_list = []  # [key, value_ori, value_type, value_len]

            # url parsing
            host_domain, url_path, path_only, file_only, file_ext, file_ext_rst, param_list = self.parse_url(url)

            tmp_list.append(url_path)
            tmp_list.append(path_only)
            tmp_list.append(file_only)
            tmp_list.append(file_ext)
            tmp_list.append(file_ext_rst)
            tmp_list.append(param_list)
            rst_list.append(tmp_list)

            if file_only == "":
                file_only = "-"

            if path_only == "":
                path_only = "-"

            if file_ext == "":
                file_ext = "-"

            # path filter
            # host domain 확인
            if host_domain in url_filter:
                # path only 확인
                if path_only in url_filter[host_domain]:
                    # file 정규화 규칙 확인
                    pattern_head = ''
                    pattern_len = 0

                    if 'num_file_' in file_only:
                        pattern_head = 'num_file_'
                        pattern_len = int(file_only.split('_')[2])
                    elif 'eng_file_' in file_only:
                        pattern_head = 'eng_file_'
                        pattern_len = int(file_only.split('_')[2])
                    elif 'mix_file_' in file_only:
                        pattern_head = 'mix_file_'
                        pattern_len = int(file_only.split('_')[2])
                    elif 'kor_file_' in file_only:
                        pattern_head = 'kor_file_'
                        pattern_len = int(file_only.split('_')[2])

                    isPatternHead = 1 if len(pattern_head) > 0 else 0
                    isPatternExt = False

                    if len(pattern_head) > 0:
                        # file_only 가 패턴 형식이고, 사전에 있는 경우 일치하는 키로 변환
                        for item in (url_filter[host_domain][path_only]).keys():
                            if pattern_head in item:
                                min_len = int(item.split('_')[2])
                                try:
                                    max_len = int(item.split('_')[3])
                                except Exception as e:
                                    max_len = min_len

                                if min_len <= pattern_len <= max_len:
                                    # Pattern인 경우에 원래 확장자 확인
                                    if file_ext in url_filter[host_domain][path_only][item]:
                                        # pattern인 경우 결과 최종 정상
                                        isPatternExt = True

                    # file only 확인
                    if isPatternHead:
                        # 파일명이 패턴으로 변환된 경우 최종 결과 확인
                        if isPatternExt:
                            path_results.append([0, 'Normal'])
                        else:
                            path_results.append([1, 'No File extention({}) info.'.format(file_ext)])
                    elif file_only in url_filter[host_domain][path_only]:
                        # 파일명이 그대로인경우 최종 결과 확인
                        if file_ext in url_filter[host_domain][path_only][file_only]:
                            # path filter 결과 최종 정상
                            path_results.append([0, 'Normal'])
                        else:
                            path_results.append([1, 'No File extention({}) info.'.format(file_ext)])
                    else:
                        # 파일명이 패턴/원문 모두 사전에 없는 경우
                        path_results.append([1, 'No File({}) info'.format(file_only)])
                else:
                    path_results.append([1, 'No Path({}) info'.format(path_only)])
            else:
                path_results.append([1, 'No Domain({}) info'.format(host_domain)])

            # param filter
            # param_list 가 있는 경우 만
            if len(param_list) > 0:
                # host domain 확인
                if host_domain in param_filter:
                    # url path 확인
                    if url_path in param_filter[host_domain]:
                        # param 들을 확인하여 불일치 발생 수 만큼 카운트하여 저장
                        param_result = 0
                        param_result_txt = ''
                        for param in param_list:
                            key = param[0]
                            value_type = param[2]
                            value_len = param[3]

                            # param key 확인
                            if key in param_filter[host_domain][url_path]:
                                # param value type 확인
                                if value_type in param_filter[host_domain][url_path][key]:
                                    # value length 확인
                                    value_min = param_filter[host_domain][url_path][key][value_type][0]
                                    value_max = param_filter[host_domain][url_path][key][value_type][1]
                                    if (value_len >= value_min) and (value_len <= value_max):
                                        # param 1개의 filter 결과 최종 정상
                                        param_result += 0
                                        param_result_txt += ''
                                    else:
                                        param_result += 1
                                        param_result_txt += 'Key({}) Value Length({}) missmatch. '.format(key,
                                                                                                          value_len)
                                else:
                                    param_result += 1
                                    param_result_txt += 'Key({}) Value Type({}) missmatch. '.format(key, value_type)
                            else:
                                param_result += 1
                                param_result_txt += 'No Key({}) info. '.format(key)

                        if param_result == 0:
                            # param filter 결과 최종 정상
                            param_results.append([0, 'Normal'])
                        else:
                            param_results.append([param_result, param_result_txt])
                    else:
                        param_results.append([1, 'No URL path({}) info'.format(url_path)])
                else:
                    param_results.append([1, 'No Domain({}) info'.format(host_domain)])
            else:
                # 파라미터가 없는 경우 : 정상
                param_results.append([0, 'Normal'])

        return path_results, param_results, rst_list

    def bt_predict(self, x):
        bt_results = list()
        bt_filter = self.ext_data.get("bt_keyword", [])

        for line in x:
            bt_results.append(self.predict_bt_filter(
                line=line[1], _filter=bt_filter
            ))

        return bt_results

    def att_predict(self, x):
        att_results = list()
        att_filter = self.ext_data.get("att_keyword", [])

        for line in x:
            att_results.append(self.predict_att_filter(line=line[0], _filter=att_filter))

        return att_results

    def mse_predict(self, x, make_rmse=False):
        # batch_size = int(self.batch_size / 2)
        batch_size = self.batch_size

        start = 0
        len_x = len(x)

        results = np.empty([len_x, 1024], dtype=np.float32)

        while start < len_x:
            end = start + batch_size
            if start == 0 and batch_size < len_x:
                # batch_x = tf.keras.backend.cast(x[start: end], tf.float32)
                # batch_x = tf.convert_to_tensor(x[start: end])
                batch_x = np.array(x[start: end], dtype=np.float32)
                # results = self.model(batch_x).numpy()
                results[start:end] = self.model.predict_on_batch(batch_x)
                # results = self.model(x[start : end]).numpy()

            elif start == 0 and batch_size >= len_x:
                # batch_x = tf.keras.backend.cast(x, tf.float32)
                # batch_x = tf.convert_to_tensor(x)
                batch_x = np.array(x, dtype=np.float32)
                # results = self.model(batch_x).numpy()
                results[start:len_x] = self.model.predict_on_batch(batch_x)
                # results = self.model(x).numpy()

            elif end >= len_x:
                # batch_x = tf.keras.backend.cast(x[start:], tf.float32)
                # batch_x = tf.convert_to_tensor(x[start:])
                batch_x = np.array(x[start:], dtype=np.float32)
                # results = np.concatenate((results, self.model(batch_x).numpy()), axis=0)
                results[start:len_x] = self.model.predict_on_batch(batch_x)
                # results = np.concatenate((results, self.model(x[start: ]).numpy()), axis=0)

            else:
                # batch_x = tf.keras.backend.cast(x[start:end], tf.float32)
                # batch_x = tf.convert_to_tensor(x[start:end])
                batch_x = np.array(x[start:end], dtype=np.float32)
                # results = np.concatenate((results, self.model(batch_x).numpy()), axis=0)
                results[start:end] = self.model.predict_on_batch(batch_x)
                # results = np.concatenate((results, self.model(x[start : end]).numpy()), axis=0)
            start += batch_size

        if make_rmse is True:
            return results
        else:
            total_results = list()
            for i in range(len_x):
                row_rmse = np.sqrt(np.mean((results[i] - np.array(x[i])) ** 2))
                if row_rmse > self.rmse:
                    total_results.append([1, row_rmse])
                else:
                    total_results.append([0, row_rmse])

            return total_results

    @staticmethod
    def predict_bt_filter(line, _filter):
        for one_filter in _filter:
            if one_filter in line:
                return [1, one_filter]

        return [0, "None"]

    @staticmethod
    def predict_att_filter(line, _filter):
        filter_list = list()
        filter_cnt = 0
        for one_filter in _filter:
            if one_filter in line:
                filter_list.append(one_filter)
                filter_cnt += 1

        if filter_cnt > 0:
            result = 1
        else:
            result = 0

        return [result, filter_cnt, str(filter_list)]

    # 탐지 url 로그 정규화 후 결과 반환
    # return value : 도메인, URL_Path(전체), URL_Path_only(URL 경로만), FILE_Name(파일명), FILE_Ext(파일 확장자), Param_list(파라미터 리스트)
    def parse_url(self, one_url):
        one_url = re.sub('^http://', '', one_url)
        one_url = re.sub('^https://', '', one_url)

        # std_0_domain = ''  # 도메인
        std_1_u_temp = ''  # URL 전체 (중간단계)
        std_2_u_path = ''  # URL 중 경로 전체 (경로 + 파일명 + 파일확장자)
        std_3_paramt = ''  # 파라미터
        # std_4_jsessn = ''  # jsessionid

        cnt_0_slash = one_url.count('/')
        cnt_1_quest = one_url.count('?')

        if cnt_0_slash == 0:  # 슬래시가 없으면 도메인 만 있는 경우
            std_0_domain = one_url
        else:
            std_0_domain = one_url.split('/', 1)[0]  # 도메인 추출
            std_1_u_temp = one_url.split('/', 1)[1]  # 도메인 제거한 URL 경로

        std_0_domain = re.sub('^www.', '', std_0_domain)

        if cnt_1_quest == 0:  # 파라미터 추출 관련
            std_3_paramt = ''
            std_2_u_path = std_1_u_temp

        elif cnt_1_quest >= 1:
            # 슬래시(/) 없이 물음표(?) 만 있는 경우 (수정 일: 2021-02-09, 수정 내용 : 예외 처리 추가)
            if cnt_0_slash == 0:
                std_3_paramt = std_0_domain.split('?', 1)[1]  # Parameter (파라미터 형태 : key=value&key=value)
                std_2_u_path = ''  # URL_PATH (없음)

                std_0_domain = std_0_domain.split('?', 1)[0]  # 도메인
            else:
                std_3_paramt = std_1_u_temp.split('?', 1)[1]  # Parameter (파라미터 형태 : key=value&key=value)
                std_2_u_path = std_1_u_temp.split('?', 1)[0]  # URL_PATH (파라미터 제거된 URL PATH)

        cnt_2_semic = std_2_u_path.count(';')
        std_2_u_path = std_2_u_path.replace('%3B', ';', 1)  # %3B >> ; 으로 치환
        std_2_u_path = std_2_u_path.replace('%3b', ';', 1)  # %3b >> ; 으로 치환

        if cnt_2_semic == 1:
            # std_4_jsessn = std_2_u_path.split(';', 1)[1]  # JsessionID (jsession:ajsdf29vjckdf)
            std_2_u_path = std_2_u_path.split(';', 1)[0]  # URL_PATH (파라미터, jession을 제외한 웹경로 + 파일명)

        cnt_3_hasht = std_2_u_path.count('#')

        if cnt_3_hasht == 1:
            std_2_u_path = std_2_u_path.split('#', 1)[0]  # URL_PATH (# 제외)

        std_2_u_path = re.sub('^/', '', std_2_u_path)  # 맨 처음 문자가 '/' 인 경우 제외
        std_2_u_path = re.sub('/$', '', std_2_u_path)  # 맨 마지막 문자가 '/' 인 경우 제외

        # std_5_u_only = ''  # URL 중 경로만
        std_5_u_only2 = ''  # URL 중 경로를 >> 코드화
        # std_6_f_file = ''  # 파일명 전체 (파일명 + 파일확장자)
        # std_7_file_n = ''  # 파일명
        std_7_file_c3 = ''  # 파일명 코드화
        std_8_file_e = ''  # 파일확장자
        std_8_file_e_rst = 'normal'

        std_10_param = ''  # 파리미터 [리스트 형태]

        cnt_5_slash = std_2_u_path.count('/')

        if cnt_5_slash == 0:  # 경로가 하나인 경우

            cnt_6_dot = std_2_u_path.count('.')

            if cnt_6_dot == 0:  # 경로인 경우
                std_5_u_only = std_2_u_path
                std_6_f_file = ''
            elif cnt_6_dot == 1:  # 파일명인 경우
                std_5_u_only = ''
                std_6_f_file = std_2_u_path
            else:
                check_file = std_2_u_path.rsplit('.', 1)[1]

                if self.int_regexp.search(check_file) is not None:
                    std_5_u_only = std_2_u_path
                    std_6_f_file = ''
                else:
                    std_5_u_only = ''
                    std_6_f_file = std_2_u_path

        else:
            std_5_u_only = std_2_u_path.rsplit('/', 1)[0]  # 파일명 찾기 (오른쪽 기준으로 '/' split)
            std_6_f_file = std_2_u_path.rsplit('/', 1)[1]  # 파일명 찾기 (오른쪽 기준으로 '/' split)

            cnt_7_dot = std_6_f_file.count('.')

            if cnt_7_dot == 0:  # 마지막 경로가 파일명이 아닌 경우
                std_5_u_only = std_5_u_only + '/' + std_6_f_file
                std_6_f_file = ''

            elif cnt_7_dot > 1:  # 2개 이상일 경우

                check_file = std_6_f_file.rsplit('.', 1)[1]

                if self.int_regexp.search(check_file) is not None:
                    std_5_u_only = std_5_u_only + '/' + std_6_f_file
                    std_6_f_file = ''

        if std_6_f_file != '':

            std_7_file_n = std_6_f_file.rsplit('.', 1)[0]  # 파일명 추출
            std_7_file_c: str = std_7_file_n
            std_8_file_e = std_6_f_file.rsplit('.', 1)[1]  # 파일확장자 추출
            std_8_file_e = std_8_file_e.lower()
            if self.ext_0_regex.search(std_8_file_e) is not None:
                std_8_file_e_rst = 'not_normal'

            # 수정 부분 START ###
            # 추가 (수정 일: 2021-02-09, 수정 내용 : FILE NAME 디코딩)
            for i in range(0, 5):
                std_7_file_c = parse.unquote(std_7_file_c)
            # 수정 부분 END ###

            # 20210820 no.3 ####
            except_ext_list = ['jsp', 'php', 'asp']
            if std_7_file_c.isdigit() and std_8_file_e in except_ext_list:
                std_7_file_c2 = std_7_file_c
            else:
                std_7_file_c2 = re.sub('[0-9]', '0', std_7_file_c)
            ######################

            std_7_file_c3 = std_7_file_c2

            for one in self.file_ext_list:
                if std_8_file_e == one:
                    cnt = 0
                    prefix = ''
                    if self.num_0_regexp.search(std_7_file_c2) is not None:
                        cnt += 1
                        prefix = "num_file_"
                    if self.englower_0_regexp.search(std_7_file_c2) is not None or self.engupper_0_regexp.search(std_7_file_c2) is not None:
                        cnt += 1
                        prefix = "eng_file_"
                    if self.han_0_regexp.search(std_7_file_c2) is not None:
                        cnt += 1
                        prefix = "kor_file_"

                    if cnt == 1:
                        std_7_file_c3 = prefix + str(len(std_7_file_c2))
                    elif cnt >= 2:
                        std_7_file_c3 = "mix_file_" + str(len(std_7_file_c2))
                    else:
                        std_7_file_c3 = std_7_file_c2

                    continue

        # 수정 부분 START ###
        # 추가 (수정 일: 2021-02-09, 수정 내용 : URL_PATH 디코딩)
        for i in range(0, 5):
            std_5_u_only = parse.unquote(std_5_u_only)
        # 수정 부분 END ###

        std_5_u_only = re.sub('[0-9]', '0', std_5_u_only)

        # 경로 만 있는 경우 (빈 값 아닌 경우)
        if std_5_u_only != '':

            std_5_u_only_list = std_5_u_only.split('/')

            new_list = []

            for one in std_5_u_only_list:
                # 20210820 no.2 #####
                cnt = 0
                prefix = ''
                if self.num_0_regexp.search(one) is not None:
                    prefix = 'num_path_'
                    cnt += 1
                if self.engupper_0_regexp.search(one) is not None or self.englower_0_regexp.search(one) is not None:
                    cnt += 1
                if self.han_0_regexp.search(one) is not None:
                    prefix = 'kor_path_'
                    cnt += 1

                if cnt == 1:
                    if prefix == '':
                        simple = one
                    else:
                        simple = prefix + str(len(one))
                elif cnt >= 2:
                    simple = 'mix_path_' + str(len(one))
                else:
                    simple = one

                new_list.append(simple)

            std_5_u_only2 = '/'.join(new_list)

        # 파라미터 부분 처리
        if std_3_paramt != '':  # 파라미터가 있는 경우
            # print('====================================================')

            std_3_paramt = std_3_paramt.replace('&amp;', '&')  # Parameter (&amp; >> & 으로 변경)
            std_3_paramt = std_3_paramt.replace('&amp%3B', '&')  # Parameter (&amp%3B >> & 으로 변경)
            std_3_paramt = std_3_paramt.replace('&amp%3b', '&')  # Parameter (&amp%3b >> & 으로 변경)
            std_3_paramt = std_3_paramt.replace('&amp%253B', '&')  # Parameter (&amp%253B >> & 으로 변경)
            std_3_paramt = std_3_paramt.replace('&amp%253b', '&')  # Parameter (&amp%253b >> & 으로 변경)
            std_3_paramt = re.sub(r'^&', '', std_3_paramt)  # Parameter (시작이 & >> '' 으로 변경)
            std_3_paramt = re.sub(r'&$', '', std_3_paramt)  # Parameter (마지막이 & >> '' 으로 변경)

            param_list = std_3_paramt.split('&')

            total_list = []

            for one_param in param_list:
                # print(one_param)
                one_list = []

                if len(one_param.split('=', 1)) == 2:
                    word_key = one_param.split('=', 1)[0]
                    word_val = one_param.split('=', 1)[1]
                else:
                    word_key = one_param.split('=', 1)[0]
                    word_val = ''

                word_type = '99_other'

                for i in range(0, 5):
                    word_key = parse.unquote(word_key)
                    word_val = parse.unquote(word_val)

                word_key = re.sub('[0-9]', '0', word_key)
                word_val = re.sub('[0-9]', '0', word_val)
                word_val = word_val.lower()

                val_len = len(word_val)

                if val_len == 0:
                    word_type = '0_empty'

                if self.han_0_regexp.search(word_val) is not None:
                    word_type = '7_searchword'

                if self.val_1_regexp.search(word_val) is not None:
                    word_type = '1_number'

                elif self.val_2_regexp.search(word_val) is not None:
                    word_type = '1_numdot'

                elif self.val_3_regexp.search(word_val) is not None:
                    word_type = '2_idNum3'

                elif self.val_4_regexp.search(word_val) is not None:
                    word_type = '2_engUnd2'

                elif self.val_5_regexp.search(word_val) is not None:
                    word_type = '2_engNum1'

                elif self.val_6_regexp.search(word_val) is not None:
                    word_type = '3_filetypeI'

                elif self.val_6_2_regexp.search(word_val) is not None:
                    word_type = '3_pathfileI'

                elif self.val_6_3_regexp.search(word_val) is not None:
                    word_type = '3_domainfileI'

                elif self.val_7_regexp.search(word_val) is not None:
                    word_type = '3_filetypeD'

                elif self.val_7_2_regexp.search(word_val) is not None:
                    word_type = '3_pathfileD'

                elif self.val_7_3_regexp.search(word_val) is not None:
                    word_type = '3_domainfileD'

                elif self.val_21_regexp.search(word_val) is not None:
                    word_type = '10_hash1'

                elif self.val_22_regexp.search(word_val) is not None:
                    word_type = '10_hash2'

                elif self.val_8_regexp.search(word_val) is not None:
                    word_type = '4_domain'

                elif self.val_9_regexp.search(word_val) is not None:
                    word_type = '4_url'

                elif self.val_10_regexp.search(word_val) is not None:
                    word_type = '5_urlpath1'

                elif self.val_11_regexp.search(word_val) is not None:
                    word_type = '5_urlpath2'

                elif self.val_12_regexp.search(word_val) is not None:
                    word_type = '5_urlpath3'

                elif self.val_13_regexp.search(word_val) is not None:
                    word_type = '6_email1'

                elif self.val_14_regexp.search(word_val) is not None:
                    word_type = '8_xml'

                elif self.val_15_regexp.search(word_val) is not None:
                    word_type = '8_xml'

                elif self.val_16_regexp.search(word_val) is not None:
                    word_type = '9_json'

                elif self.val_17_regexp.search(word_val) is not None:
                    word_type = '9_json'

                elif self.val_18_regexp.search(word_val) is not None:
                    word_type = '9_json'

                elif self.val_19_regexp.search(word_val) is not None:
                    word_type = '9_json'

                elif self.val_20_regexp.search(word_val) is not None:
                    word_type = '9_json'

                elif self.val_23_regexp.search(word_val) is not None:
                    word_type = '2_engdot'

                one_list.append(word_key)
                one_list.append(word_val)
                one_list.append(word_type)
                one_list.append(val_len)

                total_list.append(one_list)

            std_10_param = total_list

            # print('====================================================')

        std_2_u_path = re.sub('[0-9]', '0', std_2_u_path)

        # 도메인, URL_Path(전체), URL_Path_only(URL 경로만), FILE_Name(파일명), FILE_Ext(파일 확장자), Param_list(파라미터 리스트)
        return std_0_domain, std_2_u_path, std_5_u_only2, std_7_file_c3, std_8_file_e, std_8_file_e_rst, std_10_param

    @staticmethod
    def _check_dir_model(dir_model):
        return os.path.exists(dir_model)

    @staticmethod
    def _save_model_keras(model, dir_model):
        model.save_weights(dir_model + '/weights.h5', save_format='h5')

    def _load_model_keras(self, model, dir_model):
        try:
            model.load_weights(dir_model + '/weights.h5')
        except Exception as e:
            self.LOGGER.error(e, exc_info=True)

    def saved_model(self):
        param_dict = self.param_dict

        dir_model = '{}/{}/{}'.format(
            Constants.DIR_TEMP, param_dict["model_nm"], param_dict["alg_sn"]
        )

        if self._check_dir_model(dir_model):
            try:
                # backup
                FileUtils.move_dir(dir_model, dir_model + "_prev")
                FileUtils.mkdir('{}/{}/{}'.format(Constants.DIR_TEMP, param_dict["model_nm"], param_dict["alg_sn"]))
            except Exception as e:
                self.LOGGER.error(str(e), exc_info=True)
        else:
            if not FileUtils.is_exist('{}/{}'.format(Constants.DIR_TEMP, param_dict["model_nm"])):
                FileUtils.mkdir('{}/{}'.format(Constants.DIR_TEMP, param_dict["model_nm"]))
                FileUtils.mkdir('{}/{}/{}'.format(Constants.DIR_TEMP, param_dict["model_nm"], param_dict["alg_sn"]))

        result_dict = {
            "rmse": self.rmse
        }
        f = FileUtils.file_pointer("{}/apeflow_json.tmp".format(dir_model), "w")
        try:
            f.write(
                json.dumps(result_dict, indent=4)
            )
            f.write("\n")
        except Exception as e:
            self.LOGGER.error(e, exc_info=True)
        finally:
            f.close()

        os.rename("{}/apeflow_json.tmp".format(dir_model), "{}/apeflow_json.model".format(dir_model))

        try:
            out_model_type = self.OUT_MODEL_TYPE

            if out_model_type == Constants.OUT_MODEL_TF:
                # KERAS VERSION
                if self.LIB_TYPE == Constants.KERAS:
                    self._save_model_keras(self.model, dir_model)
            else:
                raise NotSupportTypeError(algorithm_type=self.OUT_MODEL_TYPE)

            # REMOVE BACKUP-MODEL
            try:
                if self._check_dir_model(dir_model + "_prev"):
                    FileUtils.remove_dir(dir_model + "_prev")
            except Exception as e:
                self.LOGGER.error(str(e), exc_info=True)

            self.LOGGER.info("model saved ....")
            self.LOGGER.info("model dir : {}".format(dir_model))

        except Exception as e:
            self.LOGGER.error(str(e), exc_info=True)
            # RESTORE
            try:
                FileUtils.remove_dir(dir_model)
                FileUtils.move_dir(dir_model + "_prev", dir_model)
            except Exception as e:
                self.LOGGER.error(str(e), exc_info=True)

    def load_model(self):
        param_dict = self.param_dict
        dir_model = '{}/{}/{}'.format(
            Constants.DIR_TEMP, param_dict["model_nm"], param_dict["alg_sn"]
        )

        if not self._check_dir_model(dir_model):
            dir_model = '{}/{}/{}'.format(
                Constants.DIR_LOAD_MODEL, param_dict["model_nm"], param_dict["alg_sn"]
            )
        try:
            f = FileUtils.file_pointer("{}/apeflow_json.model".format(dir_model), "r")
            try:
                result_dict = json.load(f)
                self.rmse = result_dict.get("rmse", 0)

            except Exception as e:
                self.LOGGER.error(e, exc_info=True)
            finally:
                f.close()
        except:
            self.LOGGER.warn("apeflow_json.model file is not existed ...")

        if self._check_dir_model(dir_model):
            try:
                # start_time = datetime.now()
                out_model_type = self.OUT_MODEL_TYPE

                if out_model_type == Constants.OUT_MODEL_TF:
                    # KERAS VERSION
                    if self.LIB_TYPE == Constants.KERAS:
                        self._load_model_keras(self.model, dir_model)
                        # TF V1
                else:
                    raise NotSupportTypeError(algorithm_type=self.OUT_MODEL_TYPE)

                # end_time = datetime.now()

                self.LOGGER.info("model load ....")
                self.LOGGER.info("model dir : {}".format(dir_model))
                # Common.AI_LOGGER.getLogger().info("model load time : {}".format(end_time - start_time))

            except Exception as e:
                self.LOGGER.warn(str(e), exc_info=True)
        else:
            self.LOGGER.warn("MODEL FILE IS NOT EXIST : [{}]".format(dir_model))


if __name__ == '__main__':
    # CLASSIFIER

    def make_dataset(file_name, __feature_list):
        __dataset = dict()
        x = list()
        y = list()

        f = None
        try:
            f = FileUtils.file_pointer(file_name, "r")
            lines = f.readlines()
            random.shuffle(lines)

            for line in lines:
                line_list = list()
                line_json = json.loads(line)
                for feature in feature_list:
                    if feature is "label":
                        label = float(line_json[feature])
                        if label == 0:
                            onehot = [1, 0]
                        else:
                            onehot = [0, 1]
                        y.append(onehot)
                    else:
                        line_list.append(float(line_json[feature]))
                x.append(line_list)

        except Exception as e:
            print(e)
            print("file read is failed")

        finally:
            if f is not None:
                f.close()

        _dataset["x"] = np.array(x)
        _dataset["y"] = np.array(x)

        return _dataset

    physical_devices = tf.config.list_physical_devices('GPU')
    print("physical devices: ", physical_devices)
    for gpu_no in range(4):
        tf.config.experimental.set_memory_growth(physical_devices[gpu_no], True)

    __param_dict = {
        "params": {},
        "algorithm_code": "KDAEOD",
        "algorithm_type": "OD",
        "data_type": "Single",
        "method_type": "Basic",
        "input_units": "23",
        "output_units": "23",

        "dropout_prob": "0.3",
        "optimizer_fn": "Adam",
        "model_nm": "KDAEOD_34",
        "alg_sn": "0",
        "job_type": "learn",
        "depth": "0",
        "global_sn": "0",
        "learning_rate": "0.01",

        "filter_sizes": "2",
        "pool_sizes": "2",
        "num_filters": "3",
        "pooling_fn": "Max1D",
        "conv_fn": "Conv1D",
        "global_step": "2",
        "num_workers": "1",

        "early_type": "0",
        "minsteps": "10",
        "early_key": "accuracy",
        "early_value": "0.98"
    }

    # model = KCNNAE(param_dict=param_dict)
    #
    # model._build()
    #
    # print("???")
    # from pycmmn.interfaces.FileUtils import FileUtils
    # import random
    # import json
    feature_list = ["agg_count_x", "time_diff_sec_x", "unique_src_ip_cnt",
                    "unique_dstn_port_cnt_x", "A_port_cnt_x", "B_port_cnt_x",
                    "C_port_cnt_x", "src_ip_avg_cnt", "dstn_port_avg_cnt_x",
                    "dstn_port_src_ip_ratio", "attack_intv_x", "agg_count_y",
                    "time_diff_sec_y", "prtc_TCP_cnt", "prtc_UDP_cnt", "prtc_ICMP_cnt",
                    "prtc_OTH_cnt", "unique_dstn_port_cnt_y", "A_port_cnt_y", "B_port_cnt_y",
                    "C_port_cnt_y", "dstn_port_avg_cnt_y", "attack_intv_y", "label"]
    _dataset = make_dataset(file_name="./data/ddos_train_v2_20210111.done",
                            __feature_list=feature_list)
    print("X Dimension CNT : {}".format(_dataset["x"][0].size))

    model_ = KDAEOD(param_dict=__param_dict)
    # model_._build()
    model_.learn(_dataset)

    pred_x = make_dataset(file_name="./data/ddos_valid_v2_20210111.done",
                          __feature_list=feature_list)
    pred_x = pred_x["x"]
    print(model_.model(pred_x))
    model_.saved_model()

    temp = KDAEOD(param_dict=__param_dict)
    temp.load_model()

    print("loaded rmse")
    print(temp.rmse)

    temp.eval({"x": pred_x})

    print(len(pred_x))
    print(len(temp.predict(pred_x)))
