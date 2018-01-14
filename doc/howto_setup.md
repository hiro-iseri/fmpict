# 【FMPict使い方】FMPictのセットアップ

## このドキュメントについて

このドキュメントでは、FMPictの最初の環境構築について手順を解説します。

## ツール導入

* 以下の最新版からfmpict.zipをダウンロードし、解凍します。  
    * https://github.com/hiro-iseri/fmpict/releases
    * fmpict/fmpict.pyを使用します。
* 以下からFreeMindをインストールします。  
    * https://ja.osdn.net/projects/freemind/

* PICTをインストールします。
    * Windows版は以下の20.PICTからダウンロード
        * http://www.pairwise.org/tools.asp
    * Mac、Linuxは以下を参考にしてください
        * http://goyoki.hatenablog.com/entry/2016/02/17/020256
* 以下からPythonをインストールします。
    * https://www.python.org/downloads/

## 環境設定

* pict.exeをスクリプトから参照可能にします。
    * Windowsなら、環境変数PATHに、PICTのインストールフォルダを追加します。

## 動作確認

1. CUI環境（Windowsならコマンドプロンプト、Macならターミナル）で、fmpict.zipの解凍フォルダに移動します。

2. 以下を実行します。  
python fmpict/fmpict.py tests/fm_sample/simple.mm

3. PICT実行結果（テスト条件組み合わせ一覧）が出力されたら環境構築は完了です。