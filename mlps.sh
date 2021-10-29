#!/bin/bash
######################################################################################
# eyeCloudAI 3.1 MLPS Run Script
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.
######################################################################################

APP_PATH=/eyeCloudAI/app/ape

PYCMMN_LIB_PATH=$APP_PATH/pycmmn/lib
APEFLOW_LIB_PATH=$APP_PATH/apeflow/lib
DATACNVRTR_LIB_PATH=$APP_PATH/dataconverter/lib
MLPS_LIB_PATH=$APP_PATH/mlps/lib
CUSTOM_LIB_PATH=$APP_PATH/custom
####
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
export CUDA_HOME=/usr/local/cuda
export PYTHONPATH=$PYCMMN_LIB_PATH:$APEFLOW_LIB_PATH:$DATACNVRTR_LIB_PATH:$MLPS_LIB_PATH:$CUSTOM_LIB_PATH

KEY=${1}
TASK_IDX=${2}
JOB_TYPE=${3}
/usr/local/bin/python3.7 -m mlps.MLProcessingServer ${KEY} ${TASK_IDX} ${JOB_TYPE}