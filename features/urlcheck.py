#encoding=utf-8
import re
import time
from pymongo import MongoClient

import sys
sys.path.append("/home/yang/GraduationProject/utils/")
import fileio


def has_url(review):
    #urlRexExp = re.compile('([a-zA-Z]+|{[0-9]+[a-zA-Z]+}+[a-zA-Z]*|{[a-zA-Z]+[0-9]+}+[0-9]*)\.[a-z0-9-A-Z]+'.decode('utf-8'))
    #urlRexExp = re.compile(r'[a-zA-Z]+[0-9]*\.[a-z0-9-A-Z]+'.decode('utf-8'))
    urlRexExp = re.compile(r'\.com|\.net|\.cn|\.COM|\.CN|\.NET|QQ|Q群'.decode('utf-8'))#re.l忽略大小写
    spaceExp = re.compile(r'\s')
    return True if urlRexExp.search(spaceExp.sub('',review).lower()) else False

def url_proc(reviewobj):
    reviewobj["url"] = int(has_url(reviewobj["content"]))

def url_value(reviews):
    if isinstance(reviews,str):
        return int(has_url(reviews))
    elif isinstance(reviews,list):
        return [int(has_url(r)) for r in reviews]
    elif isinstance(reviews,dict):
        return dict([k,int(has_url(r))] for k,r in reviews.items())

if __name__ == "__main__":
    #connection = MongoClient()
    #reviewdb = connection['reviewdb']
    #review_train = reviewdb['review_train']
    #
    #count = 0
    #d = {}
    #l = []
    #for item in review_train.find():
    #    item_id = item['itemId']
    #    
    #    for review in item['reviews']:
    #        r_id = review['id']
    #        content = review['reviewContent']
    #        append = review['appendReview']
    #first remove all the space,then match regular
    #        if has_url(content) or has_url(append):
    #            #d[r_id] = content+"\t\t"+append+"\n"
    #            d[r_id] = 1
    #            print "review: %s"%content.encode('utf-8','ignore')
    #            print "append: %s\n"%append.encode('utf-8','ignore')
    #            #time.sleep(0.5)
    #        else: d[r_id] = 0
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
    
    #for k,v in d.items():
    #    print "%s\t\t%d"%(k,v)

    #connection.disconnect()
    
    #fileio.record_to_file("../data/features/url_id_feature.dat",d)

    review_list = fileio.read_fields_from_allcsv("../data/CSV/Train/",["id","reviewContent"])
    rid_review = dict(review_list)
    rid_url = dict([rid,int(has_url(review))] for rid,review in rid_review.iteritems())
    fileio.record_to_file("../data/new_features/rid_url.dict",rid_url)

