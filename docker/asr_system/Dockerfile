ARG BASE_IMAGE=nvcr.io/nvidia/pytorch:23.06-py3

# build an image that includes only the nemo dependencies, ensures that dependencies
# are included first for optimal caching, and useful for building a development
# image (by specifying build target as `nemo-deps`)
FROM ${BASE_IMAGE} as nemo-deps

# dependency flags; should be declared after FROM
# torchaudio: not required by default
ARG REQUIRE_TORCHAUDIO=false
# k2: not required by default
ARG REQUIRE_K2=false
# ais cli: not required by default, install only if required
ARG REQUIRE_AIS_CLI=false

# Ensure apt-get won't prompt for selecting options
ENV DEBIAN_FRONTEND=noninteractive
# libavdevice-dev rerquired for latest torchaudio
RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y \
  libsndfile1 sox \
  libfreetype6 \
  swig \
  ffmpeg \
  libavdevice-dev && \
  rm -rf /var/lib/apt/lists/*

COPY docker/asr_system/requirements.txt ./
RUN pip install -U pip setuptools \
    pip install -r requirements.txt

WORKDIR /app/

