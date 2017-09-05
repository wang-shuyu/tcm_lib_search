import re
import sys
import sqlite3
import pickle
import time
import argparse
import os

from fangzi_search import  compute_cosine_similarity, get_fangzi, fangzi_to_str

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def fangzi_search_article(fangzi_str, db,
                          num_entry = 10,
                          print_original_text = True,
                          min_score = 0.2):
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    herb_fangzi_dict = pickle.load(open('data/herb_fangzi_dict.pickle', 'rb'))

    fangzi_ids = set()
    fangzi = get_fangzi(fangzi_str)
    fangzi_lst = list(fangzi.keys())
    fangzi_lst.sort()

    for i, h1 in enumerate(fangzi_lst):
        if h1 in herb_fangzi_dict:
            for h2 in fangzi_lst[(i + 1):]:
                if h2 in  herb_fangzi_dict[h1]:
                    fangzi_ids = fangzi_ids.union(herb_fangzi_dict[h1][h2])

    fangzi_ids = list(fangzi_ids)

#     scores = []
#     for i, id in enumerate(fangzi_ids):
#         if i % 100 == 0:
#             print("Progress {:f}".format(i / len(fangzi_ids)), time.ctime())
#         c.execute('select herb from fangzi where id  = ?', [id])
# #        candidate = ', '.join([r['herb'] for r in c.fetchall()])
#         tmp = [r['herb'] for r in c.fetchall()]
#         candidate = dict(zip(tmp, [1] * len(tmp)))
#         score = compute_cosine_similarity(fangzi, candidate)
#         scores.append((score, id, candidate))

    scores = []
    c.execute('select id, herb from fangzi where id in ({}) order by id'.format(','.join([str(id) for id in fangzi_ids])))
    id = None
    candidate = {}
    for r in c.fetchall():
        if not id:
            candidate[r['herb']] = 1
            id = int(r['id'])
        elif int(r['id']) ==  id:
            candidate[r['herb']] = 1
        else:
            score = compute_cosine_similarity(fangzi, candidate)
            if score >= min_score:
                scores.append((score, id, candidate))
            id = int(r['id'])
            candidate = {r['herb']:1}

    scores.sort(key = lambda x: 1 - x[0])
    i = 1
    for r in scores[:min(len(scores), num_entry)]:
        print('No. {:d}; Score: {:f}; Formula:  [{}]'.format(i, r[0],  ', '.join( sorted(list(r[2].keys())) )))
        c.execute('select * from fangzi_article where fangzi_id = ?', [r[1]])
        entry = list(c.fetchone())
        entry[1] = entry[1].replace('/Users/songqiang/Documents/tcm_data_mining/data/tcm_lib_search/classic_tcm_literature/', '').replace('.txt', '')
        print(entry)
        if print_original_text:
            c.execute('select * from fangzi_snippets where fangzi_id = ?', [r[1]])
            snippets = tuple(c.fetchone())
            text = snippets[1]
            print(text)
        print('----------------------------------------------------------------')
        i = i + 1
