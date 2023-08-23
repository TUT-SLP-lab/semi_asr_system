# semi_asr_system

# requirement

-   docker
-   docker compose (1.29.2)
-   nvidia-docker2 

## install docker-compose (1.29.2)
```bash
sudo curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## install nvidia-docker2
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install nvidia-docker2
sudo pkill -SIGHUP dockerd
```

# asr system

## LocalでASR serverを立ち上げる方法

```python
# IP Addressの修正
ASR_SYSTEM_IP = "0.0.0.0"
↓
ASR_SYSTEM_IP = "127.0.0.1"
```

```bash
# サーバの立ち上げ
python src/run_asr_server

# APIを叩く
python test/asr_system/unit_test.py
```

## docker container でfast api の立ち上げ方法

0. データの準備
    
    `docker/data/`以下にデータを準備します。
    - models: expファイルを入れる（木内からもらってください。）
    
    - split_wav: 分割された音声を入れる　（木内からもらう）

    - text: なにもしない。

    e.g
    ```
    data
        models
            exp
                asr_stats
                asr_train
                lm_stats
                lm_train
        split_wav
            **.wav
            **.wav
        text

    ```

1. (1)Imageの取得

    ```bash
    docker login 
    docker pull kinouchi1000/espnet_asr_server
    ```

2. (2)Image のビルド

    1の Imageの取得ができていればやる必要がありません。（めっちゃ時間かかる）

    ```bash
    docker compose build asr_system

    ```

3. コンテナ立ち上げ

    ```
    docker compose up -d asr_system
    ```

4. API を試しに叩く

    ```
    python test/asr_system/unit_test.py
    ```

## Slack webhook urlの登録方法

1. [Webhookを新規作成するページ](https://slack.com/services/new/incoming-webhook)に行く
2. 右上のワークスペース選択ボタンでワークスペースを自身のものに変更する
3. 投稿したいチャンネルを選択し、作成する
4. webhook URLの項目のURLをコピーする
4. `.env`ファイル内の`SLACK_WEB_HOOK_URL`にコピーしたURLを設定する
