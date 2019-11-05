# thread_title_generator2_private

なんJスレッドタイトルっぽい文書を自動生成する。

## 生成例

### 制限なし

```
Generation: SOS 名前 に 「 デス 」 が 付く 曲 NUM つ しか ない EOS PAD PAD PAD PAD PAD PAD PAD PAD PAD PAD score: 4.6163287
Generation: SOS オコエ 「 マッマ オデ は UNK ん ! 」 ← 誰 で 寝 て た ? EOS PAD PAD PAD PAD PAD PAD score: 3.591072
Generation: SOS 敵 「 ワイ の こと 好き な ん ? 」 トッモ 「 は ? 僕 は ? 」 EOS PAD PAD PAD PAD score: 3.3199003
Generation: SOS なんj 民 が 知っ て いる 一番 の UNK は ? EOS PAD PAD PAD PAD PAD PAD PAD PAD PAD PAD PAD score: 3.029164
Generation: SOS ワイ NUM 歳 大学生 結婚 し たい のに 仕事 が ない EOS PAD PAD PAD PAD PAD PAD PAD PAD PAD PAD PAD score: 2.7726371
```

### Prefix「三大」

```
Generation: SOS 三大 やらかし た UNK の 根本 の 中 で の 会話 「 ドア 机 」 「 杉浦 」 EOS PAD PAD PAD PAD score: 3.601511
Generation: SOS 三大 う けど 勢い 揃っ てる 気 が つい た 欠陥 UNK 馬 EOS PAD PAD PAD PAD PAD PAD PAD PAD PAD score: 3.2168586
Generation: SOS 三大 UNK が UNK に 必要 な もの 「 早稲田 」 「 ポテチ 」 あと 一 人 は ? EOS PAD PAD PAD score: 3.192483
Generation: SOS 三大 値段 高い と 思う な カッコイイ モビルスーツ ランキング ( NUM 番 最初 数字 ) EOS PAD PAD PAD PAD PAD PAD PAD score: 3.0752976
Generation: SOS 三大 当たり 出し が 激しい チーム 助っ人 采配 イチロー EOS PAD PAD PAD PAD PAD PAD PAD PAD PAD PAD PAD PAD PAD score: 3.0569434
```

### Prefix「【なぞなぞ】」

```
Generation: SOS 【 なぞなぞ 】 誰 でも 作る べき UNK の 曲 なー ん だ ? EOS PAD PAD PAD PAD PAD PAD PAD PAD score: 4.264069
Generation: SOS 【 なぞなぞ 】 ゴム つけ て そのまま ケーキ 誘う もの ってな ー ん だ ? EOS PAD PAD PAD PAD PAD PAD PAD score: 3.9145274
Generation: SOS 【 なぞなぞ 】 口 に 入れる と 美味しい 食べ物 ってな ~ ん だ ? EOS PAD PAD PAD PAD PAD PAD PAD PAD score: 3.8251681
Generation: SOS 【 なぞなぞ 】 UNK で 海 ワン が かける 言葉 ってな ー ん だ ? EOS PAD PAD PAD PAD PAD PAD PAD score: 3.6090522
Generation: SOS 【 なぞなぞ 】 バイク が 食わ れ て の sa お トラブル みたい な 名前 の メンバー は なん でしょ う ? EOS score: 3.5852108
```

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

