#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""
import sys
import os
sys.path.append('/home/yang/GraduationProject/features/')
import fileio

REVIEW_PATH = "../data/CSV/Train/"
FEATURE_PATH = "../data/features/"
if __name__=="__main__":
    rid_rlenratio = {}
    rid_rlendeviation = {}

    filenames = os.listdir(REVIEW_PATH)
    for filename in filenames:
        name = ""
        if not filename.split(".")[1] == "csv2":
            continue
        else:
            name = filename.split(".")[0]
        reviewList = fileio.read_fields_from_CSV(REVIEW_PATH,filename,["id","reviewContent"])
        rid_len = dict([rid,len(review)//3] for rid,review in reviewList)
        review_len = dict([review,len(review)//3] for rid,review in reviewList)
        avg_len = float(sum(rid_len.values()))/len(rid_len)
        print name,avg_len
        rid_rlendeviation.update(dict([k,v-avg_len] for k,v in rid_len.iteritems()))
        rid_rlenratio.update(dict([k,v/avg_len] for k,v in rid_len.iteritems()))
    fileio.recordToFile(FEATURE_PATH+'rid_lendeviation.dict',rid_rlendeviation)
    fileio.recordToFile(FEATURE_PATH+'rid_lenratio.dict',rid_rlenratio)



