#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

import fileio

FEATURE_PATH = "../data/features/"

#ID_FILE='../havealook/highSentiment_id.dat'
#ID_FILE='../havealook/replica_review.dat'
#ID_FILE='../data/target/all_replicaId.dat'
#ID_FILE='../data/target/suspecion_id.dat'
#ID_FILE='../features/data/replicaId.dat'
#ID_FILE='../features/data/replicaId2.dat'
#ID_FILE='lowresult.dat'
#ID_FILE='../features/data/new_replicaId.dat'
#ID_FILE='../data/target/cluster_rid1.dat'
#ID_FILE='../data/target/cluster_rid2.dat'
#ID_FILE='../data/target/annotation_fake1.dat'
#ID_FILE='../data/target/annotation_fake2.dat'
#ID_FILE='../data/target/shingle_id2.dat'
#ID_FILE='../data/target/test.dat'
#ID_FILE='../logisticRegression7.log'
#ID_FILE='../data/target/all_fake.dat'
ID_FILE='../data/target/suspicion_id2.dat'

def getIdList(l):
    return [item.strip("\n").split("\t\t")[0] for item in l]

def id_to_review(id_file):
    rid_url = fileio.read_file_to_dict(FEATURE_PATH+"url_id_feature.dat")
    rid_sent = fileio.read_file_to_dict(FEATURE_PATH+"rid_sentnorm.dict")
    #rid_sent = fileio.read_file_to_dict(FEATURE_PATH+"rid_sentratio.dict")
    rid_general = fileio.read_file_to_dict(FEATURE_PATH+"rid_general.dict")
    rid_len = fileio.read_file_to_dict(FEATURE_PATH+"rid_lenrationorm.dict")
    #rid_len = fileio.read_file_to_dict(FEATURE_PATH+"rid_lenratio.dict")
    rid_cate = fileio.read_file_to_dict(FEATURE_PATH+"rid_cateratio.dict",delimiter=None)
 
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
    
    id_list = fileio.read_file_to_list(id_file)

    new = []
    for rid in id_list:
        if rid in new:
            continue
        else:
            new.append(rid)

    id_list = new

    for rid in id_list:
        if rid in same:
            continue
        rid = str(rid)
        try:
            print rid
            print rid_review[rid]
            print rid_time[rid]
            print rid_user[rid]
            #print "*********"
            rid = eval(rid)
            #print "url",rid_url[rid]
            #print "sent",rid_sent[rid]
            #print "general",rid_general[rid]
            #print "length",rid_len[rid]
            #print "dategory",rid_cate[rid]
            print "============================="
        except:
            print "Error",rid

if __name__ == '__main__':
    id_to_review(ID_FILE)
