#encoding=utf-8
from FileIO import FileIO

import re
import time
from pymongo import MongoClient
connection = MongoClient()
reviewdb = connection['reviewdb']
review_train = reviewdb['review_train']

#urlRexExp = re.compile('([a-zA-Z]+|{[0-9]+[a-zA-Z]+}+[a-zA-Z]*|{[a-zA-Z]+[0-9]+}+[0-9]*)\.[a-z0-9-A-Z]+'.decode('utf-8'))
#urlRexExp = re.compile(r'[a-zA-Z]+[0-9]*\.[a-z0-9-A-Z]+'.decode('utf-8'))
urlRexExp = re.compile(r'\.com|\.net|\.cn|\.COM|\.CN|\.NET'.decode('utf-8'))#re.l忽略大小写
spaceExp = re.compile(r'\s')
count = 0
d = {}
l = []
for item in review_train.find():
    item_id = item['itemId']
    
    for review in item['reviews']:
        r_id = review['id']
        content = review['reviewContent']
        append = review['appendReview']
#first remove all the space,then match regular
        if urlRexExp.search(spaceExp.sub('',content).lower()) or urlRexExp.search(spaceExp.sub('',append).lower()):
            #d[r_id] = content+"\t\t"+append+"\n"
            d[r_id] = 1
            #print "review: %s"%content.encode('utf-8','ignore')
            #print "append: %s\n"%append.encode('utf-8','ignore')
            #time.sleep(0.5)
        else: d[r_id] = 0
            #pass

       # if len(content) > 0:
       #     print content
       #     print "\n"
       #     time.sleep(0.3)
       # if len(append) > 0:
       #     print append
       #     print "\n"
       #     time.sleep(0.3)
       #     

connection.disconnect()

fio = FileIO()
fio.recordToFile("../data/features/url_id_feature.dat",d)
