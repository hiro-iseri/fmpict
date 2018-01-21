# 【FMPict使い方】FMPictのセットアップ

## このドキュメントについて

このドキュメントでは、FMPictのインストール手順を解説します。  
[manual.md](manual.md) の補足ドキュメントです。

## ツール導入

### 1. 事前環境構築

* 以下からFreeMindをインストールします。  
    * https://ja.osdn.net/projects/freemind/
* PICTをインストールします。
    * Windows版は以下の20.PICTからダウンロード
        * http://www.pairwise.org/tools.asp
    * Mac、Linuxは以下を参照ください
        * http://goyoki.hatenablog.com/entry/2016/02/17/020256
* 以下からPythonをインストールします。
    * https://www.python.org/downloads/
* [Python2.7でpip未導入の場合]pipをインストールします。
    * 手順は以下など一般的な情報を参照ください。
        * https://qiita.com/suzuki_y/items/3261ffa9b67410803443

### 2. ツールインストール

#### 推奨インストール方法

以下を実行します。

```
pip install fmpict
```

#### オフライン環境へのインストール方法

1. 以下から最新版の.whlファイルをダウンロードしてください。

https://pypi.python.org/pypi/fmpict

2. 以下を実行ください。

```
pip install ダウンロードした.whlファイル
```

## 3. 環境設定

* pict.exeをfmpictから参照可能にします。
    * Windowsなら、環境変数PATHに、PICTのインストールフォルダを追加します。

## 4. 動作確認

1. CUI環境（Windowsならコマンドプロンプト、Macならターミナル）で以下を実行します。  

```
fmpict 対象マインドマップファイル
```

2. fmpictコマンドが存在しないといったエラーが表示されなければセットアップは完了です。

## fmpictのアップグレード

以下を実行します。

```
pip install -U fmpict
```
