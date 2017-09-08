# Traditional Chinese Medicine Formula Extraction and Query

This package provides a python implementation of a text mining / machine
learning framework that automatically extracts traditional Chinese medicine formula
from unstructured free texts and enables literature retrieval based on formula
composition.

## Installation

This package has the following dependencies
1. Python >= 3.5
2. sklearn >= 0.19
3. pandas >= 0.18
4. numpy >= 1.13

Suppose you already have the above packages intalled in your environment, you can
download the tcm_lib_search package source code by running:
```
git clone https://github.com/wang-shuyu/tcm_lib_search.git
```

Next, you need to download the supplementary data file
(tcm-lib-search-data-v1.0.tar.gz) from
https://1drv.ms/f/s!Am5VX_Ff6cC6lm9qf73kVS3NNl7t, and uncompress the contents of
the data file to tcm_lib_search/data directory

## Usage

There are two executable scripts: *extract_formula.py* and  *tcm_lib_search.py*.

### Use extract_formula.py to extract TCM formulas

The scripts extract_formula.py takes a text file of traditional Chinese
medicine literature as input, and extracts all formula from that book.

The basic command to invoke this command is as follows: ```extract_formula.py <filename>```. For example,
```bash
extract_formula.py 伤寒论-汉-张仲景.txt
```
Note that the input file must be in plain text file with all markup tokens removed. The above command parses the input files and output the list of extracted formula to standard output.

In order to get the original text where the extracted formulas, we can add '-T' option to the command:
```bash
extract_formula.py -T 伤寒论-汉-张仲景.txt
```

### Use tcm_lib_search.py to search for origin of formula

With the automatic formula extraction method, we preprocessed a corpus of 791 classical TCM literatures, and established a database that enable document retrivial based on formula composition. This functionality is provided by the script tcm_lib_search.py.

For example, the command below searches for literatures that described Xiao Yan San:
```bash
tcm_lib_search.py '柴胡  甘草 茯苓 当归 白芍 白术‘
```
The  tcm_lib_search.py accepts the following additional options:
* -T: if specified, the script prints out the original text scripts
* -n: speficifies the maximum number of entries to return
* -s: speficifies the minumum similarity score between query formula and search results
