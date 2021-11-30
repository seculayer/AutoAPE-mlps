FROM registry.seculayer.com:31500/ape/python-base-gpu:py3.7-cuda11.0 as builder
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

FROM registry.seculayer.com:31500/ape/python-base-gpu:py3.7-cuda11.0 as app
ARG app="/opt/app"
ENV LANG=en_US.UTF-8 LANGUAGE=en_US:en LC_ALL=en_US.UTF-8

RUN mkdir -p /eyeCloudAI/app/ape/mlps \
    && mkdir -p /eyeCloudAI/data/processing/ape/models
WORKDIR /eyeCloudAI/app/ape/mlps

COPY ./mlps.sh /eyeCloudAI/app/ape/mlps

COPY --from=builder "$app/lib" /eyeCloudAI/app/ape/mlps/lib

COPY --from=builder "$app/dist/mlps-3.0.0-py3-none-any.whl" \
        /eyeCloudAI/app/ape/mlps/mlps-3.0.0-py3-none-any.whl

RUN pip3.7 install /eyeCloudAI/app/ape/mlps/mlps-3.0.0-py3-none-any.whl --no-dependencies  \
    -t /eyeCloudAI/app/ape/mlps \
    && rm /eyeCloudAI/app/ape/mlps/mlps-3.0.0-py3-none-any.whl

RUN groupadd -g 1000 aiuser
RUN useradd -r -u 1000 -g aiuser aiuser
RUN chown -R aiuser:aiuser /eyeCloudAI
USER aiuser

CMD []