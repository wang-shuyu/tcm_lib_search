#encoding=utf-8
from __future__ import unicode_literals
import re

hanzi_pattern = re.compile(u"[\u4e00-\u9fa5]+")

def create_line_pos_index(f):
    line_starts = []
    line_starts.append(0)
    for line in open(f):
        line_starts.append(line_starts[-1] + len(line))
    return line_starts

def clean_herb_name(s):
    if s.endswith('方') or s.endswith('散') or s.endswith('剂') or s.endswith('丸') or s.endswith('汤'):
        s = s[:-1]
    return s

def extract_fangzi(tokens, token_indexes, herb_probs, max_sep = 10):
    start = -1
    end = -1
    i = 0
    max_len = len(tokens)
    fangzi_list = []
    fangzi_pos_list = []
    while i < max_len:
        if tokens[i] in ('(', '（'):
            while i < max_len and tokens[i] not in (')', '）'):
                tokens[i] = ''
                i += 1
        if i < max_len and len(tokens[i]) <= 8 and herb_probs[i] >= 0.7:
            if start == -1:
                start = i
                end = i
            else:
                if len(''.join(tokens[(end +1):i])) <= max_sep:
                    end = i
                else:
                    fangzi = [tokens[_] for _ in range(start, end + 1) if herb_probs[_] >= 0.7]
                    fangzi = [clean_herb_name(_) for _ in fangzi]
                    fangzi = [_ for _ in fangzi if len(_) > 0]
                    fangzi = list(set(fangzi))
                    if len(fangzi) >= 3:
                        fangzi_list.append(fangzi)
                        fangzi_pos_list.append((token_indexes[start], token_indexes[end] + len(tokens[end])))
                    start = i
                    end = i
        if i < max_len and not hanzi_pattern.match(tokens[i]):
            tokens[i] = ''
        i = i + 1
    if start != -1:
        fangzi = [tokens[_] for _ in range(start, end + 1) if herb_probs[_] >= 0.7]
        fangzi = [clean_herb_name(_) for _ in fangzi]
        fangzi = list(set(fangzi))
        if len(fangzi) >= 2:
            fangzi_list.append(fangzi)
            fangzi_pos_list.append((token_indexes[start], token_indexes[end] + len(tokens[end])))
    return fangzi_list, fangzi_pos_list

if __name__ == '__main__':
    pass
