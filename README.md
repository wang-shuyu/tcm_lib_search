# Traditional Chinese Medicine Formula Extraction and Query

This package provides a python implementation of a text mining / machine
learning framework that automatically extracts traditional Chinese medicine
formula from unstructured free texts and enables literature retrieval based on
formula composition.

## Download software

### Download pre-packaged executable programs

We pre-packaged the executables with all dependencies and supplementary
datasets. The pre-packaged executables can be downloaded from the links below

- Windows
    - Formula extraction program: [extract_formula for Windows](https://figshare.com/articles/Standalone_executable_program_of_extract_formula_for_Windows_platform/5504956)
    - Formula query program: [tcm_lib_search for Windows](https://figshare.com/articles/Standalone_executable_program_of_tcm_lib_search_for_Windows_platform_/5504968)
- Mac OS
    - Formula extraction program: [extract_formula for Mac OS](https://figshare.com/articles/Standalone_executable_program_of_extract_formula_for_Mac_OS_platform/5504950)
    - Formula query program: [tcm_lib_search for Mac OS](https://figshare.com/articles/Standalone_executable_program_of_tcm_lib_search_for_Mac_OS_platform/5504953)

After downloading these programs, uncompress the zip file. These programs are designed to run in console mode. Windows user can use PowerShell (see https://technet.microsoft.com/en-us/library/ff629472.aspx on how to start PowerShell). Mac users can use the Terminal application (http://blog.teamtreehouse.com/introduction-to-the-mac-os-x-command-line). Basic familiarity with terminal commands are necessary for running these programs.

### Download and install from source code
Alternatively, you can download the source code and build the package from scratch. This package has the following dependencies
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
(tcm_lib_search-data-v1.0.tar.gz) from
https://figshare.com/articles/data_directory_tarball_for_tcm_lib_search_package/5504944, and uncompress the contents of
the data file to tcm_lib_search/data directory.


## Usage

There are two executable scripts: *extract_formula.py* and *tcm_lib_search.py* from you are running the source code version. If you are running the pre-packaged standable executables, the program names are *extract_formula* and *tcm_lib_search* respectively.

### Use extract_formula.py to extract TCM formulas

The scripts extract_formula.py takes a text file of traditional Chinese
medicine literature as input, and extracts all formula from that book.

The basic command to invoke this command is as follows: ```extract_formula.py
<filename>```. For example, you can download the text file of Shan Han Lun from https://figshare.com/articles/Shan_Han_Lun/5504194. After you get the text file 伤寒论-汉-张仲景-Shan-Han-Lun.txt,
run the *extract_formula.py* program as following, you should see the list of extracted formulas.

```bash
extract_formula.py 伤寒论-汉-张仲景-Shan-Han-Lun.txt
```

Note that the input file must be in plain text file with all markup tokens
removed. The above command parses the input files and output the list of
extracted formula to standard output.

In order to get the original text where the extracted formulas, we can add '-T'
option to the command:

```bash
extract_formula.py -T 伤寒论-汉-张仲景-Shan-Han-Lun.txt
```

### Use tcm_lib_search.py to search for documents based on formula ingredients

With the automatic formula extraction method, we preprocessed a corpus of 791
classical TCM literatures, and established a database that enables document
retrivial based on formula ingredients. This functionality is provided by the
script *tcm_lib_search.py*. Given the list of herbs in a formula, the script
searches against the database, and find any literatures that includes the same
or similar formula. This functionality assists medical practioners to study the
varietion of formula and the effects of those varietions.

For example, the command below searches for literatures that described formulas
similar to Xiao Yan San:

```bash
tcm_lib_search.py '柴胡  甘草 茯苓 当归 白芍 白术'
```

The tcm_lib_search.py accepts the following options:
* -T: switches the script to print out the original text snippets
* -n: speficifies the maximum number of entries to return
* -s: speficifies the minumum similarity score between query formula and search
  results. The similar score is between 0.0 and 1.0, and the higher the score
  is, the more similar the result is to the target

Example 1: the command below searches formulas similar to the Xiao Yan San, and also prints the original text snippets where the formulas are recorded:

```bash
tcm_lib_search.py -T '柴胡  甘草 茯苓 当归 白芍 白术'
```

Example 2: the command below searches formulas similar to the Xiao Yan San with a cutoff 0.85, and also prints the original text snippets where the formulas are recorded:

```bash
tcm_lib_search.py -T -s 0.85 '柴胡  甘草 茯苓 当归 白芍 白术'
```

Example 3: the command below searches top 5 formulas in the database that most
similar to the Xiao Yan San, and also prints the original text snippets:

```bash
tcm_lib_search.py -T -n 5 '柴胡  甘草 茯苓 当归 白芍 白术'
```

## Supplementary data
The raw text files in this study is downloaded from the Medical Collections of Dai Zhi Ge: www.daizhige.org/医藏/

The common herb dictionary is available at https://figshare.com/articles/Dictionary_of_common_herbs_used_in_traditional_Chinese_medicine/5504935

The SQLite database file for the extracted formulas is available at https://figshare.com/articles/SQLite_database_file_with_extracted_herbal_formulas_and_source_information/5504941
