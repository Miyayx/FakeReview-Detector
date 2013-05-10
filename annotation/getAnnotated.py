#!/usr/bin/env python2.7
#encoding=utf-8

"""
"""

import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir) 

from pymongo import MongoClient
from features.FileIO import FileIO

connection = MongoClient()
reviewdb = connection['reviewdb']
review_train = reviewdb['review_train']
review_test = reviewdb['review_test']

d = {}
count = 0
fakeCount = 0
for item in review_train.find():
    item_id = item['itemId']
    for review in item['reviews']:
        if review.has_key('isfake'):
            if review['isfake'] == 1:
                fakeCount+=1
                print review['reviewContent'].encode('utf-8')
            d[review['id']]=review['isfake']
            count+=1

connection.disconnect()

print "Annotated:%d"%len(d)
print "Faked:%d"%fakeCount


fio = FileIO()
fio.recordToFile('../data/target/rid_target.dat',d)


