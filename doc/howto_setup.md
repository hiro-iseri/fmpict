# 【FMPict使い方】FMPictのセットアップ

## このドキュメントについて

このドキュメントでは、FMPictの最初の環境構築について手順を解説します。

## ツール導入

### 事前環境構築

* 以下からFreeMindをインストールします。  
    * https://ja.osdn.net/projects/freemind/
* PICTをインストールします。
    * Windows版は以下の20.PICTからダウンロード
        * http://www.pairwise.org/tools.asp
    * Mac、Linuxは以下を参考にしてください
        * http://goyoki.hatenablog.com/entry/2016/02/17/020256
* 以下からPythonをインストールします。
    * https://www.python.org/downloads/
* [Python2.7でpip未導入の場合]pipをインストールします。
    * 手順は以下など一般的な情報を参考にしてください。
        * https://qiita.com/suzuki_y/items/3261ffa9b67410803443

### ツールインストール

* 「pip install fmpict」を実行します。

## 環境設定

* pict.exeをスクリプトから参照可能にします。
    * Windowsなら、環境変数PATHに、PICTのインストールフォルダを追加します。

## 動作確認

1. CUI環境（Windowsならコマンドプロンプト、Macならターミナル）で以下を実行します。  

fmpict tests/fm_sample/simple.mm

3. PICT実行結果（テスト条件組み合わせ一覧）が出力されたら環境構築は完了です。