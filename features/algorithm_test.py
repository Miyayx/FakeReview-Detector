#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

import fileio
import info_print
from cutclause import SentenceCutter as SC

if __name__=="__main__":
    rid_result = fileio.read_file_to_dict("objective.temp")
    replica = fileio.read_file_to_list("data/replicaId3.dat")
    #replica = fileio.read_file_to_list("data/replica_high_freq.dat")

    review_list = fileio.read_fields_from_allcsv("../data/CSV/Train/",["id","reviewContent"])

    rid_review = dict([rid,review] for rid,review in review_list)

    count = 0
    longreview = 0
    for i in replica:
        review = rid_review[i]
        sc = SC(review)
        if len(sc.cutToClauses()) <= 3:
            continue
        longreview+=1
        if rid_result[eval(i)] < 1:
            count+=1
        print i
        print rid_review[i]
        print rid_result[eval(i)]
        print "*******************************88"

    print "total",len(replica)
    print "longreview",longreview
    print "undetected",count
    print float(count)/longreview


