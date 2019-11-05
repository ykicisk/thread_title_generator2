# thread_title_generator2_private

なんJスレッドタイトルをっぽい文書を自動生成する。

## 起動方法

```sh
# Docker起動 (JupyterLabも立ち上がる)
$ sudo docker-compose up -d

# コンテナ内で作業
$ sudo docker-compose exec dev /bin/bash

# コンテナ内で作業(root)
$ sudo docker-compose exec dev --user root /bin/bash

# docker終了
$ sudo docker-compose down
```

## 実行方法

Jupyterにアクセスします。

```
http://<ホスト名>:8889/lab?
```

`notebooks`ディレクトリに入っているノートブックを順番に実行します。

## 詳細

本リポジトリにはスレタイっぽい文章を生成する**Generator**と、
Generatorの生成した文書を評価する**Evaluater**の２つで構成されます。

Generatorでたくさんスレタイを生成し、Evaluaterで高スコアのスレタイのみを出力します。

### Generator

GeneratorはRNNによるテキスト生成器です。

乱数を使って次のワードを選ぶことで、レパートリーに富んだスレタイを生成します。

### Evaluater

「Generatorの生成したスレタイ」と「本物のスレタイ」を区別する識別器です。

