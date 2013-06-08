#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

import fileio

#DICT_FILE='../data/features/rid_lenratio.dict'
#DICT_FILE='../data/features/rid_lennorm.dict'
#DICT_FILE='../data/features/rid_sentratio.dict'
#DICT_FILE='../data/features/rid_sentnorm.dict'
#DICT_FILE='../data/features/rid_general.dict'
#DICT_FILE='../data/features/rid_cateratio.dict'
DICT_FILE='../data/features/rid_third.dict'

def getIdList(l):
    return [item.strip("\n").split("\t\t")[0] for item in l]

def id_to_review(id_file):

    reviewList = fileio.read_fields_from_allcsv("../data/CSV/Train/",["id","reviewContent","reviewTime","userNick"])

    userandtime_rid = {}
    same = []

    for rid,review,time,user in reviewList:
        key = (user,time)
        if userandtime_rid.has_key(key):
            same.append(rid)
        else: userandtime_rid[key] = rid
    
    rid_review = dict([rid,review]for rid,review,time,user in reviewList)
    rid_time = dict([rid,time]for rid,review,time,user in reviewList)
    rid_user = dict([rid,user]for rid,review,time,user in reviewList)
    
    #for rid in id_list:
    #    print rid_review[rid],rid_objective[int(rid)],"\n"
    
    id_result = fileio.read_file_to_dict(id_file)
    id_result = sorted(id_result.items(),key=lambda x:x[1],reverse = True)
    for rid,result in id_result:
        if rid in same:
            continue
        rid = str(rid)
        print rid
        print rid_review[rid]
        print rid_time[rid]
        print rid_user[rid]
        print "result",result
        print "============================="

    
if __name__ == '__main__':
    id_to_review(DICT_FILE)
