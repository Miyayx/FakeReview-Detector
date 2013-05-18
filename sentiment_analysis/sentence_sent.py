#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""
import sys
sys.path.append('/home/yang/GraduationProject/nlpirpy/')
from WordSegmentation import WordSegmentation as WS

import fileio

import matplotlib.pyplot as plt
import numpy as np

sentWordPath = '../data/WordSent/'

pos_adj = fileio.read_list_from_file(sentWordPath+'positive.dat')
neg_adj = fileio.read_list_from_file(sentWordPath+'negative.dat')
neg_adv = fileio.read_list_from_file(sentWordPath+'negative_adv.dat')
degree_adv = fileio.read_list_from_file(sentWordPath+'degree_adv.dat')

def calculateSentenceSent(ws,sentence):
    """
    str -> int(index of sentiment)
    """
    sent = 0
    ws.setString(sentence.encode('utf-8'))
    l = ws.getSegmentResult()
    for i in range(len(l)):
        w = l[i]
        if w in pos_adj:
            c = 1
            if i > 0:
                if l[i-1] in neg_adv:
                    c = c*(-1)
                elif l[i-1] in degree_adv:
                    c+=1
            sent+=c
        if w in neg_adj:
            c = -1
            if i > 0:
                if l[i-1] in neg_adv:
                    c = c*(-1)
                elif l[i-1] in degree_adv:
                    c+=1
            sent+=c
    return sent

if __name__ == '__main__':
    all_id_clauses = fileio.read_dict_from_file('../features/data/allClause_id.dat')
    ws = WS()
    id_clause_sent = dict([v,calculateSentenceSent(ws,str(k).decode('utf-8'))] for k,v in all_id_clauses.iteritems() )
    ws.exit()
    fileio.record_to_file('../data/SentenceSent/sentenceid_sent.dat',id_clause_sent)
    id_review_Temp = fileio.read_dict_from_file('../features/data/all_id_temp.dat')
    rid_sent = {}
    for rid,v in id_review_Temp.items():
        r_sent = 0
        for i in v:
           # print v
           # print i
           # print id_clause_sent[i]
            try:
                r_sent += id_clause_sent[i]
            except:
                print 'ErrorKey:',i
        try:        
            rid_sent[rid] = float(r_sent)/len(v)
        except:
            rid_sent[rid] = 0
    fileio.record_to_file('../data/SentenceSent/reviewid_sent.dat',sorted(rid_sent.items(),key = lambda x:x[1],reverse=True))
    fileio.record_to_file('../data/features/sentiment_id_feature.dat',rid_sent)

    l = rid_sent.values()
    plt.hist(l,range(-1,10))
    plt.show()
    
    highSentD = dict([k,1 if v>4 else 0] for k,v in rid_sent.iteritems())
    fileio.record_to_file('../data/features/high_sent.dat',highSentD)

    highSentList = [k for k,v in rid_sent.iteritems() if v > 4]
    fileio.record_to_file('../havealook/highSentiment_id.dat',highSentList)

