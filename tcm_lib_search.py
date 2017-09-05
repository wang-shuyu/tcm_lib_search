#! /usr/local/bin/python3

import sys
import argparse

from lib_search import fangzi_search_article, get_resource_path

parser = argparse.ArgumentParser()
parser.add_argument("fangzi",
                    help = "composion of fangzi, quoted with each herb separated by comma")
parser.add_argument("-n", "--num_entry", type = int, default = 10,
                    help = "Number of entries to return (default 10)")
parser.add_argument("-T", "--print_original_text", action = 'store_true',
                    help = "print original text if specified")
parser.add_argument("-s", "--min_score", type = float, default = 0.2,
                    help = "Min similarity score of returned entries")

args = parser.parse_args()

if __name__ == '__main__':
    db = get_resource_path('data/metadata.sqlite')

    fangzi_search_article(args.fangzi, db,
                          num_entry = args.num_entry,
                          print_original_text = args.print_original_text,
                          min_score = args.min_score)
