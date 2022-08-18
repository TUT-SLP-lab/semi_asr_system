# semi_asr_system

# requirement

-   docker
-   docker compose

# asr system

## LocalでASR serverを立ち上げる方法

    ```bash
    # サーバの立ち上げ
    python src/run_asr_server

    # APIを叩く
    python test/asr_system/unit_test.py
    ```

## docker container でfast api の立ち上げ方法

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
