#encoding=UTF-8
from pymongo import MongoClient
import re
import time

connection = MongoClient()
reviewdb = connection['reviewdb']
review_train = reviewdb['review_train']

rexExp = re.compile(r'cap'.decode('utf-8'))
#rexExp = re.compile(('\d+'),re.IGNORECASE)

#one = review_train.find_one({'reviews':{'$elemMatch':{'reviewContent':rexExp}}},{'reviews.Content'})
#
#print one
#
#for item in review_train.find({'reviews.reviewContent':rexExp},{'reviews.reviewContent'}):
#    print item
#    print item[2]['reviewContent']
#    time.sleep(2)
count = 0
for item in review_train.find():
    print "********************************"
    print item['title']
    for review in item['reviews']:
        if rexExp.search(review['reviewContent']) or rexExp.search(review['appendReview']):
        #if review.has_key('isfake') and review['isfake']==1:
            print review['id']
            print review['userNick']
            print review['reviewTime']
            print review['reviewContent']
        if review.has_key('isfake'):
            count = count +1

print count

connection.disconnect()
