FROM python:3.7

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


COPY docker/dispatcher/requirements.txt ./
RUN pip install -U pip setuptools \
    pip install -r requirements.txt

WORKDIR /app/

# cronをインストール
RUN apt install cron -y

# 実行したいcronファイルの配置
# COPY mydns.cron /etc/cron.d
RUN echo "00 * * * * curl -X DELETE 'http://${DISPATCHER_IP}:${DISPATCHER_PORT}/api/delete'" > /etc/cron.d/delete_requests.cron

CMD crond -n
