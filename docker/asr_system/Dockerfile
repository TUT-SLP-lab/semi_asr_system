FROM pytorch/pytorch:1.9.1-cuda11.1-cudnn8-runtime

RUN apt-get -y update \
    && apt-get -y upgrade  \
    && apt-get -y install \ 
    git \
    wget \
    make \
    cmake \
    sox \
    libsndfile1-dev \
    ffmpeg \
    flac \
    coreutils

RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8


# install ESPnet
RUN cd /opt \
    && git clone --depth 1 https://github.com/espnet/espnet \
    && cd espnet/tools \
    && rm -f activate_python.sh && touch activate_python.sh \
    && make TH_VERSION=1.9.1 CUDA_VERSION=11.1


COPY docker/asr_system/requirements.txt ./
RUN pip install -U pip setuptools \
    pip install -r requirements.txt

WORKDIR /app/

