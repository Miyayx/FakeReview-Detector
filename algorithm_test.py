#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

from utils import fileio
from utils import info_print
from utils.cutclause import SentenceCutter as SC

if __name__=="__main__":
    rid_result = fileio.read_file_to_dict("objective.temp")
    replica = fileio.read_file_to_list("data/target/all_fake.dat")
    #replica = fileio.read_file_to_list("data/replica_high_freq.dat")

    review_list = fileio.read_fields_from_allcsv("data/CSV/Train/",["id","reviewContent"])

    rid_review = dict([rid,review] for rid,review in review_list)

    count = 0
    longreview = 0
    for i in replica:
        i = str(i)
        review = rid_review[i]
        sc = SC(review)
        #if len(sc.cutToClauses()) <= 3:
        #    continue
        longreview+=1
        if rid_result[eval(i)] < 0.3:
            count+=1
        print i
        print rid_review[i]
        print rid_result[eval(i)]
        print "*******************************88"

    print "total",len(replica)
    print "undetected",count
    print float(count)/longreview


