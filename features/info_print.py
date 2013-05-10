#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

import fileio

#ID_FILE='../havealook/highSentiment_id.dat'
#ID_FILE='../havealook/replica_review.dat'
ID_FILE='data/replicaId3.dat'
#ID_FILE='data/replicaId2.dat'
#ID_FILE='lowresult.dat'
#ID_FILE='data/replica_high_freq.dat'

def getIdList(l):
    return [item.strip("\n").split("\t\t")[0] for item in l]

def id_to_review(id_file):

    #rid_objective = fileIO.readFileToDict("../data/features/rid_objective.dict")
    #id_list = getIdList(fileIO.readFileToList("../data/features/rid_objective.dict"))
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
    
    
    #rid_review = dict([rid,review] for rid,review in reviewList)
    
    #for rid in id_list:
    #    print rid_review[rid],rid_objective[int(rid)],"\n"
    
    id_list = fileio.read_file_to_list(id_file)

    for rid in id_list:
        if rid in same:
            continue
        print rid
        print rid_review[rid]
        print rid_time[rid]
        print rid_user[rid]
        print "============================="
    
if __name__ == '__main__':
    id_to_review(ID_FILE)
