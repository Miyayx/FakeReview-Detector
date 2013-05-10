#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""
from cutClause import SentenceCutter
from FileIO import FileIO

CATE_SENT_FILE="data/category_sent.dat"

if __name__=='__main__':
    fio = FileIO()
    sent_cate = fio.readFileToDict(CATE_SENT_FILE,reverse=True)
    reviewList = fio.readFieldsFromAllCSV("../data/CSV/Train/",["id","reviewContent"])
    for r_id,review in reviewList:
        sc = SentenceCutter(review)
        clauses = sc.cutToClauses()
        count = 0
        for i in clauses:
            if sent_cate.has_key(i.encode('utf-8')):
                count+=1
        ratio = float(count)/len(clauses)
        #if ratio > 0.8 and len(clauses)>3:
        #    print r_id,review
        print "%s\t\t%f"%(r_id,ratio)


