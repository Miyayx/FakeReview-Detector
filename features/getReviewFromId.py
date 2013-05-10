#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

from FileIO import FileIO

#ID_FILE='../havealook/highSentiment_id.dat'
#ID_FILE='../havealook/replica_review.dat'
#ID_FILE='data/replicaId.dat'
ID_FILE='data/replicaId2.dat'

def getIdList(l):
    return [item.strip("\n").split("\t\t")[0] for item in l]

fileIO = FileIO()
#rid_objective = fileIO.readFileToDict("../data/features/rid_objective.dict")
#id_list = getIdList(fileIO.readFileToList("../data/features/rid_objective.dict"))
reviewList = fileIO.readFieldsFromAllCSV("../data/CSV/Train/",["id","reviewContent","reviewTime","userNick"])

id_list = fileIO.readFileToList(ID_FILE)

rid_review = dict([rid,review]for rid,review,time,user in reviewList)
rid_time = dict([rid,time]for rid,review,time,user in reviewList)
rid_user = dict([rid,user]for rid,review,time,user in reviewList)


#rid_review = dict([rid,review] for rid,review in reviewList)

#for rid in id_list:
#    print rid_review[rid],rid_objective[int(rid)],"\n"

for rid in id_list:
    print rid_review[rid]
    print rid_time[rid]
    print rid_user[rid]
    print "============================="

