
from pymongo import MongoClient

connection = MongoClient()
reviewdb = connection['reviewdb']
review_train = reviewdb['review_train']
review_test = reviewdb['review_test']

for item in review_train.find():
    item_id = item['itemId']
    for review in item['reviews']:
        if review.has_key('isfake'):
            continue
        print "\n"    
        print "title: %s"%item['title']
        print "user: %s"%review['userNick']
        print "review_id: %s"%review['id']
        print review['reviewContent']
        print "append: %s"%review['appendReview']
        c = (input('isfake? :'))
        if c == 1 or c == 'y':
            review_train.update({'reviews.id':review['id']},{'$set':{'reviews.$.isfake':int(1)}})
        else:
            review_train.update({'reviews.id':review['id']},{'$set':{'reviews.$.isfake':int(0)}})

connection.disconnect()
