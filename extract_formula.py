#! /usr/local/bin/python3

import sys
import warnings
import argparse

from pprint import pprint

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-T", "--print_original_text", action = 'store_true',
                        help = "print original text if specified")
    parser.add_argument("book", nargs = '?',
                        help = "text file to be parsed")

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_arguments()

    from m02_herb_classifier import numeric_column_selector, pos_column_selector, \
        pos_label_encoder, pos_label_onehot_encoder

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        from m03_article_tokenizer import tokenize_article

    from m04_formula_extractor import extract_fangzi

    text, tokens, token_indexes, herb_probs = tokenize_article(args.book)
    fangzi_list, fangzi_pos_list = extract_fangzi(tokens, token_indexes, herb_probs)

    for i in range(len(fangzi_list)):
        print('\n\n')
        print(' '.join(fangzi_list[i]))
        if args.print_original_text:
            print('-' * 60)
            start = max(fangzi_pos_list[i][0] - 30, 0)
            end = min(fangzi_pos_list[i][1] + 30, len(text))
            print(text[start:end])
