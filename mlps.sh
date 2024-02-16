#!/bin/bash
######################################################################################
# eyeCloudAI 3.1 MLPS Run Script
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.
######################################################################################

APP_PATH=/eyeCloudAI/app/ape
####
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
export CUDA_HOME=/usr/local/cuda

if [ -x "${APP_PATH}/mlps/.venv/bin/python3" ]
then
  PYTHON_BIN="$APP_PATH/mlps/.venv/bin/python3"
else
  PYTHON_BIN="$(command -v python3.7)"

  export PYTHONPATH=$PYTHONPATH:$APP_PATH/mlps/lib:$APP_PATH/mlps
  export PYTHONPATH=$PYTHONPATH:$APP_PATH/pycmmn/lib:$APP_PATH/pycmmn
  export PYTHONPATH=$PYTHONPATH:$APP_PATH/apeflow/lib:$APP_PATH/apeflow
  export PYTHONPATH=$PYTHONPATH:$APP_PATH/dataconverter/lib:$APP_PATH/dataconverter
fi

KEY=${1}
TASK_IDX=${2}
JOB_TYPE=${3}

$PYTHON_BIN -m mlps.MLProcessingServer ${KEY} ${TASK_IDX} ${JOB_TYPE}
