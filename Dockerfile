ARG UBUNTU_VERSION=20.04

FROM ubuntu:${UBUNTU_VERSION} as base

# See http://bugs.python.org/issue19846
ENV LANG C.UTF-8
ARG PYTHON=python3

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends --fix-missing \
    ${PYTHON} \
    ${PYTHON}-pip

RUN ${PYTHON} -m pip --no-cache-dir install --upgrade \
    pip \
    setuptools \
    psutil

RUN ln -s $(which ${PYTHON}) /usr/local/bin/python

ARG PYTORCH_VERSION=2.0.1
ARG TIKTOKEN_VERSION=0.4.0
ARG GRADIO_VERSION=3.36.1
ARG BOTO3_VERSION=1.28.9
ARG TORCH_CPU_URL=https://download.pytorch.org/whl/cpu/torch_stable.html

RUN \
    python -m pip install --no-cache-dir \
    torch==${PYTORCH_VERSION}+cpu -f ${TORCH_CPU_URL} tiktoken==${TIKTOKEN_VERSION} gradio==${GRADIO_VERSION} boto3==${BOTO3_VERSION}

WORKDIR /workspace

EXPOSE 80

COPY ["app.py", "."]

CMD [ "python3" , "app.py" ]