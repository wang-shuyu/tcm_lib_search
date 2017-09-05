# Traditional Chinese Medicine Formula Extraction and Query

This package provides a python implementation of a text mining / machine
learning framework to automatically extract traditional Chinese medicine formula
from unstructured free texts and enable literature retrieval based on formula
composition.

## Installation

This package has the following dependencies
1. Python >= 3.5
2. sklearn >= 0.19
3. pandas >= 0.18
4. numpy >= 1.13

Suppose you already have these packages intalled in your environment, you can
download the tcm\_lib\_search package source code by running:
```
git clone https://github.com/wang-shuyu/tcm\_lib\_search.git
```

Next, you need to download the supplementary data file
(tcm-lib-search-data-v1.0.tar.gz) from
https://1drv.ms/f/s!Am5VX_Ff6cC6lm9qf73kVS3NNl7t, and uncompress the contents of
the data file to tcm\_lib\_search/data directory

## Usage

There are two executable scripts: *extract\_formula.py* and  *tcm\_lib\_search.py*.

### Use extract\_formula.py to extract TCM formulas

The scripts extract\_formula.py takes a text file with traditional Chinese
medicine literature as input, and extracts all formulas from that book.

The basic command to invoke this command is as follows: ```extract\_formula.py <filename>```. For example,
```bash
extract\_formula.py 伤寒论-汉-张仲景.txt
```
Note that the input file must be in plain text file with all markup tokens removed. The above command parses the input files and output the list of extracted formula to standard output.

In order to get the original text where the extracted formulas, we can add '-T' option to the command:
```bash
extract\_formula.py -T 伤寒论-汉-张仲景.txt
```

### Use tcm\_lib\_search.py to search for origin of formula

Given the composition of a formula, the script tcm\_lib\_search.py searches a
pre-calculated database, and returns the original literature where the formula
or similar formula was described.

For example, the command below searches for literatures that described Xiao Yan San:
```bash
tcm\_lib\_search.py '柴胡  甘草 茯苓 当归 白芍 白术‘
```
The  tcm\_lib\_search.py accepts the following additional options:
* -T: if specified, the script prints out the original text scripts
* -n: speficifies the maximum number of entries to return
* -s: speficifies the minumum similarity score between query formula and search results
