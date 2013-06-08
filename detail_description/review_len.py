#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""
import sys
import os
sys.path.append('/home/yang/GraduationProject/utils/')
import fileio
from cutclause import SentenceCutter as SC

REVIEW_PATH = "../data/CSV/Train/"
FEATURE_PATH = "../data/features/"

def remove_alpha(review):
    sc = SC(review)
    clauses = sc.cutToClauses()
    review = ""
    for c in clauses:
        review+=c
    return review

def length_proc(reviewobj):
    reviewobj["length"] = len(unicode(reviewobj["content"],"utf-8"))
    return reviewobj["length"]

def review_len(reviews):
    pass

if __name__=="__main__":
    rid_rlenratio = {}
    rid_rlennorm = {}
    rid_rlenrationorm = {}

    filenames = os.listdir(REVIEW_PATH)
    for filename in filenames:
        name = ""
        if not filename.split(".")[1] == "csv2":
            continue
        else:
            name = filename.split(".")[0]
        reviewList = fileio.read_fields_from_csv(REVIEW_PATH+filename,["id","reviewContent"])
        rid_review = dict(reviewList)
        rid_review = dict([k,remove_alpha(v)] for k,v in rid_review.iteritems())
        
        rid_len = dict([rid,len(unicode(review,"utf-8"))] for rid,review in reviewList)
        review_len = dict([review,len(unicode(review,"utf-8"))] for rid,review in reviewList)
        
        #for k,v in review_len.items():
        #    print k,v

        avg_len = float(sum(rid_len.values()))/len(rid_len)
        print name,avg_len
        #ratio = dict([k,abs(v-avg_len)/avg_len] for k,v in rid_len.iteritems())
        ratio = dict([k,v/avg_len] for k,v in rid_len.iteritems())
        rid_rlenratio.update(ratio)
        ratio_max = max(ratio.values())
        ratio_min = min(ratio.values())
        rid_rlenrationorm.update(dict([k,(v-ratio_min)/(ratio_max-ratio_min)] for k,v in ratio.iteritems()))
        rid_rlennorm.update(dict([k,(v-ratio_min)/(ratio_max-ratio_min)] for k,v in rid_len.iteritems()))

    fileio.record_to_file(FEATURE_PATH+'rid_len.dict',rid_len)
    fileio.record_to_file(FEATURE_PATH+'rid_lenratio.dict',rid_rlenratio)
    fileio.record_to_file(FEATURE_PATH+'rid_lenrationorm.dict',rid_rlenrationorm)
    fileio.record_to_file(FEATURE_PATH+'rid_lennorm.dict',rid_rlennorm)

