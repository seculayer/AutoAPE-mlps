#!/bin/bash
##########################################################################
# eyeCloudAI 3.0 mlps BUILD
# Author : Jin Kim
# e-mail : jinkim@seculayer.co.kr
# Powered by Seculayer © 2021 Service Model Team, R&D Center of Seculayer Inc.
##########################################################################

echo '               __           '
echo '    ____ ___  / /___  _____ '
echo '   / __ `__ \/ / __ \/ ___/ '
echo '  / / / / / / / /_/ (__  )  '
echo ' /_/ /_/ /_/_/ .___/____/   '
echo '            /_/             '

##########################################################################
BASE_DIR=
EXEC_FILE="$0"
BASE_NAME=`basename "$EXEC_FILE"`
if [ "$EXEC_FILE" = "./$BASE_NAME" ] || [ "$EXEC_FILE" = "$BASE_NAME" ]; then
        BASE_DIR=`pwd`
else
        BASE_DIR=`echo "$EXEC_FILE" | sed 's/'"\/${BASE_NAME}"'$//'`
fi

DEPLOY_PATH=${BASE_DIR}/../deploy
if [ ! -d "${DEPLOY_PATH}" ]
then
  mkdir -p "${DEPLOY_PATH}"
fi

PIP3_PATH=$DEPLOY_PATH/pip3

##########################################################################
APE_PATH="/eyeCloudAI/app/ape"
MODULE_NM="mlps"
VERSION="3.0.0"
BUILD_DT=`date '+%Y%m%d%H%M'`
BUILD_RV="${1}"

######################################################
echo "##########################################################"
echo '1. Building python module'
echo "##########################################################"
##########################################################################
# BACKUP
BACKUP_DIR=`date +%Y%m%d%H%M%S`

if [ ! -d "${BASE_DIR}/backup/${BACKUP_DIR}" ]
then
	mkdir -p "${BASE_DIR}/backup/${BACKUP_DIR}"
fi

mv "${DEPLOY_PATH}/pip3/${MODULE_NM}"*.whl "${BASE_DIR}/backup/${BACKUP_DIR}"
######################################################
# export ENVIRONMENT
export PYTHONPATH=${PYTHONPATH}:${BASE_DIR}/../pycmmn:${BASE_DIR}
######################################################
# BUILD
echo "module : ${MODULE_NM}
version : ${VERSION}
build date : ${BUILD_DT}
revision : ${BUILD_RV}" > "${BASE_DIR}/${MODULE_NM}"/VERSION

python3.7 $BASE_DIR/setup.py bdist_wheel

##########################################################################
# MOVE Data
mv "${BASE_DIR}/dist/${MODULE_NM}"*.whl  "${PIP3_PATH}"

##########################################################################
echo ''
echo "##########################################################"
echo "2. Configuration file settings."
echo "##########################################################"
echo ''
##########################################################################
# CONFIGURATION FILES
chmod +x "${BASE_DIR}"/../k8s-utils/run/configmap.sh
${BASE_DIR}/../k8s-utils/run/configmap.sh mlps

###########################################################################
## delete remained data
rm -rf "${BASE_DIR}"/build/bdist*
rm -rf "${BASE_DIR}"/build/lib*
rm -rf "${BASE_DIR}"/build/temp*
rm -rf "${BASE_DIR}"/$MODULE_NM.egg-info

# db information update
# chmod +x $BASE_DIR/../k8s-utils/run/update-image-db.sh
# $BASE_DIR/../k8s-utils/run/update-image-db.sh $MODULE_NM $BUILD_RV
