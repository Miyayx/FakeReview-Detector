#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

import fileio

CATEGORY_FILE="data/category.dat"
CLAUSE_FILE="data/clauseDict.dat"
CATE_SENT_FILE="data/category_sent.dat"

if __name__=='__main__':
    sent_cate = {}
    with open(CATEGORY_FILE,'r') as f:
        for line in f.readlines():
            sentence = line.strip('\n').split(' ')[1]
            print sentence
            cate_num = (line.strip('\n').split(' ')[0][0])
            print cate_num
            sent_cate[sentence] = cate_num

    clause_dict = fileio.read_file_to_dict(CATE_SENT_FILE,reverse=True)
    #clause_dict = dict([k,v] for k,v in clause_dict.iteritems() if v > 2 )

#    new_sent_cate = dict([k,0] for k in clause_dict.keys() )
    new_sent_cate = dict([k,v] for k,v in clause_dict.iteritems() )
    for k,v in new_sent_cate.items():
        if v != 0:
            continue
        if sent_cate.has_key(k):
            new_sent_cate[k] = sent_cate[k]
        elif len(str(k)) <= 6:
            new_sent_cate.pop(k)
        else:
            pass

    cate_sent = sorted(new_sent_cate.items(),key=lambda x:x[1],reverse = True)

    fileio.record_to_file(CATE_SENT_FILE,[[v,k] for k,v in cate_sent])

