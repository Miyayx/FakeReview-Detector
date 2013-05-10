#encoding=utf-8

import time
from pymongo import MongoClient
connection = MongoClient()
reviewdb = connection['reviewdb']
review_train = reviewdb['review_train']

for item in review_train.find():
    item_id = item['itemId']
    reviewD = {}
    for review in item['reviews']:
        key = review['userNick']
        value = review['reviewContent']
        if reviewD.has_key(key):
            reviewD[key].append(review)
        else:
            reviewD[key] = []
            reviewD[key].append(review)
    for k,v in reviewD.items():
        if len(v) > 1:
#            time.sleep(2)
            print "\n"
            print "title: %s"%item['title']
            print "user: %s"%k
            for r in v:
                print "review_id: %s"%r['id']
                print "date: %s"%r['reviewTime']
                print r['reviewContent']
                print "append: %s"%r['appendReview']
            for r in v:
                if r.has_key('isfake'):
                    continue
                c = (input('review %s isfake? :'%r['id']))
                if c == 1 or c == 'y':
                    review_train.update({'reviews.id':r['id']},{'$set':{'reviews.$.isfake':int(1)}})
                else:
                    review_train.update({'reviews.id':r['id']},{'$set':{'reviews.$.isfake':int(0)}})

connection.disconnect()



