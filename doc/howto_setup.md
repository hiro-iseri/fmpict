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
* [Python2.7〜3.3でpip未導入の場合]pipをインストールします。
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

### 3. 環境設定

* pict実行ファイルをfmpictから参照可能にします。
    * Windowsなら、環境変数PATHに、pict.exeのインストールフォルダを追加します。

### 4. 動作確認

1. CUI環境（Windowsならコマンドプロンプト、Macならターミナル）で以下を実行します。  

```
fmpict 対象マインドマップファイル
```

2. fmpictコマンドが存在しないといったエラーが表示されなければセットアップは完了です。

## トラブルシューティング

### pipが見つからないといったエラーが発生

* pipがインストールされていない場合があります。Python2.7〜3.3ではpipが同梱されていません。前述のリンク先の説明に従ってインストールしてください。
* pipの実行ファイルが参照可能になっていない場合があります。Windowsの場合、pip実行ファイルの格納場所をWindows環境変数PATHに追加ください。
    * 手動インストールした際のpipの格納場所は、python.exeの格納フォルダか、その中の「Scripts」フォルダです。python.exeの格納場所は、Windowsではデフォルトでは以下のいずれかが多いです。
        * C:\Users\【ユーザ名】\AppData\Local\Programs\Python\Python**\Scripts
        * C:\Python**\Scripts
* pythonの実行ファイルが参照可能になっていない場合があります。Windowsの場合、前述のpython.exeの格納場所をWindows環境変数PATHに追加ください。

### fmpictが見つからないといったエラーが発生

* fmpictの実行ファイルが参照可能になっていない場合があります。fmpictの実行ファイルは、前述のpipと同じフォルダか、その中の「Scripts」フォルダに格納されています。Windowsの場合、fmpict実行ファイルの格納場所をWindows環境変数PATHに追加ください。
* Macなどでは、稀に複数バージョンのPythonが同居していて、pipとpythonのバージョンがばらばらになっていることが、エラーの原因となる場合があります。「type pip」「where pip」などで実行ファイルの格納場所を確認して、pipと実行に用いるPythonのバージョンが一致いていることを確認してみてください。問題があった場合、実行に用いるPythonに同梱しているpipでインストールください。

## fmpictのアップグレード

以下を実行します。

```
pip install -U fmpict
```

## fmpictのアンインストール

以下を実行します。
```
pip uninstall fmpict
```
