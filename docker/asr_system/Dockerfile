FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-devel


# install ESPnet
RUN cd /opt \
    && git clone --depth 1 https://github.com/espnet/espnet \
    && cd espnet/tools \
    && ./setup_python.sh $(command -v python3) \
    && make TH_VERSION=1.11.0 CUDA_VERSION=11.3


COPY docker/asr_system/requirements.txt ./
RUN pip install -U pip setuptools \
    pip install -r requirements.txt

WORKDIR /app/

