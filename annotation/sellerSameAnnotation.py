from pymongo import MongoClient

connection = MongoClient()
reviewdb = connection['reviewdb']
collection = reviewdb['review_train']

for item1 in collection.find():
    sid1 = item1['sellerId']
    item1_id = item1['itemId']
    print "seller %s"%sid1
    print item1_id
    for item2 in collection.find({'sellerId':sid1}):
        if item2['itemId'] == item1_id:
            continue
        print item2['sellerId']
        print item2['title']
        item2_id = item2['itemId']
        for review1 in item1['reviews']:
            for review2 in item2['reviews']:
                if review1['userNick'] == review2['userNick']:
                    print "********************************************"

                    review2_id = review2['id']
                    print "userNick %s"%review1['userNick']
                    print "1 "+review1['reviewContent']
                    print "2 "+review2['reviewContent']
                    if not review1.has_key('isfake'):
                        review1_id = review1['id']
                        print "review1_id %s"%review1_id
                        c = int(input('review1:'))
                        collection.update({'reviews.id':review1_id},{"$set":{"reviews.$.isfake":c}})
                        if review2.has_key('isfake'):
                            break

                    if review2.has_key('isfake'):
                        continue
                    print "review2_id %s"%review2_id    
                    c = int(input('review2:'))
                    collection.update({'reviews.id':review2_id},{"$set":{"reviews.$.isfake":c}})
                   
connection.disconnect()
