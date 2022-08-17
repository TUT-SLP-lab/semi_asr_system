# semi_asr_system

# requirement

-   docker
-   docker compose

# asr system

## fast api の立ち上げ方法

0. Local で API を立ち上げる場合(Option, 1~2 を skip)

    ```
    python src/run_asr_server.py
    ```

1. image のビルド（めっちゃ時間かかるかも）

    ```
    docker compose build asr_system

    ```

2. コンテナ立ち上げ

    ```
    docker compose up -d asr_system
    ```

3. API を試しに叩く

    ```
    python test/asr_system/unit_test.py
    ```
