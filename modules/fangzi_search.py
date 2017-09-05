#! /usr/local/bin/python3

import re
import math
import sys

def read_fangzi_db(f):
    方剂药物 = open(f)
    h = 方剂药物.readline()
    药物 = h.strip().split(sep = ',')[1:]
    db = []
    for line in 方剂药物:
        fields = line.split(sep = ',')
        编号 = fields[0]
        vals = [float(e) for e in fields[1:]]
        d = dict([e for e in zip(药物, vals) if abs(e[1]) > 1e-10])
        db.append((编号, d))
    return db

def compute_cosine_similarity(d1, d2):
    """
    compute cosine similariry between two fangzi
    d1 = {'当归':1, '附子':1, '炙甘草':1}
    d2 = {'当归':1, '黄芩':1, '炙甘草':1}
    """
    yaowu = list(set(d1.keys() | d2.keys()))
    l1 = [d1[e] if e in d1 else 0 for e in yaowu]
    l2 = [d2[e] if e in d2 else 0 for e in yaowu]
    normal1 = math.sqrt(sum([i ** 2 for i in l1]))
    normal2 = math.sqrt(sum([i ** 2 for i in l2]))
    cp = sum([l1[i] * l2[i] for i in range(len(l1))])
    return cp / (normal1 * normal2)

def get_fangzi(s):
    yaowu =[f.strip() for f in  s.replace(' ', ',').replace('，', ',').split(sep = ',') if f]
    return dict(zip(yaowu, [1 for e in yaowu]))

def fangzi_to_str(d):
    return ', '.join([k + '(' + str(v) + ')' for k, v in  d.items()])

def fangzi_search(target, db, cutoff = 0.3):
    result = list()
    i = 0
    for 编号, 组成 in db:
        similarity = compute_cosine_similarity(target, 组成)
        result.append((i, similarity))
        i = i + 1

    result = [e for e in result if e[1] >= cutoff]
    result.sort(key = lambda e: e[1], reverse = True)
    for id, 相似度 in result:
        print("{:d}\t{:f}\t{}".format(int(db[id][0]), 相似度,  fangzi_to_str(db[id][1])))

if __name__ == '__main__':
    target_s = ','.join(sys.argv[1:])
    target = get_fangzi(target_s)
    db = read_fangzi_db('/Users/songqiang/Documents/tcm_data_mining/data/fangzi_chengfen_matrix.csv')
    print(fangzi_to_str(target))
    print('------------------------------------')
    fangzi_search(target, db)
