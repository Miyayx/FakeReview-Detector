from pymongo import MongoClient

connection = MongoClient()
reviewdb = connection['reviewdb']
review_train = reviewdb['review_train']

review_id = "61996789393"

c = (input('review %s isfake? :'%review_id)    )
if c == 1 or c == 'y':
    review_train.update({'reviews.id':review_id},{'$set':{'reviews.$.isfake':int(1)}})
else:
    review_train.update({'reviews.id':review_id},{'$set':{'reviews.$.isfake':int(0)}})


