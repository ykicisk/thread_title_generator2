# output samples

`notebooks/05_generate_sample.ipynb`の出力結果

## 読み方

一部アレな文書が生成されてしまうことがあるためbase64でエンコードしています。

読みたい場合は適当な方法でデコードして確認してください。

## ファイル構成

### Evaluatorの高スコア文書のみ

* `free_with_evaluator64.txt`: 制限無しで生成したスレタイ
* `sandai_with_evaluator64.txt`: Prefix「三大」で生成したスレタイ
* `nazonazo_with_evaluator64.txt`: Prefix「【なぞなぞ】」で生成したスレタイ

### Generatorの出力そのまま

* `free_without_evaluator64.txt`: 制限無しで生成したスレタイ
* `sandai_without_evaluator64.txt`: Prefix「三大」で生成したスレタイ
* `nazonazo_without_evaluator64.txt`: Prefix「【なぞなぞ】」で生成したスレタイ
