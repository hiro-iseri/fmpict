# FMPict User’s Guide

## Overview

FMPict help test design by classification tree method.
FMPict retrieves a freemind file descripted classification tree, and generates test case covering n-wise coverage(n:1-3).

The advantages of PMPict:

* FMPict can express a combination test in freeminde. So FMPict can clearly express equivalence partitions and abstract structure of test conditions.
* FMPict can erase repeated descriptions of test conditions.

## Install

the following tools should be installed:

* PICT
* FreeMind
* Python

### Install Command

```
pip install fmpict
```

### Uninstall Command

```
pip uninstall fmpict
```

### Execution check environment

Windows 10, MaxOS X

## Run fmpict

if you run the following command, fmpict generates a testcase by freemind file and output it to standard output.

`fmpict [filepath of FreeMind file]`

if you run the following comannd, fmpict generates testcase file.

`fmpict [filepath of FreeMind file] -s -g`

## Style of FreeMind

### Basic Node Type

* Test Condition Node
    * Test Input. This node corresponds to classification in the classification tree method.
    * Node with folder icon, or Nodes that start with the @ character are test condition node.
* Value Node
    * Value in Test Condition Node. This node corresponds to class in the classification tree method.
    * a child of the test condition node, and the inner node in the test condition node is the value node

Example:

![basic_rule](image/en/test_input.png)

when fmpict retrieves the above figure, fmpit generates the following text file and input it to PICT.

```
classification1:class1, class2, class3
classification2:class4, class5
```

### Comment and invalid node

* Nodes starting with "#" are comment nodes. Comment nodes and their descendants are ignored.

Example:

![basic_rule](image/en/comment.png)

when fmpict retrieves the above figure, fmpit ignores "#memo" and "sample for sample"

### Hierarchy of test conditions and values

Test conditions and values ​​can have a hierarchical structure.

テスト条件ノード、値ノードは階層化が可能です。

* If the value is hierarchical, only the end value is used
* If test conditions are hierarchical, test conditions with only value nodes as descendants are used.

Example:

![layered](image/en/test_struct.png)

上記のFreemindが入力された場合、fmpictはTC2、TC3、value1、value3、value4を使用します。
fmpictはTC1、value2は無視します。

### Eliminate duplication with link

Link notation is used to describe overlapping test conditions together.

* Nodes starting with ">" are common definition nodes.
* Nodes starting with "<" are references to common definition nodes.
* If the node texts after ">" and "<" match, "reference to common definition node" will be collectively replaced with the child node of "common definition node".

In the following example, all "<Size" nodes will be replaced by child nodes of ">Size".

![basic_rule](image/en/link.png)

When FMPict is executed in the above figure, the following text data is generated and input to PICT.

```
Food Size:Large,Small
Drink Size:Large,Small,Medium
```

### Select a node by tag

Tag notation is used to narrow down the nodes to be analyzed.

* A character string surrounded by “[” and “]” is a tag. Write the tag at the beginning of the node string. Please write only half-width alphanumeric characters and underscores
    * Tags can be attached to all nodes (including test condition nodes, value nodes, links, and options). Always write the tag first. For example, when adding a tag to a test condition node, describe as [[tag] @test condition name].
    * The tag is removed from the output.
    * Multiple tags can be listed like "[Tag 1] [Tag 2]".
* Enable tag notation with optional arguments described below.
    * If the tag option (-t) is specified in the option argument, the node with the tag specified in the argument is processed. Nodes with tags not specified in the argument are ignored.

This section describes the case where the following FreeMind files are processed.

![tag](image/tag.png)


[When tag notation is not enabled] When this example is executed with the following command, “test input 1”, “value 1”, and “value 2” are input to PICT.

```
fmpict targetfile
```

[When only tag1 is selected] When executed with the following command, "test input 1" and "value 1" are input to PICT. "Value 2" is ignored.

```
fmpict targetfile -t "[tag1]"
```



### Option Node

* Child nodes of nodes with {sub_model_definitions} written are transferred to the sub_model_definitions part of the PICT input file.
* Child nodes of nodes with {constraint_definitions} are transferred to the constraint_definitions part of the PICT input file.
* Child nodes of nodes with {pict_exec_option} are expanded to PICT runtime options.

以下のFreeMindファイルで実行した場合について説明します。

![basic_rule](image/option_rule.png)

上記の図でFMPictを実行した場合、以下のPICT入力データが生成されます（{constraint_definitions}の内容が末尾に追記される）。

```
文字コード:UTF-8,SHIFT-JIS,ASCII
半角・全角:全角あり,全角なし
文字長:上限以上,範囲内,空文字
IF [文字コード] = "ASCII"   THEN [半角・全角] <= 全角なし;
```

そして以下のPICT実行コマンドが実行されます({pict_exec_option}指定テキストを実行コマンド末尾に付記)。

```
pict PICT入力データファイル /s
```

## FMPictの実行オプション

fmpictは実行オプションを持ちます。

### オプション引数

* -h
    * ヘルプを表示します。
* -p FILE_PATH
    * 指定されたFILE_PATHにPICT入力ファイルを保存します（このオプションがない場合、FILE_PATHはtemp.txtになります）。
* -g
    * PICT実行をスキップします。PICT入力ファイル生成のみ行います。
* -s
    * 中間生成するPICT入力ファイルを削除せず保持します（このオプションがない場合、PICT入力ファイルは自動削除されます）。
* -t
    * タグ絞り込みを行います。"[tag名]"を列記した文字列を指定します。指定された文字列以外のタグノードは解析から除外されます。

実行例：sample.mmを入力に、pict_list.txtにPICT入力ファイルを保存

```
fmpict sample.mm -s -g -p pict_list.txt
```

### ヘルプ一覧
```
This tool generates test cases using freemind and pict

positional arguments:
  freemind_file_path    *.mm input file

optional arguments:
  -h, --help            show this help message and exit
  -p PICT_FILE_PATH, --pict_file_path PICT_FILE_PATH
                        save pict file to specified path
  -g, --genparamlist    execute until pict file generation
  -s, --savepictfile    save pict file
  -t SELECT_TAG_LIST, --select_tag_list SELECT_TAG_LIST
                        select specified tag in generating
```

## Contact

Github: https://github.com/hiro-iseri/fmpict  
Mail: iseri.hiroki[＠]gmail.com  
Author: Hiroki Iseri
