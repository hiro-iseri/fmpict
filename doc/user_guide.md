# FMPict User’s Guide

## Overview

FMPict helps test design by classification tree method.
FMPict generates test case covering n-wise coverage(n:1-3) from a freemind file descripted classification tree.

## Install

the following tools should be installed:

* PICT
    * FMPict must be able to run PICT Application. For Windows, the folder path containing pict.exe must be added to the system environment variable "PATH".
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

### Checked Execution environment

Windows 10, MaxOS X

## Run fmpict

When the following command is executed, FMPict generates a testcase by FreeMind file and output it to standard output.

`fmpict [filepath of FreeMind file]`

When the following command is executed, fmpict generates test condition file.

`fmpict [filepath of FreeMind file] -s -g -p testcondition.txt`

## Style of FreeMind

### Basic Node Type

fmpict describes test conditions with two basic nodes.

* Test Condition Node
    * Test Input. This node corresponds to classification in the classification tree method.
    * Node with folder icon, or Nodes that start with the '@' character are test condition node.
* Value Node
    * Value in Test Condition Node. This node corresponds to class in the classification tree method.
    * A child of the test condition node is the value node

Example:

![basic_rule](image/en/test_input.png)

when fmpict retrieves the above figure, fmpit generates the following text file and input it to PICT.

```
classification1:class1, class2, class3
classification2:class4, class5
```

### Comment and invalid node

The Nodes starting with "#" are comment nodes.
Comment nodes and their descendants are ignored.

Example:

![basic_rule](image/en/comment.png)

when fmpict retrieves the above figure, fmpit ignores "#memo" and "sample for sample"

### Hierarchy of test conditions and values

Test conditions and values ​​can have a hierarchical structure.

* If the value is hierarchical, fmpict only use the end value node.
* If test conditions are hierarchical, fmpict only use test conditions with only value nodes as descendants.

Example:

![layered](image/en/test_struct.png)


If FMPict retrieves the above Freemind file, fmpict uses TC2, TC3, value1, value3, value4, and fmpict ignores TC1 and value2.

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

![tag](image/en/tag.png)


[When tag notation is not enabled] When this example is executed with the following command, “Small”, “Large” are input to PICT.

```
fmpict targetfile
```

[When only tag1 is selected] When executed with the following command, "Small" is input to PICT. "Large" is ignored.

### Option Node

* Child nodes of nodes with {sub_model_definitions} written are transferred to the sub_model_definitions part of the PICT input file.
* Child nodes of nodes with {constraint_definitions} are transferred to the constraint_definitions part of the PICT input file.
* Child nodes of nodes with {pict_exec_option} are expanded to PICT runtime options.

Example:

![basic_rule](image/en/option.png)

When fmpict receives the above figure, the following PICT execution command is executed ({pict_exec_option} specification text is added at the end of the execution command).

```
pict [freemind file] /s
```

## Selecting test coverage criteria

fmpict sets test coverage by specifying options to {pict_exec_option}

### Select 2-wise coverage 100%

If you do not set any options, fmpict creates a test case with 2wise coverage 100%

Input File:

![c2](image/en/nwise_example.png)

Output:

```
Y       X       Z
Y2      X2      Z2
Y2      X1      Z1
Y1      X1      Z2
Y1      X2      Z1
```

### Select 1-wise coverage 100%

When creating a test case with 1wise coverage 100%, enter the PICT command “/o:1” in the child node of {pict_exec_option}.

Input File:

![c2](image/en/1wise.png)

Output:

```
Y       X       Z
Y2      X2      Z2
Y1      X1      Z1
```

If you want to set 3wise coverage 100%, specify / o: 3 as well

## Detailed Option

* -h
    * Display help.
* -p FILE_PATH
    * Save the PICT input file to the specified FILE_PATH (if this option is not present, FILE_PATH will be temp.txt).
* -g
    * Skip PICT execution. Only PICT input file generation is performed.
* -s
    * Keep the PICT input file that is generated intermediately without deleting it (the PICT input file is automatically deleted if this option is not present).
* -t
    * Filters tags. Specify a character string that lists "[tag name]". Tag nodes other than the specified string are excluded from the analysis.

Execution example: input sample.mm and save PICT input file to pict_list.txt

```
fmpict sample.mm -s -g -p pict_list.txt
```

## Contact

Github: https://github.com/hiro-iseri/fmpict  
Mail: iseri.hiroki[＠]gmail.com  
Author: Hiroki Iseri
