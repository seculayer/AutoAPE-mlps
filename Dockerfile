FROM seculayer/python:3.7-cuda11.2 as builder
MAINTAINER jinkim "jinkim@seculayer.com"

ARG app="/opt/app"

RUN mkdir -p $app
WORKDIR $app

COPY ./requirements.txt ./requirements.txt
RUN pip3.7 install -r ./requirements.txt -t $app/lib

COPY ./mlps ./mlps
COPY ./setup.py ./setup.py

RUN pip3.7 install wheel
RUN python3.7 setup.py bdist_wheel

FROM seculayer/python:3.7-cuda11.2 as app
ARG app="/opt/app"

RUN mkdir -p /eyeCloudAI/app/ape/mlps \
    && mkdir -p /eyeCloudAI/data/processing/ape/models

RUN groupadd -g 1000 aiuser
RUN useradd -r -u 1000 -g aiuser aiuser
RUN chown -R aiuser:aiuser /eyeCloudAI

USER aiuser

WORKDIR /eyeCloudAI/app/ape/mlps

COPY ./mlps.sh /eyeCloudAI/app/ape/mlps

COPY --from=builder --chown=aiuser:aiuser "$app/lib" /eyeCloudAI/app/ape/mlps/lib/

COPY --from=builder --chown=aiuser:aiuser "$app/dist/mlps-3.0.0-py3-none-any.whl" /eyeCloudAI/app/ape/mlps/

RUN pip3.7 install /eyeCloudAI/app/ape/mlps/mlps-3.0.0-py3-none-any.whl --no-dependencies  \
    -t /eyeCloudAI/app/ape/mlps \
    && rm /eyeCloudAI/app/ape/mlps/mlps-3.0.0-py3-none-any.whl

ENV LANG=en_US.UTF-8 LANGUAGE=en_US:en LC_ALL=en_US.UTF-8

CMD []
