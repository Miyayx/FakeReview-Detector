#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

import fileio

ID_FILE = "data/replicaId.dat"

if __name__=="__main__":
    review_list = fileio.read_fields_from_allcsv("../data/CSV/Train/",["id","reviewContent","reviewTime","userNick"])

    rid_review = dict([rid,review]for rid,review,time,user in review_list)
    rid_time = dict([rid,time]for rid,review,time,user in review_list)
    rid_user = dict([rid,user]for rid,review,time,user in review_list)

    id_list = fileio.read_file_to_list(ID_FILE) 



    




