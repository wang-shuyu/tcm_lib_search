#encoding=utf-8
from __future__ import unicode_literals
import sys
sys.path.append("jieba")

import re
import pandas
import pickle

from sklearn.pipeline import make_pipeline
from sklearn import linear_model, preprocessing, neighbors, svm
from sklearn.pipeline import FeatureUnion, Pipeline, make_pipeline, make_union
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn import feature_selection


import jieba
# import pickle

from lib_search import get_resource_path
from m01_HerbCheck import HerbChecker

# add TCM herb dictionary
herb_file = get_resource_path('data/common_herbs.txt')
jieba.load_userdict(herb_file)
import jieba.posseg
import jieba.analyse
checker = HerbChecker(herb_file)

# load variable transformation pipe and herb token classifier model
var_transform_file = get_resource_path('data/variable_transformation.pkl')
with open(var_transform_file, 'rb') as f:
    var_transform_pipeline = pickle.load(f)

herb_model_file = get_resource_path('data/logisticreg-penaltyl1-C1.0.pkl')
with open(herb_model_file, 'rb') as f:
    herb_model = pickle.load(f)

herb_token_classifier = make_pipeline(var_transform_pipeline, herb_model)

labels = (
          'ind_after_kuohao',
          'ind_after_dunhao',
          'ind_after_yi',
          'ind_after_yong',
          'ind_after_jia',
          'ind_after_jian',
          'ind_after_qu',
          'ind_before_kuohao',
          'ind_before_dunhao',
          'ind_before_deng',
          'ind_before_tang',
          'ind_before_san',
          'ind_before_fang',
          'ind_before_gao',
          'pos_flag_pre',
          'pos_flag_curr',
          'pos_flag_next',
          'ind_herb_context',
          'ind_same_context_with_other_herb',
          'num_herb_density')

hanzi_pattern  = re.compile('[\u4e00-\u9fff]+')

def tokenize_article(book):
    text = "".join(open(book).readlines())
    words = jieba.posseg.cut(text, HMM = False)
    words = tuple(words)

    tokens = [t.word for t in words]
    token_indexes = []
    i = 0
    for t in tokens:
        idx = text.find(t, i)
        token_indexes.append(idx)
        i = idx + 1

    herb_probs = [0 for i in range(len(words))]
    for i in range(len(words)):
        if checker.check(words[i].word):
            herb_probs[i] = 1
            continue

        if i == 0:
            herb_probs[i] = 0
            continue

        # ignore if token is not chinese character
        if not hanzi_pattern.match(words[i].word):
            herb_probs[i] = 0
            continue

        feature_dict = {}

        # after indicators
        for j, term in enumerate(('）',  '、', '宜', '用', '加', '减', '去')):
            feature_dict[labels[j]] = int(words[i-1].word.endswith(term));

        # before indicators
        for j, term in enumerate(('（', '、', '等', '汤', '散', '方', '膏')):
            feature_dict[labels[7 + j]] = int(words[i + 1].word.startswith(term));

        # 词性
        feature_dict['pos_flag_pre'] = words[i-1].flag
        feature_dict['pos_flag_curr'] = words[i].flag
        feature_dict['pos_flag_next'] = words[i+1].flag

        # common herb checker frequenct of around text
        start = max(0, i - 10)
        end = min(i + 10, len(words))
        token_cnt = 0
        herb_token_cnt = 0
        ind_same_context_with_other_herb = 0
        for j in range(start, end):
            if j != i:
                token_cnt += 1
                if checker.check(words[j].word):
                    herb_token_cnt += 1

                    if ind_same_context_with_other_herb == 0 \
                       and words[i - 1].word[-1] == words[j - 1].word[-1] \
                       and words[i + 1].word[0] == words[j + 1].word[0]:
                        ind_same_context_with_other_herb = 1

        feature_dict['ind_herb_context'] = int(herb_token_cnt > 0)
        feature_dict['ind_same_context_with_other_herb'] = ind_same_context_with_other_herb
        feature_dict['num_herb_density'] = [herb_token_cnt / token_cnt]

#        print(feature_dict)
        feature_df = pandas.DataFrame(feature_dict)
#        print(feature_df)
        try:
            res = herb_token_classifier.predict_proba(feature_df)
        except ValueError:
            res = None

        if res is not None:
            herb_probs[i] = res[0, 1]
        else:
            herb_probs[i] = 0

#       print(words[i], res, herb_probs[i])

    return text, tokens, token_indexes, herb_probs

if __name__ == '__main__':
    text, tokens, token_indexes, herb_probs =  tokenize_article('/Users/songqiang/Documents/tcm_data_mining/data/tcm_lib_search/classic_tcm_literature/劝读十则-清-唐宗海.txt')
    for i in range(len(tokens)):
        print(tokens[i], token_indexes[i], herb_probs[i])
